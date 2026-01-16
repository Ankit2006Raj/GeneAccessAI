"""
ML Ops API Routes
Exposes ML Ops functionality through REST API
"""

from flask import Blueprint, request, jsonify, send_file
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_ops.model_versioning import ModelVersionManager
from ml_ops.model_monitoring import ModelPerformanceMonitor
from ml_ops.model_explainability import ModelExplainer
from ml_ops.bias_detection import BiasDetector
from ml_ops.feature_store import FeatureStore
from ml_ops.ab_testing import ABTestManager
from ml_ops.retraining_pipeline import AutoRetrainingPipeline

mlops_bp = Blueprint('mlops', __name__, url_prefix='/api/mlops')

# Initialize ML Ops components
version_manager = ModelVersionManager()
monitor = ModelPerformanceMonitor()
feature_store = FeatureStore()
ab_manager = ABTestManager()
retraining_pipeline = AutoRetrainingPipeline(monitor=monitor, version_manager=version_manager)


# ============================================================================
# MODEL VERSIONING ENDPOINTS
# ============================================================================

@mlops_bp.route('/versions', methods=['GET'])
def list_versions():
    """List all model versions"""
    status = request.args.get('status')
    versions = version_manager.list_versions(status=status)
    return jsonify({'versions': versions})


@mlops_bp.route('/versions/<version_id>', methods=['GET'])
def get_version(version_id):
    """Get specific version information"""
    version_info = version_manager.get_version_info(version_id)
    if version_info:
        return jsonify(version_info)
    return jsonify({'error': 'Version not found'}), 404


@mlops_bp.route('/versions/active', methods=['GET'])
def get_active_version():
    """Get active model version"""
    active_version = version_manager.metadata.get('active_version')
    if active_version:
        version_info = version_manager.get_version_info(active_version)
        return jsonify(version_info)
    return jsonify({'error': 'No active version'}), 404


