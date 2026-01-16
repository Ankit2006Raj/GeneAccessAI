"""
Bias Detection and Mitigation
Detects and mitigates bias in ML models across protected attributes
"""

import numpy as np
from collections import defaultdict
import json
from pathlib import Path


class BiasDetector:
    """Detects and analyzes bias in model predictions"""
    
    def __init__(self, protected_attributes=None):
        """
        Initialize bias detector
        
        Args:
            protected_attributes: List of protected attribute names
                                 (e.g., ['gender', 'ethnicity', 'age_group'])
        """
        self.protected_attributes = protected_attributes or ['gender', 'ethnicity', 'age_group']
        self.bias_reports = []
    
    def calculate_demographic_parity(self, predictions, protected_attr_values):
        """
        Calculate demographic parity (equal positive prediction rates)
        
        Args:
            predictions: Binary predictions (0 or 1)
            protected_attr_values: Values of protected attribute
        
        Returns:
            Demographic parity difference
        """
        unique_groups = np.unique(protected_attr_values)
        
        positive_rates = {}
        for group in unique_groups:
            group_mask = protected_attr_values == group
            group_predictions = predictions[group_mask]
            
            if len(group_predictions) > 0:
                positive_rate = np.mean(group_predictions)
                positive_rates[str(group)] = float(positive_rate)
        
        if len(positive_rates) < 2:
            return 0.0, positive_rates
        
        # Calculate max difference
        rates = list(positive_rates.values())
        parity_diff = max(rates) - min(rates)
        
        return float(parity_diff), positive_rates
    
    def calculate_equal_opportunity(self, predictions, actuals, protected_attr_values):
        """
        Calculate equal opportunity (equal true positive rates)
        
        Args:
            predictions: Binary predictions
            actuals: Actual labels
            protected_attr_values: Values of protected attribute
        
        Returns:
            Equal opportunity difference
        """
        unique_groups = np.unique(protected_attr_values)
        
        tpr_by_group = {}
        for group in unique_groups:
            group_mask = protected_attr_values == group
            group_predictions = predictions[group_mask]
            group_actuals = actuals[group_mask]
            
            # Calculate TPR (True Positive Rate)
            positive_mask = group_actuals == 1
            if np.sum(positive_mask) > 0:
                tpr = np.mean(group_predictions[positive_mask])
                tpr_by_group[str(group)] = float(tpr)
        
        if len(tpr_by_group) < 2:
            return 0.0, tpr_by_group
        
        # Calculate max difference
        tprs = list(tpr_by_group.values())
        eo_diff = max(tprs) - min(tprs)
        
        return float(eo_diff), tpr_by_group
    
    def calculate_equalized_odds(self, predictions, actuals, protected_attr_values):
        """
        Calculate equalized odds (equal TPR and FPR)
        
        Args:
            predictions: Binary predictions
            actuals: Actual labels
            protected_attr_values: Values of protected attribute
        
        Returns:
            Equalized odds difference
        """
        unique_groups = np.unique(protected_attr_values)
        
        metrics_by_group = {}
        for group in unique_groups:
            group_mask = protected_attr_values == group
            group_predictions = predictions[group_mask]
            group_actuals = actuals[group_mask]
            
            # Calculate TPR
            positive_mask = group_actuals == 1
            tpr = 0.0
            if np.sum(positive_mask) > 0:
                tpr = np.mean(group_predictions[positive_mask])
            
            # Calculate FPR
            negative_mask = group_actuals == 0
            fpr = 0.0
            if np.sum(negative_mask) > 0:
                fpr = np.mean(group_predictions[negative_mask])
            
            metrics_by_group[str(group)] = {
                'tpr': float(tpr),
                'fpr': float(fpr)
            }
        
        if len(metrics_by_group) < 2:
            return 0.0, metrics_by_group
        
        # Calculate max TPR and FPR differences
        tprs = [m['tpr'] for m in metrics_by_group.values()]
        fprs = [m['fpr'] for m in metrics_by_group.values()]
        
        tpr_diff = max(tprs) - min(tprs)
        fpr_diff = max(fprs) - min(fprs)
        
        eo_diff = max(tpr_diff, fpr_diff)
        
        return float(eo_diff), metrics_by_group
    
    def calculate_disparate_impact(self, predictions, protected_attr_values):
        """
        Calculate disparate impact ratio
        
        Args:
            predictions: Binary predictions
            protected_attr_values: Values of protected attribute
        
        Returns:
            Disparate impact ratio (should be close to 1.0)
        """
        unique_groups = np.unique(protected_attr_values)
        
        if len(unique_groups) < 2:
            return 1.0, {}
        
        positive_rates = {}
        for group in unique_groups:
            group_mask = protected_attr_values == group
            group_predictions = predictions[group_mask]
            
            if len(group_predictions) > 0:
                positive_rate = np.mean(group_predictions)
                positive_rates[str(group)] = float(positive_rate)
        
        # Calculate disparate impact (min rate / max rate)
        rates = list(positive_rates.values())
        if max(rates) == 0:
            return 1.0, positive_rates
        
        di_ratio = min(rates) / max(rates)
        
        return float(di_ratio), positive_rates
    
    def analyze_bias(self, predictions, actuals, protected_attributes_data):
        """
        Comprehensive bias analysis
        
        Args:
            predictions: Model predictions (binary or continuous)
            actuals: Actual labels (optional, can be None)
            protected_attributes_data: Dictionary mapping attribute names to values
        
        Returns:
            Comprehensive bias report
        """
        # Convert predictions to binary if needed
        if predictions.dtype == float:
            binary_predictions = (predictions > 0.5).astype(int)
        else:
            binary_predictions = predictions
        
        report = {
            'timestamp': str(np.datetime64('now')),
            'total_samples': len(predictions),
            'bias_metrics': {}
        }
        
        for attr_name, attr_values in protected_attributes_data.items():
            attr_report = {}
            
            # Demographic Parity
            dp_diff, dp_rates = self.calculate_demographic_parity(
                binary_predictions, attr_values
            )
            attr_report['demographic_parity'] = {
                'difference': dp_diff,
                'rates_by_group': dp_rates,
                'threshold': 0.1,
                'passed': dp_diff < 0.1
            }
            
            # Disparate Impact
            di_ratio, di_rates = self.calculate_disparate_impact(
                binary_predictions, attr_values
            )
            attr_report['disparate_impact'] = {
                'ratio': di_ratio,
                'rates_by_group': di_rates,
                'threshold': 0.8,  # 80% rule
                'passed': di_ratio >= 0.8
            }
            
            # Equal Opportunity (if actuals available)
            if actuals is not None:
                eo_diff, eo_rates = self.calculate_equal_opportunity(
                    binary_predictions, actuals, attr_values
                )
                attr_report['equal_opportunity'] = {
                    'difference': eo_diff,
                    'tpr_by_group': eo_rates,
                    'threshold': 0.1,
                    'passed': eo_diff < 0.1
                }
                
                # Equalized Odds
                eqo_diff, eqo_metrics = self.calculate_equalized_odds(
                    binary_predictions, actuals, attr_values
                )
                attr_report['equalized_odds'] = {
                    'difference': eqo_diff,
                    'metrics_by_group': eqo_metrics,
                    'threshold': 0.1,
                    'passed': eqo_diff < 0.1
                }
            
            report['bias_metrics'][attr_name] = attr_report
        
        # Overall bias assessment
        report['overall_assessment'] = self._assess_overall_bias(report['bias_metrics'])
        
        self.bias_reports.append(report)
        
        return report
    
    def _assess_overall_bias(self, bias_metrics):
        """Assess overall bias level"""
        total_checks = 0
        passed_checks = 0
        
        for attr_name, attr_metrics in bias_metrics.items():
            for metric_name, metric_data in attr_metrics.items():
                if 'passed' in metric_data:
                    total_checks += 1
                    if metric_data['passed']:
                        passed_checks += 1
        
        if total_checks == 0:
            return {
                'status': 'unknown',
                'pass_rate': 0.0,
                'recommendation': 'Insufficient data for bias assessment'
            }
        
        pass_rate = passed_checks / total_checks
        
        if pass_rate >= 0.9:
            status = 'low_bias'
            recommendation = 'Model shows low bias. Continue monitoring.'
        elif pass_rate >= 0.7:
            status = 'moderate_bias'
            recommendation = 'Model shows moderate bias. Consider bias mitigation techniques.'
        else:
            status = 'high_bias'
            recommendation = 'Model shows significant bias. Bias mitigation required.'
        
        return {
            'status': status,
            'pass_rate': pass_rate,
            'passed_checks': passed_checks,
            'total_checks': total_checks,
            'recommendation': recommendation
        }
    
    def generate_bias_report(self, report):
        """Generate human-readable bias report"""
        text = "Bias Detection Report\n"
        text += "=" * 60 + "\n\n"
        
        text += f"Total Samples: {report['total_samples']}\n"
        text += f"Timestamp: {report['timestamp']}\n\n"
        
        text += "Overall Assessment:\n"
        text += "-" * 60 + "\n"
        assessment = report['overall_assessment']
        text += f"Status: {assessment['status'].upper()}\n"
        text += f"Pass Rate: {assessment['pass_rate']:.1%}\n"
        text += f"Recommendation: {assessment['recommendation']}\n\n"
        
        for attr_name, attr_metrics in report['bias_metrics'].items():
            text += f"\nProtected Attribute: {attr_name.upper()}\n"
            text += "-" * 60 + "\n"
            
            for metric_name, metric_data in attr_metrics.items():
                text += f"\n{metric_name.replace('_', ' ').title()}:\n"
                
                if 'difference' in metric_data:
                    text += f"  Difference: {metric_data['difference']:.4f}\n"
                if 'ratio' in metric_data:
                    text += f"  Ratio: {metric_data['ratio']:.4f}\n"
                
                text += f"  Threshold: {metric_data['threshold']}\n"
                text += f"  Status: {'✓ PASSED' if metric_data['passed'] else '✗ FAILED'}\n"
        
        return text
    
    def save_report(self, report, filepath):
        """Save bias report to file"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Also save human-readable version
        text_report = self.generate_bias_report(report)
        text_filepath = filepath.with_suffix('.txt')
        with open(text_filepath, 'w') as f:
            f.write(text_report)
        
        print(f"✓ Bias report saved to {filepath}")
    
    def suggest_mitigation_strategies(self, report):
        """Suggest bias mitigation strategies based on report"""
        strategies = []
        
        assessment = report['overall_assessment']
        
        if assessment['status'] == 'high_bias':
            strategies.append({
                'strategy': 'Resampling',
                'description': 'Balance training data across protected groups',
                'priority': 'high'
            })
            strategies.append({
                'strategy': 'Reweighting',
                'description': 'Assign higher weights to underrepresented groups',
                'priority': 'high'
            })
        
        if assessment['status'] in ['moderate_bias', 'high_bias']:
            strategies.append({
                'strategy': 'Fairness Constraints',
                'description': 'Add fairness constraints during model training',
                'priority': 'medium'
            })
            strategies.append({
                'strategy': 'Post-processing',
                'description': 'Adjust predictions to satisfy fairness criteria',
                'priority': 'medium'
            })
        
        strategies.append({
            'strategy': 'Regular Monitoring',
            'description': 'Continuously monitor bias metrics in production',
            'priority': 'high'
        })
        
        return strategies
