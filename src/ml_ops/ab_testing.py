"""
A/B Testing for ML Models
Manages experiments comparing different model versions
"""

import json
import numpy as np
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import random


class ABTestManager:
    """Manages A/B tests for model comparison"""
    
    def __init__(self, storage_dir='./ab_tests'):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.experiments_file = self.storage_dir / 'experiments.json'
        self.experiments = self._load_experiments()
        
        self.results_dir = self.storage_dir / 'results'
        self.results_dir.mkdir(exist_ok=True)
    
    def _load_experiments(self):
        """Load experiment configurations"""
        if self.experiments_file.exists():
            with open(self.experiments_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_experiments(self):
        """Save experiment configurations"""
        with open(self.experiments_file, 'w') as f:
            json.dump(self.experiments, f, indent=2)
    
    def create_experiment(self, experiment_name, model_a_version, model_b_version,
                         traffic_split=0.5, description='', success_metric='accuracy'):
        """
        Create a new A/B test experiment
        
        Args:
            experiment_name: Unique name for the experiment
            model_a_version: Version ID of model A (control)
            model_b_version: Version ID of model B (treatment)
            traffic_split: Fraction of traffic to model B (0.0 to 1.0)
            description: Description of the experiment
            success_metric: Primary metric to evaluate
        
        Returns:
            experiment_id
        """
        if experiment_name in self.experiments:
            raise ValueError(f"Experiment '{experiment_name}' already exists")
        
        experiment_id = f"exp_{len(self.experiments) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.experiments[experiment_name] = {
            'experiment_id': experiment_id,
            'model_a_version': model_a_version,
            'model_b_version': model_b_version,
            'traffic_split': traffic_split,
            'description': description,
            'success_metric': success_metric,
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'total_requests': 0,
            'model_a_requests': 0,
            'model_b_requests': 0
        }
        
        self._save_experiments()
        
        # Create results file
        results_file = self.results_dir / f"{experiment_id}.jsonl"
        results_file.touch()
        
        print(f"✓ Experiment '{experiment_name}' created")
        print(f"  Model A: {model_a_version}")
        print(f"  Model B: {model_b_version}")
        print(f"  Traffic Split: {traffic_split*100:.0f}% to Model B")
        
        return experiment_id
    
    def assign_variant(self, experiment_name, user_id=None):
        """
        Assign a user to a variant (model A or B)
        
        Args:
            experiment_name: Name of the experiment
            user_id: Optional user ID for consistent assignment
        
        Returns:
            'model_a' or 'model_b'
        """
        if experiment_name not in self.experiments:
            raise ValueError(f"Experiment '{experiment_name}' not found")
        
        experiment = self.experiments[experiment_name]
        
        if experiment['status'] != 'active':
            # Default to model A if experiment is not active
            return 'model_a'
        
        traffic_split = experiment['traffic_split']
        
        # Consistent assignment based on user_id
        if user_id is not None:
            hash_value = hash(f"{experiment_name}_{user_id}")
            assignment = (hash_value % 100) / 100.0
        else:
            assignment = random.random()
        
        variant = 'model_b' if assignment < traffic_split else 'model_a'
        
        # Update request counts
        experiment['total_requests'] += 1
        if variant == 'model_a':
            experiment['model_a_requests'] += 1
        else:
            experiment['model_b_requests'] += 1
        
        self._save_experiments()
        
        return variant
    
    def log_result(self, experiment_name, variant, prediction, actual=None, 
                   metrics=None, latency=None, user_id=None):
        """
        Log a result from the experiment
        
        Args:
            experiment_name: Name of the experiment
            variant: 'model_a' or 'model_b'
            prediction: Model prediction
            actual: Actual label (if available)
            metrics: Additional metrics
            latency: Prediction latency
            user_id: User ID
        """
        if experiment_name not in self.experiments:
            raise ValueError(f"Experiment '{experiment_name}' not found")
        
        experiment = self.experiments[experiment_name]
        experiment_id = experiment['experiment_id']
        
        result_entry = {
            'timestamp': datetime.now().isoformat(),
            'variant': variant,
            'prediction': prediction,
            'actual': actual,
            'metrics': metrics or {},
            'latency': latency,
            'user_id': user_id
        }
        
        results_file = self.results_dir / f"{experiment_id}.jsonl"
        with open(results_file, 'a') as f:
            f.write(json.dumps(result_entry) + '\n')
    
    def get_experiment_results(self, experiment_name):
        """Get results for an experiment"""
        if experiment_name not in self.experiments:
            raise ValueError(f"Experiment '{experiment_name}' not found")
        
        experiment = self.experiments[experiment_name]
        experiment_id = experiment['experiment_id']
        
        results_file = self.results_dir / f"{experiment_id}.jsonl"
        
        if not results_file.exists():
            return []
        
        results = []
        with open(results_file, 'r') as f:
            for line in f:
                results.append(json.loads(line))
        
        return results
    
    def analyze_experiment(self, experiment_name):
        """
        Analyze experiment results and determine winner
        
        Returns:
            Analysis report with statistical significance
        """
        if experiment_name not in self.experiments:
            raise ValueError(f"Experiment '{experiment_name}' not found")
        
        experiment = self.experiments[experiment_name]
        results = self.get_experiment_results(experiment_name)
        
        if not results:
            return {
                'status': 'insufficient_data',
                'message': 'No results available yet'
            }
        
        # Separate results by variant
        model_a_results = [r for r in results if r['variant'] == 'model_a']
        model_b_results = [r for r in results if r['variant'] == 'model_b']
        
        # Calculate metrics for each variant
        model_a_metrics = self._calculate_variant_metrics(model_a_results)
        model_b_metrics = self._calculate_variant_metrics(model_b_results)
        
        # Statistical significance test
        significance = self._test_significance(model_a_results, model_b_results)
        
        # Determine winner
        success_metric = experiment['success_metric']
        model_a_score = model_a_metrics.get(success_metric, 0)
        model_b_score = model_b_metrics.get(success_metric, 0)
        
        if model_b_score > model_a_score and significance['is_significant']:
            winner = 'model_b'
            improvement = ((model_b_score - model_a_score) / model_a_score) * 100
        elif model_a_score > model_b_score and significance['is_significant']:
            winner = 'model_a'
            improvement = ((model_a_score - model_b_score) / model_b_score) * 100
        else:
            winner = 'inconclusive'
            improvement = 0
        
        analysis = {
            'experiment_name': experiment_name,
            'status': 'analyzed',
            'model_a': {
                'version': experiment['model_a_version'],
                'requests': len(model_a_results),
                'metrics': model_a_metrics
            },
            'model_b': {
                'version': experiment['model_b_version'],
                'requests': len(model_b_results),
                'metrics': model_b_metrics
            },
            'winner': winner,
            'improvement': improvement,
            'statistical_significance': significance,
            'recommendation': self._generate_recommendation(winner, improvement, significance)
        }
        
        return analysis
    
    def _calculate_variant_metrics(self, results):
        """Calculate metrics for a variant"""
        if not results:
            return {}
        
        # Filter results with actual labels
        labeled_results = [r for r in results if r.get('actual') is not None]
        
        metrics = {
            'total_predictions': len(results)
        }
        
        if labeled_results:
            # Calculate accuracy
            correct = sum(1 for r in labeled_results 
                         if r['prediction'] == r['actual'])
            metrics['accuracy'] = correct / len(labeled_results)
        
        # Calculate average latency
        latencies = [r['latency'] for r in results if r.get('latency') is not None]
        if latencies:
            metrics['avg_latency'] = np.mean(latencies)
            metrics['p95_latency'] = np.percentile(latencies, 95)
        
        return metrics
    
    def _test_significance(self, model_a_results, model_b_results, alpha=0.05):
        """
        Test statistical significance using two-proportion z-test
        
        Args:
            model_a_results: Results from model A
            model_b_results: Results from model B
            alpha: Significance level
        
        Returns:
            Significance test results
        """
        # Filter labeled results
        a_labeled = [r for r in model_a_results if r.get('actual') is not None]
        b_labeled = [r for r in model_b_results if r.get('actual') is not None]
        
        if not a_labeled or not b_labeled:
            return {
                'is_significant': False,
                'p_value': None,
                'message': 'Insufficient labeled data for significance test'
            }
        
        # Calculate success rates
        n_a = len(a_labeled)
        n_b = len(b_labeled)
        
        success_a = sum(1 for r in a_labeled if r['prediction'] == r['actual'])
        success_b = sum(1 for r in b_labeled if r['prediction'] == r['actual'])
        
        p_a = success_a / n_a
        p_b = success_b / n_b
        
        # Pooled proportion
        p_pool = (success_a + success_b) / (n_a + n_b)
        
        # Standard error
        se = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
        
        if se == 0:
            return {
                'is_significant': False,
                'p_value': 1.0,
                'message': 'No variance in results'
            }
        
        # Z-score
        z_score = (p_b - p_a) / se
        
        # P-value (two-tailed test)
        from scipy import stats
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        
        return {
            'is_significant': p_value < alpha,
            'p_value': float(p_value),
            'z_score': float(z_score),
            'confidence_level': 1 - alpha,
            'sample_size_a': n_a,
            'sample_size_b': n_b
        }
    
    def _generate_recommendation(self, winner, improvement, significance):
        """Generate recommendation based on analysis"""
        if winner == 'inconclusive':
            if not significance['is_significant']:
                return "Continue experiment to gather more data. No significant difference detected yet."
            else:
                return "Models perform similarly. Consider other factors like latency or cost."
        
        if winner == 'model_b':
            if improvement > 5:
                return f"Model B shows significant improvement ({improvement:.1f}%). Recommend promoting to production."
            else:
                return f"Model B shows modest improvement ({improvement:.1f}%). Consider business impact before promotion."
        
        if winner == 'model_a':
            return f"Model A (control) performs better. Do not promote Model B."
        
        return "Insufficient data for recommendation."
    
    def stop_experiment(self, experiment_name):
        """Stop an active experiment"""
        if experiment_name not in self.experiments:
            raise ValueError(f"Experiment '{experiment_name}' not found")
        
        self.experiments[experiment_name]['status'] = 'stopped'
        self.experiments[experiment_name]['stopped_at'] = datetime.now().isoformat()
        self._save_experiments()
        
        print(f"✓ Experiment '{experiment_name}' stopped")
    
    def list_experiments(self, status=None):
        """List all experiments"""
        experiments = list(self.experiments.values())
        
        if status:
            experiments = [e for e in experiments if e['status'] == status]
        
        return experiments
