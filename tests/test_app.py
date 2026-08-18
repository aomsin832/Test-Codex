from streamlit.testing.v1 import AppTest
from pathlib import Path


def test_target_switch_updates_overview_without_value_leakage():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py", default_timeout=30).run()
    assert not app.exception
    atlas = {metric.label: metric.value for metric in app.metric[:8]}
    assert atlas["Enterprise Value"] == "$250.0m"
    assert atlas["Cyber findings"] == "14"
    assert atlas["Base synthetic remediation"] == "$6.3m"

    app.selectbox[0].set_value("forge").run()
    assert not app.exception
    forge = {metric.label: metric.value for metric in app.metric[:8]}
    assert forge["Enterprise Value"] == "$140.0m"
    assert forge["Cyber findings"] == "10"
    assert forge["Base synthetic remediation"] == "$14.1m"
    assert forge != atlas
    assert app.number_input[0].value == 140_000_000
    assert app.number_input[1].value == 14_000_000

    app.number_input[0].set_value(123_000_000).run()
    app.selectbox[0].set_value("harbor").run()
    assert not app.exception
    harbor = {metric.label: metric.value for metric in app.metric[:8]}
    assert harbor["Enterprise Value"] == "$275.0m"
    assert harbor["Cyber findings"] == "9"
    assert app.number_input[0].value == 275_000_000
    assert app.number_input[1].value == 22_000_000

    app.number_input[2].set_value(1000).run()
    app.slider[0].set_value(100).run()
    assert any("negative mechanical Illustrative EV" in warning.value for warning in app.warning)
