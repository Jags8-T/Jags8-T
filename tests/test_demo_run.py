from demo_run import build_demo_report


def test_build_demo_report_shape():
    report = build_demo_report()
    assert report["metrics"]["total_tests"] == 8
    assert "pass_rate_by_test" in report
    assert "copilot_examples" in report
    assert "summary" in report["copilot_examples"]
