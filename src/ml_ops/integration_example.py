"""
Integration Example: Using ML Ops Components Together
Demonstrates how to use all ML Ops features in a production workflow
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

from model_versioning import ModelVersionManager
from model_monitoring import ModelPerformanceMonitor
from model_explainability import ModelExplainer
from bias_detection import BiasDetector
from feature_store import FeatureStore
from ab_testing import ABTestManager
from retraining_pipeline import AutoRetrainingPipeline


def complete_mlops_workflow():
    """
    Complete ML Ops workflow demonstration
    """
    print("=" * 70)
    print("COMPLETE ML OPS WORKFLOW DEMONSTRATION")
    print("=" * 70)
    
    # ========================================================================
    # 1. FEATURE STORE: Manage and version features
    # ========================================================================
    print("\n1. FEATURE STORE")
    print("-" * 70)
    
    feature_store = FeatureStore(storage_dir='./demo_feature_store')
    
    # Register feature groups
    feature_store.register_feature_group(
        'genetic_features',
        features=['age', 'symptom_count', 'family_history_score', 'ethnicity_code'],
        description='Core genetic risk assessment features'
    )
    
    # Register individual features
    feature_store.register_feature('age', 'numerical', 'Patient age in years')
    feature_store.register_feature('symptom_count', 'numerical', 'Number of symptoms')
    feature_store.register_feature('family_history_score', 'numerical', 'Family history risk score')
    feature_store.register_feature('ethnicity_code', 'categorical', 'Ethnicity category')
    
    # ========================================================================
    # 2. MODEL TRAINING AND VERSIONING
    # ========================================================================
    print("\n2. MODEL TRAINING AND VERSIONING")
    print("-" * 70)
    
    # Generate synthetic training data
    X_train, y_train = make_classification(
        n_samples=1000, n_features=10, n_informative=8,
        n_redundant=2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Calculate training metrics
    train_accuracy = model.score(X_train, y_train)
    
    # Version management
    version_manager = ModelVersionManager(
        tracking_uri='./demo_mlruns',
        experiment_name='genetic_risk_demo'
    )
    
    version_id = version_manager.register_model(
        model=model,
        model_name='genetic_risk_predictor',
        metrics={'accuracy': train_accuracy, 'n_estimators': 100},
        params={'n_estimators': 100, 'random_state': 42},
        tags={'environment': 'demo', 'algorithm': 'random_forest'}
    )
    
    print(f"Model registered with version: {version_id}")
    
    # ========================================================================
    # 3. MODEL EXPLAINABILITY
    # ========================================================================
    print("\n3. MODEL EXPLAINABILITY")
    print("-" * 70)
    
    feature_names = [f'feature_{i}' for i in range(10)]
    explainer = ModelExplainer(
        model=model,
        feature_names=feature_names,
        training_data=X_train
    )
    
    # Explain a single prediction
    test_instance = X_train[0:1]
    explanation = explainer.explain_prediction(test_instance, method='auto')
    
    print(f"Explanation method: {explanation['method']}")
    print("Top 3 contributing features:")
    for i, feat in enumerate(explanation['top_features'][:3], 1):
        print(f"  {i}. {feat['feature']}: importance={feat['importance']:.4f}")
    
    # ========================================================================
    # 4. BIAS DETECTION
    # ========================================================================
    print("\n4. BIAS DETECTION")
    print("-" * 70)
    
    # Generate synthetic protected attributes
    gender = np.random.choice(['male', 'female'], size=len(y_train))
    ethnicity = np.random.choice(['group_a', 'group_b', 'group_c'], size=len(y_train))
    
    # Get predictions
    predictions = model.predict(X_train)
    
    # Detect bias
    bias_detector = BiasDetector(protected_attributes=['gender', 'ethnicity'])
    
    bias_report = bias_detector.analyze_bias(
        predictions=predictions,
        actuals=y_train,
        protected_attributes_data={
            'gender': gender,
            'ethnicity': ethnicity
        }
    )
    
    print(f"Overall bias status: {bias_report['overall_assessment']['status']}")
    print(f"Pass rate: {bias_report['overall_assessment']['pass_rate']:.1%}")
    
    # ========================================================================
    # 5. MODEL MONITORING
    # ========================================================================
    print("\n5. MODEL MONITORING")
    print("-" * 70)
    
    monitor = ModelPerformanceMonitor(storage_dir='./demo_monitoring')
    
    # Set baseline metrics
    monitor.set_baseline({
        'accuracy': train_accuracy,
        'avg_latency': 0.05,
        'prediction_distribution': {'0': 0.5, '1': 0.5}
    })
    
    # Simulate production predictions
    X_test, y_test = make_classification(
        n_samples=100, n_features=10, n_informative=8,
        n_redundant=2, random_state=43
    )
    
    for i in range(len(X_test)):
        pred = model.predict(X_test[i:i+1])[0]
        monitor.log_prediction(
            features=X_test[i:i+1],
            prediction=pred,
            actual=y_test[i],
            latency=np.random.uniform(0.04, 0.06)
        )
    
    # Check for drift
    drift_report = monitor.detect_drift(hours=24)
    print(f"Drift detection status: {drift_report['status']}")
    print(f"Number of alerts: {len(drift_report.get('alerts', []))}")
    
    # ========================================================================
    # 6. A/B TESTING
    # ========================================================================
    print("\n6. A/B TESTING")
    print("-" * 70)
    
    ab_manager = ABTestManager(storage_dir='./demo_ab_tests')
    
    # Train a second model variant
    model_b = RandomForestClassifier(n_estimators=150, random_state=42)
    model_b.fit(X_train, y_train)
    
    version_id_b = version_manager.register_model(
        model=model_b,
        model_name='genetic_risk_predictor',
        metrics={'accuracy': model_b.score(X_train, y_train), 'n_estimators': 150},
        params={'n_estimators': 150, 'random_state': 42},
        tags={'environment': 'demo', 'algorithm': 'random_forest', 'variant': 'b'}
    )
    
    # Create A/B test
    experiment_id = ab_manager.create_experiment(
        experiment_name='rf_100_vs_150',
        model_a_version=version_id,
        model_b_version=version_id_b,
        traffic_split=0.5,
        description='Compare RF with 100 vs 150 estimators'
    )
    
    # Simulate A/B test traffic
    for i in range(100):
        variant = ab_manager.assign_variant('rf_100_vs_150', user_id=f"user_{i}")
        
        if variant == 'model_a':
            pred = model.predict(X_test[i:i+1])[0]
        else:
            pred = model_b.predict(X_test[i:i+1])[0]
        
        ab_manager.log_result(
            experiment_name='rf_100_vs_150',
            variant=variant,
            prediction=pred,
            actual=y_test[i],
            latency=np.random.uniform(0.04, 0.06)
        )
    
    # Analyze experiment
    analysis = ab_manager.analyze_experiment('rf_100_vs_150')
    print(f"A/B Test Winner: {analysis['winner']}")
    print(f"Recommendation: {analysis['recommendation']}")
    
    # ========================================================================
    # 7. AUTOMATED RETRAINING
    # ========================================================================
    print("\n7. AUTOMATED RETRAINING PIPELINE")
    print("-" * 70)
    
    retraining_pipeline = AutoRetrainingPipeline(
        storage_dir='./demo_retraining',
        monitor=monitor,
        version_manager=version_manager
    )
    
    # Configure triggers
    retraining_pipeline.configure_triggers(
        accuracy_drop=0.05,
        data_drift=0.15,
        time_based=30,
        sample_threshold=1000
    )
    
    # Check if retraining is needed
    retraining_check = retraining_pipeline.check_retraining_needed()
    print(f"Retraining needed: {retraining_check['should_retrain']}")
    
    if retraining_check['should_retrain']:
        print("Retraining reasons:")
        for reason in retraining_check['reasons']:
            print(f"  - {reason['trigger']}: {reason['details']}")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 70)
    print("WORKFLOW COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print("\nComponents demonstrated:")
    print("  ✓ Feature Store - Feature management and versioning")
    print("  ✓ Model Versioning - MLflow-based model tracking")
    print("  ✓ Model Explainability - SHAP/LIME explanations")
    print("  ✓ Bias Detection - Fairness metrics and analysis")
    print("  ✓ Model Monitoring - Performance tracking and drift detection")
    print("  ✓ A/B Testing - Experiment management and analysis")
    print("  ✓ Automated Retraining - Trigger-based model updates")
    print("\nAll components are production-ready and industry-standard!")


if __name__ == '__main__':
    complete_mlops_workflow()
