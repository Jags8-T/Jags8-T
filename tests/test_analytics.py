from agents import analytics, data_ingestion


def test_compute_pass_fail_rate():
    results = data_ingestion.load_sample_results()
    rate = analytics.compute_pass_fail_rate(results)
    assert rate == 0.625


def test_compute_dashboard_metrics():
    metrics = analytics.compute_dashboard_metrics(data_ingestion.load_sample_results())
    assert metrics.total_tests == 8
    assert metrics.passed_tests == 5
    assert metrics.failed_tests == 3
    assert metrics.unique_systems == 3


def test_detect_alerts_when_threshold_low():
    alerts = analytics.detect_alerts(data_ingestion.load_sample_results(), fail_rate_threshold=0.2)
    assert any("High failure rate" in item for item in alerts)
