from streamlit.testing.v1 import AppTest


def test_evaluator_page_loads_without_exception() -> None:
    at = AppTest.from_file("filename.py", default_timeout=60).run()
    assert len(at.exception) == 0


def test_evaluator_click_renders_similarity_score() -> None:
    at = AppTest.from_file("filename.py", default_timeout=60).run()
    assert len(at.exception) == 0
    at.text_input[0].set_value("abc")
    at.text_input[1].set_value("abd")
    at.button[0].click()
    at.run()
    assert len(at.exception) == 0
    assert any("Similarity score" in markdown.value for markdown in at.markdown)
