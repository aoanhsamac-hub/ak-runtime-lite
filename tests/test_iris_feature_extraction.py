"""Test Iris Feature Extraction."""

import pytest


def test_import_feature_engine():
    import services.iris_feature_extraction_engine as ffe
    assert hasattr(ffe, "extract_features")


def test_extract_features_empty():
    from services.iris_feature_extraction_engine import extract_features
    result = extract_features([], "XAUUSDm")
    assert "trend" in result


def test_extract_features_bullish():
    from services.iris_feature_extraction_engine import extract_features
    ohlcv = [
        {"open": 100, "high": 105, "low": 99, "close": 100},
        {"open": 100, "high": 108, "low": 99, "close": 109},
    ]
    result = extract_features(ohlcv, "XAUUSDm")
    assert result["trend"] == "bullish"


def test_extract_features_bearish():
    from services.iris_feature_extraction_engine import extract_features
    ohlcv = [
        {"open": 100, "high": 101, "low": 99, "close": 100},
        {"open": 100, "high": 101, "low": 85, "close": 88},
    ]
    result = extract_features(ohlcv, "XAUUSDm")
    assert result["trend"] == "bearish"


def test_volatility_calculation():
    from services.iris_feature_extraction_engine import extract_features
    ohlcv = [{"open": 100, "high": 110, "low": 90, "close": 105}]
    result = extract_features(ohlcv, "XAUUSDm")
    assert "volatility" in result


def test_momentum_calculation():
    from services.iris_feature_extraction_engine import extract_features
    ohlcv = [{"open": 100, "high": 102, "low": 99, "close": 103}]
    result = extract_features(ohlcv, "XAUUSDm")
    assert "momentum" in result


def test_range_calculation():
    from services.iris_feature_extraction_engine import extract_features
    ohlcv = [{"open": 100, "high": 110, "low": 90, "close": 105}]
    result = extract_features(ohlcv, "XAUUSDm")
    assert "range" in result


def test_feature_registry_updated():
    from services.iris_feature_extraction_engine import extract_features, get_features
    extract_features([{"open": 100, "high": 102, "low": 99, "close": 101}], "XAUUSDm")
    features = get_features()
    assert len(features) >= 1


def test_feature_id_format():
    from services.iris_feature_extraction_engine import extract_features
    result = extract_features([{"open": 100, "high": 102, "low": 99, "close": 101}], "XAUUSDm")
    assert "FEAT-" in result.get("feature_id", "")