from agents import analytics, data_ingestion


def test_compute_pass_fail_rate():
    results = data_ingestion.load_sample_results()
    rate = analytics.compute_pass_fail_rate(results)
    # There are two passing results out of four total
    assert rate == 0.5
