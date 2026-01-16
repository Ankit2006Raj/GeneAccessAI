"""
Model Versioning with MLflow and DVC
Tracks model versions, experiments, and artifacts
"""

import os
import json
import pickle
import hashlib
from datetime import datetime
from pathlib import Path
import shutil

try:
    import mlflow
    import mlflow.sklearn
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    print("MLflow not installed. Using fallback versioning.")


class ModelVersionManager:
    """Manages model versions with MLflow integration and fallback"""
    
    def __init__(self, tracking_uri='./mlruns', experiment_name='genetic_risk_prediction'):
        self.tracking_uri = tracking_uri
        self.experiment_name = experiment_name
        self.models_dir = Path('models/versions')
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata_file = self.models_dir / 'metadata.json'
        self.metadata = self._load_metadata()
        
        if MLFLOW_AVAILABLE:
            mlflow.set_tracking_uri(tracking_uri)
            mlflow.set_experiment(experiment_name)
    
    def _load_metadata(self):
        """Load version metadata"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {'versions': [], 'active_version': None, 'champion_model': None}
    
    def _save_metadata(self):
        """Save version metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def _compute_model_hash(self, model_path):
        """Compute hash of model file"""
        hasher = hashlib.sha256()
        with open(model_path, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()[:16]
    
    def register_model(self, model, model_name, metrics, params, tags=None):
        """
        Register a new model version
        
        Args:
            model: Trained model object
            model_name: Name of the model
            metrics: Dictionary of performance metrics
            params: Dictionary of model parameters
            tags: Optional tags for the model
        
        Returns:
            version_id: Unique version identifier
        """
        version_id = f"v{len(self.metadata['versions']) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        model_path = self.models_dir / f"{model_name}_{version_id}.pkl"
        
        # Save model locally
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        model_hash = self._compute_model_hash(model_path)
        
        version_info = {
            'version_id': version_id,
            'model_name': model_name,
            'model_path': str(model_path),
            'model_hash': model_hash,
            'metrics': metrics,
            'params': params,
            'tags': tags or {},
            'created_at': datetime.now().isoformat(),
            'status': 'registered'
        }
        
        # Log to MLflow if available
        if MLFLOW_AVAILABLE:
            try:
                with mlflow.start_run(run_name=f"{model_name}_{version_id}"):
                    # Log parameters
                    mlflow.log_params(params)
                    
                    # Log metrics
                    mlflow.log_metrics(metrics)
                    
                    # Log model
                    mlflow.sklearn.log_model(model, "model")
                    
                    # Log tags
                    if tags:
                        mlflow.set_tags(tags)
                    
                    version_info['mlflow_run_id'] = mlflow.active_run().info.run_id
            except Exception as e:
                print(f"MLflow logging failed: {e}")
        
        self.metadata['versions'].append(version_info)
        
        # Set as active if first version
        if not self.metadata['active_version']:
            self.metadata['active_version'] = version_id
        
        self._save_metadata()
        
        print(f"✓ Model registered: {version_id}")
        print(f"  Metrics: {metrics}")
        
        return version_id
    
    def load_model(self, version_id=None):
        """Load a specific model version or the active version"""
        if version_id is None:
            version_id = self.metadata['active_version']
        
        if not version_id:
            raise ValueError("No active model version found")
        
        version_info = next((v for v in self.metadata['versions'] if v['version_id'] == version_id), None)
        
        if not version_info:
            raise ValueError(f"Version {version_id} not found")
        
        model_path = Path(version_info['model_path'])
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        return model, version_info
    
    def set_active_version(self, version_id):
        """Set the active model version"""
        version_info = next((v for v in self.metadata['versions'] if v['version_id'] == version_id), None)
        
        if not version_info:
            raise ValueError(f"Version {version_id} not found")
        
        self.metadata['active_version'] = version_id
        self._save_metadata()
        
        print(f"✓ Active version set to: {version_id}")
    
    def promote_to_champion(self, version_id):
        """Promote a model version to champion (production)"""
        version_info = next((v for v in self.metadata['versions'] if v['version_id'] == version_id), None)
        
        if not version_info:
            raise ValueError(f"Version {version_id} not found")
        
        # Demote previous champion
        if self.metadata['champion_model']:
            prev_champion = next((v for v in self.metadata['versions'] 
                                 if v['version_id'] == self.metadata['champion_model']), None)
            if prev_champion:
                prev_champion['status'] = 'archived'
        
        version_info['status'] = 'champion'
        self.metadata['champion_model'] = version_id
        self._save_metadata()
        
        print(f"✓ Model promoted to champion: {version_id}")
    
    def compare_versions(self, version_ids, metric='accuracy'):
        """Compare multiple model versions"""
        results = []
        
        for vid in version_ids:
            version_info = next((v for v in self.metadata['versions'] if v['version_id'] == vid), None)
            if version_info:
                results.append({
                    'version_id': vid,
                    'metric_value': version_info['metrics'].get(metric, 0),
                    'created_at': version_info['created_at'],
                    'status': version_info['status']
                })
        
        # Sort by metric value
        results.sort(key=lambda x: x['metric_value'], reverse=True)
        
        return results
    
    def list_versions(self, status=None):
        """List all model versions"""
        versions = self.metadata['versions']
        
        if status:
            versions = [v for v in versions if v['status'] == status]
        
        return versions
    
    def get_version_info(self, version_id):
        """Get detailed information about a version"""
        return next((v for v in self.metadata['versions'] if v['version_id'] == version_id), None)
    
    def rollback_to_version(self, version_id):
        """Rollback to a previous version"""
        version_info = next((v for v in self.metadata['versions'] if v['version_id'] == version_id), None)
        
        if not version_info:
            raise ValueError(f"Version {version_id} not found")
        
        self.set_active_version(version_id)
        print(f"✓ Rolled back to version: {version_id}")
    
    def archive_old_versions(self, keep_last_n=5):
        """Archive old model versions, keeping only the last N"""
        versions = sorted(self.metadata['versions'], 
                         key=lambda x: x['created_at'], 
                         reverse=True)
        
        archived_count = 0
        for version in versions[keep_last_n:]:
            if version['status'] not in ['champion', 'active']:
                version['status'] = 'archived'
                archived_count += 1
        
        self._save_metadata()
        print(f"✓ Archived {archived_count} old versions")
