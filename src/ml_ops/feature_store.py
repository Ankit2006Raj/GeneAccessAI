"""
Feature Store
Centralized storage and management of ML features
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class FeatureStore:
    """Manages feature storage, versioning, and retrieval"""
    
    def __init__(self, storage_dir='./feature_store'):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.features_dir = self.storage_dir / 'features'
        self.features_dir.mkdir(exist_ok=True)
        
        self.metadata_file = self.storage_dir / 'metadata.json'
        self.metadata = self._load_metadata()
    
    def _load_metadata(self):
        """Load feature metadata"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {
            'feature_groups': {},
            'feature_definitions': {},
            'versions': []
        }
    
    def _save_metadata(self):
        """Save feature metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def register_feature_group(self, group_name, features, description=''):
        """
        Register a group of related features
        
        Args:
            group_name: Name of the feature group
            features: List of feature names
            description: Description of the feature group
        """
        self.metadata['feature_groups'][group_name] = {
            'features': features,
            'description': description,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        self._save_metadata()
        print(f"✓ Feature group '{group_name}' registered with {len(features)} features")
    
    def register_feature(self, feature_name, feature_type, description='', 
                        transformation=None, dependencies=None):
        """
        Register a single feature definition
        
        Args:
            feature_name: Name of the feature
            feature_type: Type of feature ('numerical', 'categorical', 'binary')
            description: Description of the feature
            transformation: Transformation applied to create feature
            dependencies: List of dependent features
        """
        self.metadata['feature_definitions'][feature_name] = {
            'type': feature_type,
            'description': description,
            'transformation': transformation,
            'dependencies': dependencies or [],
            'created_at': datetime.now().isoformat()
        }
        
        self._save_metadata()
        print(f"✓ Feature '{feature_name}' registered")
    
    def store_features(self, entity_id, features_dict, version='latest'):
        """
        Store features for an entity
        
        Args:
            entity_id: Unique identifier for the entity
            features_dict: Dictionary of feature name -> value
            version: Version identifier
        """
        version_dir = self.features_dir / version
        version_dir.mkdir(exist_ok=True)
        
        entity_file = version_dir / f"{entity_id}.json"
        
        feature_data = {
            'entity_id': entity_id,
            'features': features_dict,
            'timestamp': datetime.now().isoformat(),
            'version': version
        }
        
        with open(entity_file, 'w') as f:
            json.dump(feature_data, f, indent=2)
    
    def get_features(self, entity_id, feature_names=None, version='latest'):
        """
        Retrieve features for an entity
        
        Args:
            entity_id: Unique identifier for the entity
            feature_names: List of specific features to retrieve (None for all)
            version: Version identifier
        
        Returns:
            Dictionary of features
        """
        version_dir = self.features_dir / version
        entity_file = version_dir / f"{entity_id}.json"
        
        if not entity_file.exists():
            return None
        
        with open(entity_file, 'r') as f:
            feature_data = json.load(f)
        
        features = feature_data['features']
        
        if feature_names:
            features = {k: v for k, v in features.items() if k in feature_names}
        
        return features
    
    def batch_store_features(self, features_df, entity_id_column, version='latest'):
        """
        Store features for multiple entities from DataFrame
        
        Args:
            features_df: DataFrame with features
            entity_id_column: Name of column containing entity IDs
            version: Version identifier
        """
        version_dir = self.features_dir / version
        version_dir.mkdir(exist_ok=True)
        
        stored_count = 0
        for _, row in features_df.iterrows():
            entity_id = row[entity_id_column]
            features_dict = row.drop(entity_id_column).to_dict()
            
            # Convert numpy types to Python types
            features_dict = {k: self._convert_to_python_type(v) 
                           for k, v in features_dict.items()}
            
            self.store_features(entity_id, features_dict, version)
            stored_count += 1
        
        print(f"✓ Stored features for {stored_count} entities")
    
    def _convert_to_python_type(self, value):
        """Convert numpy types to Python types"""
        if isinstance(value, (np.integer, np.floating)):
            return float(value)
        elif isinstance(value, np.ndarray):
            return value.tolist()
        return value
    
    def batch_get_features(self, entity_ids, feature_names=None, version='latest'):
        """
        Retrieve features for multiple entities
        
        Args:
            entity_ids: List of entity IDs
            feature_names: List of specific features to retrieve
            version: Version identifier
        
        Returns:
            DataFrame with features
        """
        features_list = []
        
        for entity_id in entity_ids:
            features = self.get_features(entity_id, feature_names, version)
            if features:
                features['entity_id'] = entity_id
                features_list.append(features)
        
        if not features_list:
            return None
        
        return pd.DataFrame(features_list)
    
    def create_feature_version(self, version_name, description=''):
        """Create a new feature version"""
        version_info = {
            'version_name': version_name,
            'description': description,
            'created_at': datetime.now().isoformat()
        }
        
        self.metadata['versions'].append(version_info)
        self._save_metadata()
        
        version_dir = self.features_dir / version_name
        version_dir.mkdir(exist_ok=True)
        
        print(f"✓ Feature version '{version_name}' created")
    
    def list_feature_groups(self):
        """List all registered feature groups"""
        return list(self.metadata['feature_groups'].keys())
    
    def get_feature_group(self, group_name):
        """Get feature group definition"""
        return self.metadata['feature_groups'].get(group_name)
    
    def get_feature_definition(self, feature_name):
        """Get feature definition"""
        return self.metadata['feature_definitions'].get(feature_name)
    
    def compute_feature_statistics(self, version='latest'):
        """Compute statistics for all features in a version"""
        version_dir = self.features_dir / version
        
        if not version_dir.exists():
            return None
        
        all_features = defaultdict(list)
        
        for entity_file in version_dir.glob('*.json'):
            with open(entity_file, 'r') as f:
                feature_data = json.load(f)
                for feature_name, value in feature_data['features'].items():
                    if isinstance(value, (int, float)):
                        all_features[feature_name].append(value)
        
        statistics = {}
        for feature_name, values in all_features.items():
            if values:
                statistics[feature_name] = {
                    'count': len(values),
                    'mean': float(np.mean(values)),
                    'std': float(np.std(values)),
                    'min': float(np.min(values)),
                    'max': float(np.max(values)),
                    'median': float(np.median(values))
                }
        
        return statistics
    
    def validate_features(self, features_dict):
        """Validate features against registered definitions"""
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        for feature_name, value in features_dict.items():
            if feature_name not in self.metadata['feature_definitions']:
                validation_results['warnings'].append(
                    f"Feature '{feature_name}' not registered"
                )
                continue
            
            definition = self.metadata['feature_definitions'][feature_name]
            feature_type = definition['type']
            
            # Type validation
            if feature_type == 'numerical':
                if not isinstance(value, (int, float)):
                    validation_results['valid'] = False
                    validation_results['errors'].append(
                        f"Feature '{feature_name}' should be numerical, got {type(value)}"
                    )
            elif feature_type == 'categorical':
                if not isinstance(value, str):
                    validation_results['valid'] = False
                    validation_results['errors'].append(
                        f"Feature '{feature_name}' should be categorical (string), got {type(value)}"
                    )
            elif feature_type == 'binary':
                if value not in [0, 1, True, False]:
                    validation_results['valid'] = False
                    validation_results['errors'].append(
                        f"Feature '{feature_name}' should be binary (0/1), got {value}"
                    )
        
        return validation_results
    
    def export_features(self, version='latest', output_format='csv'):
        """Export all features to file"""
        version_dir = self.features_dir / version
        
        if not version_dir.exists():
            print(f"Version '{version}' not found")
            return None
        
        all_data = []
        for entity_file in version_dir.glob('*.json'):
            with open(entity_file, 'r') as f:
                feature_data = json.load(f)
                all_data.append(feature_data['features'])
        
        if not all_data:
            print("No features found")
            return None
        
        df = pd.DataFrame(all_data)
        
        output_file = self.storage_dir / f"features_{version}.{output_format}"
        
        if output_format == 'csv':
            df.to_csv(output_file, index=False)
        elif output_format == 'parquet':
            df.to_parquet(output_file, index=False)
        elif output_format == 'json':
            df.to_json(output_file, orient='records', indent=2)
        
        print(f"✓ Features exported to {output_file}")
        return output_file
