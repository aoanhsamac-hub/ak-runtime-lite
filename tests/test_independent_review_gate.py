from services.independent_review_gate import IndependentReviewGate


def test_hermes_recommendation_hungvuong_review():
    gate = IndependentReviewGate()
    result = gate.validate({"recommender": "Hermes", "reviewer": "Hung Vuong"})
    assert result["passed"]
    assert "independently validated" in result["reason"]


def test_same_recommender_reviewer_fails():
    gate = IndependentReviewGate()
    result = gate.validate({"recommender": "Sage", "reviewer": "Sage"})
    assert not result["passed"]
    assert "cannot also be the final reviewer" in result["reason"]


def test_unauthorized_recommender_fails():
    gate = IndependentReviewGate()
    result = gate.validate({"recommender": "Janus", "reviewer": "Hung Vuong"})
    assert not result["passed"]
    assert "not authorized" in result["reason"]


def test_unauthorized_reviewer_fails():
    gate = IndependentReviewGate()
    result = gate.validate({"recommender": "Hermes", "reviewer": "Janus"})
    assert not result["passed"]
    assert "not authorized" in result["reason"]


def test_sage_recommendation_allowed():
    gate = IndependentReviewGate()
    result = gate.validate({"recommender": "Sage", "reviewer": "Hung Vuong"})
    assert result["passed"]


def test_batch_validation():
    gate = IndependentReviewGate()
    recs = [
        {"recommender": "Hermes", "reviewer": "Hung Vuong"},
        {"recommender": "Hermes", "reviewer": "Hermes"},
    ]
    results = gate.validate_batch(recs)
    assert results[0]["passed"]
    assert not results[1]["passed"]
