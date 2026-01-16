"""
Model Explainability using SHAP and LIME
Provides interpretable explanations for model predictions
"""

import numpy as np
import warnings

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    print("SHAP not installed. Install with: pip install shap")

try:
    from lime import lime_tabular
    LIME_AVAILABLE = True
except ImportError:
    LIME_AVAILABLE = False
    print("LIME not installed. Install with: pip install lime")


class ModelExplainer:
    """Provides model explanations using SHAP and LIME"""
    
    def __init__(self, model, feature_names, training_data=None):
        """
        Initialize explainer
        
        Args:
            model: Trained model
            feature_names: List of feature names
            training_data: Training data for background distribution (optional)
        """
        self.model = model
        self.feature_names = feature_names
        self.training_data = training_data
        
        self.shap_explainer = None
        self.lime_explainer = None
        
        self._initialize_explainers()
    
    def _initialize_explainers(self):
        """Initialize SHAP and LIME explainers"""
        # Initialize SHAP
        if SHAP_AVAILABLE and self.training_data is not None:
            try:
                # Use TreeExplainer for tree-based models
                if hasattr(self.model, 'predict_proba'):
                    self.shap_explainer = shap.TreeExplainer(self.model)
                else:
                    # Use KernelExplainer as fallback
                    background = shap.sample(self.training_data, 100)
                    self.shap_explainer = shap.KernelExplainer(
                        self.model.predict, 
                        background
                    )
                print("✓ SHAP explainer initialized")
            except Exception as e:
                print(f"SHAP initialization failed: {e}")
        
        # Initialize LIME
        if LIME_AVAILABLE and self.training_data is not None:
            try:
                self.lime_explainer = lime_tabular.LimeTabularExplainer(
                    self.training_data,
                    feature_names=self.feature_names,
                    mode='classification',
                    discretize_continuous=True
                )
                print("✓ LIME explainer initialized")
            except Exception as e:
                print(f"LIME initialization failed: {e}")
    
    def explain_prediction_shap(self, instance, plot=False):
        """
        Explain prediction using SHAP
        
        Args:
            instance: Single instance to explain
            plot: Whether to generate plot (requires matplotlib)
        
        Returns:
            Dictionary with SHAP values and feature importance
        """
        if not SHAP_AVAILABLE or self.shap_explainer is None:
            return self._fallback_explanation(instance)
        
        try:
            # Get SHAP values
            shap_values = self.shap_explainer.shap_values(instance)
            
            # Handle multi-class output
            if isinstance(shap_values, list):
                shap_values = shap_values[0]
            
            # Get feature importance
            feature_importance = []
            for i, feature_name in enumerate(self.feature_names):
                importance = abs(shap_values[0][i]) if len(shap_values.shape) > 1 else abs(shap_values[i])
                feature_importance.append({
                    'feature': feature_name,
                    'importance': float(importance),
                    'value': float(instance[0][i]) if len(instance.shape) > 1 else float(instance[i])
                })
            
            # Sort by importance
            feature_importance.sort(key=lambda x: x['importance'], reverse=True)
            
            explanation = {
                'method': 'SHAP',
                'feature_importance': feature_importance,
                'top_features': feature_importance[:5]
            }
            
            return explanation
            
        except Exception as e:
            print(f"SHAP explanation failed: {e}")
            return self._fallback_explanation(instance)
    
    def explain_prediction_lime(self, instance, num_features=10):
        """
        Explain prediction using LIME
        
        Args:
            instance: Single instance to explain
            num_features: Number of top features to show
        
        Returns:
            Dictionary with LIME explanation
        """
        if not LIME_AVAILABLE or self.lime_explainer is None:
            return self._fallback_explanation(instance)
        
        try:
            # Flatten instance if needed
            instance_flat = instance.flatten() if len(instance.shape) > 1 else instance
            
            # Get LIME explanation
            exp = self.lime_explainer.explain_instance(
                instance_flat,
                self.model.predict_proba,
                num_features=num_features
            )
            
            # Extract feature importance
            feature_importance = []
            for feature_idx, weight in exp.as_list():
                # Parse feature name and value from LIME format
                feature_parts = feature_idx.split()
                feature_name = feature_parts[0] if feature_parts else f"feature_{feature_idx}"
                
                # Find actual feature index
                try:
                    feat_idx = self.feature_names.index(feature_name)
                    feature_value = float(instance_flat[feat_idx])
                except (ValueError, IndexError):
                    feature_value = 0.0
                
                feature_importance.append({
                    'feature': feature_name,
                    'importance': abs(float(weight)),
                    'contribution': float(weight),
                    'value': feature_value
                })
            
            # Sort by importance
            feature_importance.sort(key=lambda x: x['importance'], reverse=True)
            
            explanation = {
                'method': 'LIME',
                'feature_importance': feature_importance,
                'top_features': feature_importance[:5],
                'prediction_probability': exp.predict_proba
            }
            
            return explanation
            
        except Exception as e:
            print(f"LIME explanation failed: {e}")
            return self._fallback_explanation(instance)
    
    def _fallback_explanation(self, instance):
        """Fallback explanation using feature importance"""
        try:
            # Try to get feature importance from model
            if hasattr(self.model, 'feature_importances_'):
                importances = self.model.feature_importances_
            else:
                # Use uniform importance
                importances = np.ones(len(self.feature_names)) / len(self.feature_names)
            
            instance_flat = instance.flatten() if len(instance.shape) > 1 else instance
            
            feature_importance = []
            for i, feature_name in enumerate(self.feature_names):
                feature_importance.append({
                    'feature': feature_name,
                    'importance': float(importances[i]),
                    'value': float(instance_flat[i]) if i < len(instance_flat) else 0.0
                })
            
            feature_importance.sort(key=lambda x: x['importance'], reverse=True)
            
            return {
                'method': 'Feature Importance (Fallback)',
                'feature_importance': feature_importance,
                'top_features': feature_importance[:5]
            }
            
        except Exception as e:
            print(f"Fallback explanation failed: {e}")
            return {
                'method': 'None',
                'feature_importance': [],
                'top_features': [],
                'error': str(e)
            }
    
    def explain_prediction(self, instance, method='auto'):
        """
        Explain prediction using specified method
        
        Args:
            instance: Single instance to explain
            method: 'shap', 'lime', or 'auto' (tries SHAP first, then LIME)
        
        Returns:
            Explanation dictionary
        """
        if method == 'shap' or (method == 'auto' and SHAP_AVAILABLE):
            return self.explain_prediction_shap(instance)
        elif method == 'lime' or (method == 'auto' and LIME_AVAILABLE):
            return self.explain_prediction_lime(instance)
        else:
            return self._fallback_explanation(instance)
    
    def generate_explanation_report(self, instance, prediction):
        """
        Generate human-readable explanation report
        
        Args:
            instance: Single instance
            prediction: Model prediction
        
        Returns:
            Formatted explanation text
        """
        explanation = self.explain_prediction(instance)
        
        report = f"Prediction Explanation ({explanation['method']})\n"
        report += "=" * 50 + "\n\n"
        
        report += f"Predicted: {prediction}\n\n"
        
        report += "Top Contributing Factors:\n"
        report += "-" * 50 + "\n"
        
        for i, feat in enumerate(explanation['top_features'], 1):
            report += f"{i}. {feat['feature']}: "
            report += f"value={feat['value']:.2f}, "
            report += f"importance={feat['importance']:.4f}\n"
        
        return report
    
    def batch_explain(self, instances, method='auto'):
        """
        Explain multiple predictions
        
        Args:
            instances: Multiple instances to explain
            method: Explanation method
        
        Returns:
            List of explanations
        """
        explanations = []
        
        for instance in instances:
            exp = self.explain_prediction(instance.reshape(1, -1), method=method)
            explanations.append(exp)
        
        return explanations
    
    def get_global_feature_importance(self):
        """Get global feature importance from model"""
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            
            feature_importance = []
            for i, feature_name in enumerate(self.feature_names):
                feature_importance.append({
                    'feature': feature_name,
                    'importance': float(importances[i])
                })
            
            feature_importance.sort(key=lambda x: x['importance'], reverse=True)
            
            return feature_importance
        
        return None
