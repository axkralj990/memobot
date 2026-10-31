from datetime import date

from src.models import DailyEntryInput


ZERO_DEFAULT_FIELDS = ("mindful_min", "alcohol_unt", "fasting", "cold_min")


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


def test_zero_default_fields_preserve_provided_values():
    entry = DailyEntryInput(
        entry_date=date(2026, 10, 31),
        mindful_min=10,
        alcohol_unt=1.5,
        fasting=16,
        cold_min=2,
    )

    assert entry.mindful_min == 10
    assert entry.alcohol_unt == 1.5
    assert entry.fasting == 16
    assert entry.cold_min == 2
