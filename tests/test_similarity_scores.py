import pytest

from modules.similarity import SimilarityScorer


@pytest.fixture(scope="module")
def scorer() -> SimilarityScorer:
    return SimilarityScorer()


def test_identical_sentences_score_one(scorer: SimilarityScorer) -> None:
    sentence = "The quick brown fox jumps over the lazy dog."
    assert round(scorer.score(sentence, sentence), 3) == 1.0


def test_cat_paraphrase_scores_0_984(scorer: SimilarityScorer) -> None:
    score = scorer.score("a cat sits on the mat", "a cat is sitting on a mat")
    assert round(score, 3) == 0.984


def test_cat_vs_stock_prices_scores_0_079(scorer: SimilarityScorer) -> None:
    score = scorer.score("a cat sits on the mat", "stock prices fell today")
    assert round(score, 3) == 0.079
