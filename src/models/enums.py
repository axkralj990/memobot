"""Enum types for daily log tracking."""

from enum import StrEnum


class Productivity(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AnxietyStatus(StrEnum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"


class PhysicalStatus(StrEnum):
    OK = "ok"
    GOOD = "good"
    BAD = "bad"
    NOT_SO_GOOD = "not so good"


class Temperature(StrEnum):
    SCORCHING = "scorching"
    HOT = "hot"
    WARM = "warm"
    PERFECT = "perfect"
    NORMAL = "normal"
    COLD = "cold"
    FREEZING = "freezing"


class Weather(StrEnum):
    SUNNY = "sunny"
    HORRIBLE = "horrible"
    RAINY = "rainy"
    POURING = "pouring"
    DARK = "dark"
    STORMS = "storms"
    WINDY = "windy"
    SCATTERED = "scattered"
    CLEAR = "clear"
    HUMID = "humid"
    SNOWING = "snowing"
    MIXED = "mixed"
    CLOUDY = "cloudy"
    THUNDERSTORMS = "thunderstorms"
    FOG = "fog"


class Supplement(StrEnum):
    PROTEINS = "proteins"
    CREATINE = "creatine"
    COLLAGEN = "collagen"
    OMEGA3 = "omega3"
    VIT_MIN = "vit+min"
    BCAA = "bcaa"
    ZINC = "zinc"
    MG_THEANINE = "Mg+Theanine"
    ASHWAGANDHA = "ashwagandha"
