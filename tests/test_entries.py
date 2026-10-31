from datetime import date

from src.models import DailyEntryInput


ZERO_DEFAULT_FIELDS = ("mindful_min", "alcohol_unt", "fasting")


def test_zero_default_fields_when_omitted():
    entry = DailyEntryInput(entry_date=date(2026, 10, 31))

    for field in ZERO_DEFAULT_FIELDS:
        assert getattr(entry, field) == 0


def test_zero_default_fields_accept_explicit_null():
    entry = DailyEntryInput.model_validate(
        {
            "entry_date": "2026-10-31",
            **{field: None for field in ZERO_DEFAULT_FIELDS},
        }
    )

    for field in ZERO_DEFAULT_FIELDS:
        assert getattr(entry, field) == 0
        assert field not in entry.model_fields_set


def test_zero_default_fields_preserve_provided_values():
    entry = DailyEntryInput(
        entry_date=date(2026, 10, 31),
        mindful_min=10,
        alcohol_unt=1.5,
        fasting=16,
    )

    assert entry.mindful_min == 10
    assert entry.alcohol_unt == 1.5
    assert entry.fasting == 16


def test_cold_exposure_is_a_boolean_defaulting_to_false():
    omitted = DailyEntryInput(entry_date=date(2026, 10, 31))
    explicit_null = DailyEntryInput.model_validate(
        {"entry_date": "2026-10-31", "cold_exposure": None}
    )
    exposed = DailyEntryInput(
        entry_date=date(2026, 10, 31),
        cold_exposure=True,
    )

    assert omitted.cold_exposure is False
    assert explicit_null.cold_exposure is False
    assert "cold_exposure" not in explicit_null.model_fields_set
    assert exposed.cold_exposure is True