@mlops_bp.route('/versions/<version_id>/activate', methods=['POST'])
def activate_version(version_id):
    """Set a version as active"""
    try:
        version_manager.set_active_version(version_id)
        return jsonify({'success': True, 'active_version': version_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@mlops_bp.route('/versions/<version_id>/promote', methods=['POST'])
def promote_version(version_id):
    """Promote version to champion (production)"""
    try:
        version_manager.promote_to_champion(version_id)
        return jsonify({'success': True, 'champion_model': version_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@mlops_bp.route('/versions/compare', methods=['POST'])
def compare_versions():
    """Compare multiple model versions"""
    data = request.get_json()
    version_ids = data.get('version_ids', [])
    metric = data.get('metric', 'accuracy')
    
    comparison = version_manager.compare_versions(version_ids, metric)
    return jsonify({'comparison': comparison})


# ============================================================================
# MODEL MONITORING ENDPOINTS
# ============================================================================

@mlops_bp.route('/monitoring/dashboard', methods=['GET'])
def monitoring_dashboard():
    """Get monitoring dashboard data"""
    hours = int(request.args.get('hours', 24))
    dashboard_data = monitor.get_dashboard_data(hours=hours)
    return jsonify(dashboard_data)


@mlops_bp.route('/monitoring/metrics', methods=['GET'])
def get_metrics():
    """Get current performance metrics"""
    hours = int(request.args.get('hours', 24))
    metrics = monitor.calculate_metrics(hours=hours)
    return jsonify(metrics)


@mlops_bp.route('/monitoring/drift', methods=['GET'])
def check_drift():
    """Check for model drift"""
    hours = int(request.args.get('hours', 24))
    drift_report = monitor.detect_drift(hours=hours)
    return jsonify(drift_report)


@mlops_bp.route('/monitoring/baseline', methods=['POST'])
def set_baseline():
    """Set baseline metrics"""
    data = request.get_json()
    metrics = data.get('metrics', {})
    monitor.set_baseline(metrics)
    return jsonify({'success': True, 'baseline': metrics})


# ============================================================================
# MODEL EXPLAINABILITY ENDPOINTS
# ============================================================================

@mlops_bp.route('/explain', methods=['POST'])
def explain_prediction():
    """Explain a model prediction"""
    data = request.get_json()
    
    # This would need the actual model and explainer initialized
    # For now, return a placeholder response
    return jsonify({
        'method': 'SHAP',
        'explanation': 'Explainability requires model context',
        'note': 'Initialize ModelExplainer with your trained model'
    })


# ============================================================================
# BIAS DETECTION ENDPOINTS
# ============================================================================

@mlops_bp.route('/bias/analyze', methods=['POST'])
def analyze_bias():
    """Analyze model for bias"""
    data = request.get_json()
    
    # This would need actual predictions and protected attributes
    # For now, return a placeholder response
    return jsonify({
        'status': 'pending',
        'message': 'Bias analysis requires predictions and protected attribute data',
        'note': 'Use BiasDetector.analyze_bias() with your data'
    })


# ============================================================================
# FEATURE STORE ENDPOINTS
# ============================================================================

@mlops_bp.route('/features/groups', methods=['GET'])
def list_feature_groups():
    """List all feature groups"""
    groups = feature_store.list_feature_groups()
    return jsonify({'feature_groups': groups})


@mlops_bp.route('/features/groups/<group_name>', methods=['GET'])
def get_feature_group(group_name):
    """Get feature group definition"""
    group = feature_store.get_feature_group(group_name)
    if group:
        return jsonify(group)
    return jsonify({'error': 'Feature group not found'}), 404


@mlops_bp.route('/features/<entity_id>', methods=['GET'])
def get_features(entity_id):
    """Get features for an entity"""
    version = request.args.get('version', 'latest')
    features = feature_store.get_features(entity_id, version=version)
    
    if features:
        return jsonify({'entity_id': entity_id, 'features': features})
    return jsonify({'error': 'Features not found'}), 404


@mlops_bp.route('/features/statistics', methods=['GET'])
def get_feature_statistics():
    """Get feature statistics"""
    version = request.args.get('version', 'latest')
    stats = feature_store.compute_feature_statistics(version=version)
    return jsonify({'statistics': stats})


# ============================================================================
# A/B TESTING ENDPOINTS
# ============================================================================

@mlops_bp.route('/experiments', methods=['GET'])
def list_experiments():
    """List all A/B test experiments"""
    status = request.args.get('status')
    experiments = ab_manager.list_experiments(status=status)
    return jsonify({'experiments': experiments})


@mlops_bp.route('/experiments/<experiment_name>', methods=['GET'])
def get_experiment(experiment_name):
    """Get experiment details"""
    if experiment_name in ab_manager.experiments:
        return jsonify(ab_manager.experiments[experiment_name])
    return jsonify({'error': 'Experiment not found'}), 404


@mlops_bp.route('/experiments/<experiment_name>/analyze', methods=['GET'])
def analyze_experiment(experiment_name):
    """Analyze experiment results"""
    try:
        analysis = ab_manager.analyze_experiment(experiment_name)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@mlops_bp.route('/experiments/<experiment_name>/stop', methods=['POST'])
def stop_experiment(experiment_name):
    """Stop an experiment"""
    try:
        ab_manager.stop_experiment(experiment_name)
        return jsonify({'success': True, 'status': 'stopped'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ============================================================================
# RETRAINING PIPELINE ENDPOINTS
# ============================================================================

@mlops_bp.route('/retraining/status', methods=['GET'])
def retraining_status():
    """Get retraining pipeline status"""
    status = retraining_pipeline.get_retraining_status()
    return jsonify(status)


@mlops_bp.route('/retraining/check', methods=['GET'])
def check_retraining():
    """Check if retraining is needed"""
    check_result = retraining_pipeline.check_retraining_needed()
    return jsonify(check_result)


@mlops_bp.route('/retraining/history', methods=['GET'])
def retraining_history():
    """Get retraining history"""
    limit = int(request.args.get('limit', 10))
    history = retraining_pipeline.get_retraining_history(limit=limit)
    return jsonify({'history': history})


@mlops_bp.route('/retraining/configure', methods=['POST'])
def configure_retraining():
    """Configure retraining triggers"""
    data = request.get_json()
    
    retraining_pipeline.configure_triggers(
        accuracy_drop=data.get('accuracy_drop'),
        data_drift=data.get('data_drift'),
        time_based=data.get('time_based'),
        sample_threshold=data.get('sample_threshold')
    )
    
    return jsonify({'success': True, 'config': retraining_pipeline.config})


# ============================================================================
# HEALTH CHECK
# ============================================================================

@mlops_bp.route('/health', methods=['GET'])
def health_check():
    """ML Ops system health check"""
    return jsonify({
        'status': 'healthy',
        'components': {
            'version_manager': 'active',
            'monitor': 'active',
            'feature_store': 'active',
            'ab_testing': 'active',
            'retraining_pipeline': 'active'
        },
        'active_model_version': version_manager.metadata.get('active_version'),
        'champion_model': version_manager.metadata.get('champion_model')
    })
