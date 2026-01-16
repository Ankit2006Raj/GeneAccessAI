"""
Automated Retraining Pipeline
Monitors model performance and triggers retraining when needed
"""

import json
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import pickle


class AutoRetrainingPipeline:
    """Manages automated model retraining"""
    
    def __init__(self, storage_dir='./retraining', monitor=None, version_manager=None):
        """
        Initialize retraining pipeline
        
        Args:
            storage_dir: Directory for retraining artifacts
            monitor: ModelPerformanceMonitor instance
            version_manager: ModelVersionManager instance
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.monitor = monitor
        self.version_manager = version_manager
        
        self.config_file = self.storage_dir / 'retraining_config.json'
        self.config = self._load_config()
        
        self.schedule_file = self.storage_dir / 'retraining_schedule.json'
        self.schedule = self._load_schedule()
    
    def _load_config(self):
        """Load retraining configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        
        # Default configuration
        return {
            'triggers': {
                'accuracy_drop': 0.05,  # Retrain if accuracy drops by 5%
                'data_drift': 0.15,  # Retrain if data drift exceeds 15%
                'time_based': 30,  # Retrain every 30 days
                'sample_threshold': 1000  # Retrain after 1000 new samples
            },
            'retraining_strategy': 'incremental',  # 'full' or 'incremental'
            'validation_split': 0.2,
            'min_improvement': 0.01,  # Minimum improvement to deploy new model
            'auto_deploy': False  # Automatically deploy if improvement threshold met
        }
    
    def _save_config(self):
        """Save retraining configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _load_schedule(self):
        """Load retraining schedule"""
        if self.schedule_file.exists():
            with open(self.schedule_file, 'r') as f:
                return json.load(f)
        return {
            'last_retrain': None,
            'next_scheduled_retrain': None,
            'retraining_history': []
        }
    
    def _save_schedule(self):
        """Save retraining schedule"""
        with open(self.schedule_file, 'w') as f:
            json.dump(self.schedule, f, indent=2)
    
    def configure_triggers(self, accuracy_drop=None, data_drift=None, 
                          time_based=None, sample_threshold=None):
        """Configure retraining triggers"""
        if accuracy_drop is not None:
            self.config['triggers']['accuracy_drop'] = accuracy_drop
        if data_drift is not None:
            self.config['triggers']['data_drift'] = data_drift
        if time_based is not None:
            self.config['triggers']['time_based'] = time_based
        if sample_threshold is not None:
            self.config['triggers']['sample_threshold'] = sample_threshold
        
        self._save_config()
        print("✓ Retraining triggers configured")
    
    def check_retraining_needed(self):
        """
        Check if retraining is needed based on configured triggers
        
        Returns:
            Dictionary with retraining decision and reasons
        """
        reasons = []
        should_retrain = False
        
        # Check accuracy drop
        if self.monitor:
            drift_report = self.monitor.detect_drift()
            
            if drift_report['status'] == 'monitored':
                # Check for accuracy degradation
                accuracy_alerts = [a for a in drift_report.get('alerts', []) 
                                 if a['type'] == 'accuracy_degradation']
                
                if accuracy_alerts:
                    should_retrain = True
                    reasons.append({
                        'trigger': 'accuracy_drop',
                        'details': accuracy_alerts[0]['message']
                    })
                
                # Check for data drift
                drift_alerts = [a for a in drift_report.get('alerts', []) 
                              if a['type'] == 'prediction_drift']
                
                if drift_alerts:
                    should_retrain = True
                    reasons.append({
                        'trigger': 'data_drift',
                        'details': drift_alerts[0]['message']
                    })
        
        # Check time-based trigger
        if self.schedule['last_retrain']:
            last_retrain = datetime.fromisoformat(self.schedule['last_retrain'])
            days_since_retrain = (datetime.now() - last_retrain).days
            
            if days_since_retrain >= self.config['triggers']['time_based']:
                should_retrain = True
                reasons.append({
                    'trigger': 'time_based',
                    'details': f"{days_since_retrain} days since last retraining"
                })
        elif self.config['triggers']['time_based'] > 0:
            # No previous retraining, schedule one
            should_retrain = True
            reasons.append({
                'trigger': 'time_based',
                'details': 'Initial retraining'
            })
        
        return {
            'should_retrain': should_retrain,
            'reasons': reasons,
            'timestamp': datetime.now().isoformat()
        }
    
    def retrain_model(self, training_data, labels, model_class, model_params=None):
        """
        Retrain model with new data
        
        Args:
            training_data: Training features
            labels: Training labels
            model_class: Model class to instantiate
            model_params: Model parameters
        
        Returns:
            Retraining results
        """
        print("Starting model retraining...")
        
        # Split data for validation
        from sklearn.model_selection import train_test_split
        
        X_train, X_val, y_train, y_val = train_test_split(
            training_data, labels,
            test_size=self.config['validation_split'],
            random_state=42
        )
        
        # Train new model
        model_params = model_params or {}
        new_model = model_class(**model_params)
        new_model.fit(X_train, y_train)
        
        # Evaluate on validation set
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        val_predictions = new_model.predict(X_val)
        
        new_metrics = {
            'accuracy': float(accuracy_score(y_val, val_predictions)),
            'precision': float(precision_score(y_val, val_predictions, average='weighted', zero_division=0)),
            'recall': float(recall_score(y_val, val_predictions, average='weighted', zero_division=0)),
            'f1_score': float(f1_score(y_val, val_predictions, average='weighted', zero_division=0))
        }
        
        # Compare with current model
        should_deploy = False
        improvement = 0
        
        if self.version_manager:
            try:
                current_model, current_info = self.version_manager.load_model()
                current_predictions = current_model.predict(X_val)
                current_accuracy = accuracy_score(y_val, current_predictions)
                
                improvement = new_metrics['accuracy'] - current_accuracy
                
                if improvement >= self.config['min_improvement']:
                    should_deploy = True
                    print(f"✓ New model shows improvement: {improvement:.2%}")
                else:
                    print(f"✗ New model improvement insufficient: {improvement:.2%}")
            except Exception as e:
                print(f"Could not compare with current model: {e}")
                should_deploy = True  # Deploy if no current model
        else:
            should_deploy = True
        
        # Register new model version
        if self.version_manager:
            version_id = self.version_manager.register_model(
                model=new_model,
                model_name='genetic_risk_predictor',
                metrics=new_metrics,
                params=model_params,
                tags={'retraining': 'automated', 'improvement': improvement}
            )
            
            # Auto-deploy if configured and improvement threshold met
            if self.config['auto_deploy'] and should_deploy:
                self.version_manager.set_active_version(version_id)
                print(f"✓ New model automatically deployed: {version_id}")
        
        # Update retraining schedule
        retraining_record = {
            'timestamp': datetime.now().isoformat(),
            'metrics': new_metrics,
            'improvement': improvement,
            'deployed': should_deploy,
            'training_samples': len(training_data)
        }
        
        self.schedule['last_retrain'] = datetime.now().isoformat()
        self.schedule['retraining_history'].append(retraining_record)
        
        # Schedule next retraining
        next_retrain = datetime.now() + timedelta(days=self.config['triggers']['time_based'])
        self.schedule['next_scheduled_retrain'] = next_retrain.isoformat()
        
        self._save_schedule()
        
        print("✓ Model retraining completed")
        
        return {
            'success': True,
            'metrics': new_metrics,
            'improvement': improvement,
            'should_deploy': should_deploy,
            'deployed': should_deploy and self.config['auto_deploy'],
            'version_id': version_id if self.version_manager else None
        }
    
    def schedule_retraining(self, days_from_now):
        """Schedule next retraining"""
        next_retrain = datetime.now() + timedelta(days=days_from_now)
        self.schedule['next_scheduled_retrain'] = next_retrain.isoformat()
        self._save_schedule()
        
        print(f"✓ Next retraining scheduled for {next_retrain.strftime('%Y-%m-%d')}")
    
    def get_retraining_status(self):
        """Get current retraining status"""
        status = {
            'last_retrain': self.schedule['last_retrain'],
            'next_scheduled_retrain': self.schedule['next_scheduled_retrain'],
            'retraining_history_count': len(self.schedule['retraining_history']),
            'config': self.config
        }
        
        # Check if retraining is needed
        retraining_check = self.check_retraining_needed()
        status['retraining_needed'] = retraining_check
        
        return status
    
    def get_retraining_history(self, limit=10):
        """Get recent retraining history"""
        history = self.schedule['retraining_history']
        return history[-limit:] if limit else history
    
    def run_pipeline(self, training_data, labels, model_class, model_params=None, force=False):
        """
        Run complete retraining pipeline
        
        Args:
            training_data: Training features
            labels: Training labels
            model_class: Model class
            model_params: Model parameters
            force: Force retraining even if not needed
        
        Returns:
            Pipeline execution results
        """
        print("=" * 60)
        print("Automated Retraining Pipeline")
        print("=" * 60)
        
        # Check if retraining is needed
        retraining_check = self.check_retraining_needed()
        
        if not force and not retraining_check['should_retrain']:
            print("✓ Retraining not needed at this time")
            return {
                'executed': False,
                'reason': 'Retraining not needed',
                'check': retraining_check
            }
        
        print("\nRetraining triggered:")
        for reason in retraining_check['reasons']:
            print(f"  - {reason['trigger']}: {reason['details']}")
        
        # Execute retraining
        print("\nExecuting retraining...")
        results = self.retrain_model(training_data, labels, model_class, model_params)
        
        return {
            'executed': True,
            'check': retraining_check,
            'results': results
        }
