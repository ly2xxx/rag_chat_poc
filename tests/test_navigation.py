from pathlib import Path
from streamlit.testing.v1 import AppTest

EXPECTED_LINKS = [
    "Home",
    "Keywords-Research",
    "Robby-Chat-file",
    "Robby-Chat-web",
    "Robby-Summary-youtube",
    "Text-Similarity-score(beta)",
]

def test_home_menu_has_visible_page_links() -> None:
    at = AppTest.from_file("streamlit_app.py", default_timeout=60).run()
    assert len(at.exception) == 0
    assert [title.value for title in at.title] == ["🏠 Home"]
    assert [link.proto.label for link in at.sidebar.get("page_link")] == EXPECTED_LINKS

def test_text_similarity_page_switches_without_exception() -> None:
    at = AppTest.from_file("streamlit_app.py", default_timeout=60).run()
    at.switch_page("pages/4_Text-Similarity-beta.py").run()
    assert len(at.exception) == 0

def test_no_st_pages_imports_outside_playground() -> None:
    needle = "st_" + "pages"
    offenders = [
        str(path)
        for path in Path(".").rglob("*.py")
        if "playground" not in path.parts
        and ".venv" not in path.parts
        and path.resolve() != Path(__file__).resolve()
        and needle in path.read_text(encoding="utf-8", errors="ignore")
    ]
    assert offenders == []
