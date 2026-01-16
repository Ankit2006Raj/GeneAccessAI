"""
Model Performance Monitoring
Tracks model performance, data drift, and prediction quality in production
"""

import json
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import warnings


class ModelPerformanceMonitor:
    """Monitors model performance and detects degradation"""
    
    def __init__(self, storage_dir='./monitoring'):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.metrics_file = self.storage_dir / 'metrics_log.jsonl'
        self.predictions_file = self.storage_dir / 'predictions_log.jsonl'
        self.alerts_file = self.storage_dir / 'alerts.json'
        
        self.thresholds = {
            'accuracy_drop': 0.05,  # Alert if accuracy drops by 5%
            'prediction_drift': 0.15,  # Alert if prediction distribution shifts by 15%
            'latency_increase': 2.0,  # Alert if latency doubles
            'error_rate': 0.10  # Alert if error rate exceeds 10%
        }
        
        self.baseline_metrics = self._load_baseline()
    
    def _load_baseline(self):
        """Load baseline metrics"""
        baseline_file = self.storage_dir / 'baseline_metrics.json'
        if baseline_file.exists():
            with open(baseline_file, 'r') as f:
                return json.load(f)
        return None
    
    def set_baseline(self, metrics):
        """Set baseline metrics for comparison"""
        self.baseline_metrics = {
            'accuracy': metrics.get('accuracy', 0),
            'precision': metrics.get('precision', 0),
            'recall': metrics.get('recall', 0),
            'f1_score': metrics.get('f1_score', 0),
            'avg_latency': metrics.get('avg_latency', 0),
            'prediction_distribution': metrics.get('prediction_distribution', {}),
            'timestamp': datetime.now().isoformat()
        }
        
        baseline_file = self.storage_dir / 'baseline_metrics.json'
        with open(baseline_file, 'w') as f:
            json.dump(self.baseline_metrics, f, indent=2)
        
        print("✓ Baseline metrics set")
    
    def log_prediction(self, features, prediction, actual=None, latency=None, metadata=None):
        """
        Log a single prediction for monitoring
        
        Args:
            features: Input features
            prediction: Model prediction
            actual: Actual label (if available)
            latency: Prediction latency in seconds
            metadata: Additional metadata
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'prediction': prediction,
            'actual': actual,
            'latency': latency,
            'features_hash': hash(str(features)),
            'metadata': metadata or {}
        }
        
        with open(self.predictions_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def log_metrics(self, metrics, model_version=None):
        """Log performance metrics"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'model_version': model_version,
            'metrics': metrics
        }
        
        with open(self.metrics_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def get_recent_predictions(self, hours=24):
        """Get predictions from the last N hours"""
        if not self.predictions_file.exists():
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        predictions = []
        
        with open(self.predictions_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                entry_time = datetime.fromisoformat(entry['timestamp'])
                if entry_time >= cutoff_time:
                    predictions.append(entry)
        
        return predictions
    
    def calculate_metrics(self, hours=24):
        """Calculate performance metrics from recent predictions"""
        predictions = self.get_recent_predictions(hours)
        
        if not predictions:
            return None
        
        # Filter predictions with actual labels
        labeled_predictions = [p for p in predictions if p.get('actual') is not None]
        
        if not labeled_predictions:
            return {
                'total_predictions': len(predictions),
                'avg_latency': np.mean([p['latency'] for p in predictions if p.get('latency')]),
                'prediction_distribution': self._calculate_distribution(predictions)
            }
        
        # Calculate accuracy
        correct = sum(1 for p in labeled_predictions 
                     if p['prediction'] == p['actual'])
        accuracy = correct / len(labeled_predictions)
        
        # Calculate latency
        latencies = [p['latency'] for p in predictions if p.get('latency')]
        avg_latency = np.mean(latencies) if latencies else None
        
        # Prediction distribution
        pred_dist = self._calculate_distribution(predictions)
        
        metrics = {
            'total_predictions': len(predictions),
            'labeled_predictions': len(labeled_predictions),
            'accuracy': accuracy,
            'avg_latency': avg_latency,
            'prediction_distribution': pred_dist,
            'timestamp': datetime.now().isoformat()
        }
        
        return metrics
    
    def _calculate_distribution(self, predictions):
        """Calculate prediction distribution"""
        dist = defaultdict(int)
        for p in predictions:
            pred = p['prediction']
            if isinstance(pred, dict):
                pred = pred.get('disorder', 'unknown')
            dist[str(pred)] += 1
        
        total = len(predictions)
        return {k: v/total for k, v in dist.items()}
    
    def detect_drift(self, hours=24):
        """Detect data drift and model degradation"""
        if not self.baseline_metrics:
            return {'status': 'no_baseline', 'alerts': []}
        
        current_metrics = self.calculate_metrics(hours)
        
        if not current_metrics:
            return {'status': 'insufficient_data', 'alerts': []}
        
        alerts = []
        
        # Check accuracy drift
        if 'accuracy' in current_metrics and 'accuracy' in self.baseline_metrics:
            accuracy_drop = self.baseline_metrics['accuracy'] - current_metrics['accuracy']
            if accuracy_drop > self.thresholds['accuracy_drop']:
                alerts.append({
                    'type': 'accuracy_degradation',
                    'severity': 'high',
                    'message': f"Accuracy dropped by {accuracy_drop:.2%}",
                    'baseline': self.baseline_metrics['accuracy'],
                    'current': current_metrics['accuracy']
                })
        
        # Check latency increase
        if current_metrics.get('avg_latency') and self.baseline_metrics.get('avg_latency'):
            latency_ratio = current_metrics['avg_latency'] / self.baseline_metrics['avg_latency']
            if latency_ratio > self.thresholds['latency_increase']:
                alerts.append({
                    'type': 'latency_increase',
                    'severity': 'medium',
                    'message': f"Latency increased by {(latency_ratio-1)*100:.1f}%",
                    'baseline': self.baseline_metrics['avg_latency'],
                    'current': current_metrics['avg_latency']
                })
        
        # Check prediction distribution drift
        if 'prediction_distribution' in current_metrics and 'prediction_distribution' in self.baseline_metrics:
            drift_score = self._calculate_distribution_drift(
                self.baseline_metrics['prediction_distribution'],
                current_metrics['prediction_distribution']
            )
            
            if drift_score > self.thresholds['prediction_drift']:
                alerts.append({
                    'type': 'prediction_drift',
                    'severity': 'medium',
                    'message': f"Prediction distribution shifted (drift score: {drift_score:.2f})",
                    'drift_score': drift_score
                })
        
        # Save alerts
        if alerts:
            self._save_alerts(alerts)
        
        return {
            'status': 'monitored',
            'alerts': alerts,
            'current_metrics': current_metrics,
            'baseline_metrics': self.baseline_metrics
        }
    
    def _calculate_distribution_drift(self, baseline_dist, current_dist):
        """Calculate distribution drift using Jensen-Shannon divergence"""
        all_keys = set(baseline_dist.keys()) | set(current_dist.keys())
        
        p = np.array([baseline_dist.get(k, 0) for k in all_keys])
        q = np.array([current_dist.get(k, 0) for k in all_keys])
        
        # Normalize
        p = p / (p.sum() + 1e-10)
        q = q / (q.sum() + 1e-10)
        
        # Jensen-Shannon divergence
        m = (p + q) / 2
        
        def kl_div(p, q):
            return np.sum(np.where(p != 0, p * np.log((p + 1e-10) / (q + 1e-10)), 0))
        
        js_div = (kl_div(p, m) + kl_div(q, m)) / 2
        
        return float(js_div)
    
    def _save_alerts(self, alerts):
        """Save alerts to file"""
        alert_entry = {
            'timestamp': datetime.now().isoformat(),
            'alerts': alerts
        }
        
        # Load existing alerts
        existing_alerts = []
        if self.alerts_file.exists():
            with open(self.alerts_file, 'r') as f:
                existing_alerts = json.load(f)
        
        existing_alerts.append(alert_entry)
        
        # Keep only last 100 alert entries
        existing_alerts = existing_alerts[-100:]
        
        with open(self.alerts_file, 'w') as f:
            json.dump(existing_alerts, f, indent=2)
    
    def get_dashboard_data(self, hours=24):
        """Get data for monitoring dashboard"""
        current_metrics = self.calculate_metrics(hours)
        drift_report = self.detect_drift(hours)
        
        # Get recent alerts
        recent_alerts = []
        if self.alerts_file.exists():
            with open(self.alerts_file, 'r') as f:
                all_alerts = json.load(f)
                recent_alerts = all_alerts[-10:]  # Last 10 alert entries
        
        return {
            'current_metrics': current_metrics,
            'baseline_metrics': self.baseline_metrics,
            'drift_report': drift_report,
            'recent_alerts': recent_alerts,
            'health_status': self._calculate_health_status(drift_report)
        }
    
    def _calculate_health_status(self, drift_report):
        """Calculate overall health status"""
        if drift_report['status'] != 'monitored':
            return 'unknown'
        
        alerts = drift_report.get('alerts', [])
        
        if not alerts:
            return 'healthy'
        
        high_severity = any(a['severity'] == 'high' for a in alerts)
        
        if high_severity:
            return 'critical'
        
        return 'warning'
