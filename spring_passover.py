import datetime
from convertdate import hebrew
from ephem import next_spring_equinox
import matplotlib.pyplot as plt


def hebrew_equinox(year: str) -> tuple:
    greg_equinox = next_spring_equinox(year).datetime()
    hebrew_equinox = hebrew.from_gregorian(
        greg_equinox.year, greg_equinox.month, greg_equinox.day
    )

    return hebrew_equinox


def distance_from_years_end(date: tuple) -> int:
    """
    Calculates the distance from the end of the hebrew year to the given hebrew date.
    The input is given as (year, month, day).
    """
    gregorian_date = datetime.date(*hebrew.to_gregorian(*date))
    alef_nissan_gregorianed = datetime.date(
        *hebrew.to_gregorian(date[0], 1, 1)
    )

    distance = alef_nissan_gregorianed - gregorian_date
    return distance.days


def nissans_shift(year: int) -> int:
    return distance_from_years_end(hebrew_equinox(str(year)))


def nissans_history(init_year: int, years_back: int) -> list:
    return [
        (y, nissans_shift(y))
        for y in range(init_year - years_back, init_year + 1)
    ]


def main():
    nissans_shits = nissans_history(2024, 300)
    plt.scatter(*zip(*nissans_shits))
    plt.axhline(y=15, color="red", linestyle="--")
    # plt.axhline(y=-15, color="red", linestyle="--")
    plt.title("Days between the equinox and Alef Nissan")
    plt.show()


if __name__ == "__main__":
    main()
