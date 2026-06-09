"""Test Zone Validation Engine."""

from services.iris.zone_validation_engine import MarketForecast, ZoneValidationEngine


def test_validate_zone_touched():
    forecast = MarketForecast("test-val-1", "XAUUSDm", "M5")
    forecast.zone_low = 1900.0
    forecast.zone_high = 1950.0
    engine = ZoneValidationEngine()
    validation = engine.validate_forecast(forecast, [1920.0])
    assert validation["zone_touched"] is True


def test_validate_zone_miss():
    forecast = MarketForecast("test-val-2", "XAUUSDm", "M5")
    forecast.zone_low = 2000.0
    forecast.zone_high = 2100.0
    engine = ZoneValidationEngine()
    validation = engine.validate_forecast(forecast, [1900.0])
    assert validation["zone_touched"] is False


def test_validation_has_required_fields():
    forecast = MarketForecast("test-val-3", "EURUSDm", "M15")
    forecast.zone_low = 1.0
    forecast.zone_high = 1.1
    engine = ZoneValidationEngine()
    validation = engine.validate_forecast(forecast, [])
    required = ["zone_touched", "false_zone", "max_favorable_excursion", "max_adverse_excursion", "final_score"]
    for field in required:
        assert field in validation
