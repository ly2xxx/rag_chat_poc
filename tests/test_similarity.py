import pytest

from modules.similarity import SimilarityScorer

@pytest.fixture(scope="module")
def scorer() -> SimilarityScorer:
    return SimilarityScorer()

def test_identical_sentences_score_above_0_99(scorer: SimilarityScorer) -> None:
    sentence = "The quick brown fox jumps over the lazy dog."
    assert scorer.score(sentence, sentence) > 0.99

def test_cat_variant_scores_higher_than_stock_prices(scorer: SimilarityScorer) -> None:
    cat_score = scorer.score("a cat sits on the mat", "a cat is sitting on a mat")
    stock_score = scorer.score("a cat sits on the mat", "stock prices fell today")
    assert cat_score > stock_score
