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


def fraction_of_bad_years(years_list: list) -> float:
    return sum([nissans_shift(y) > 15 for y in years_list]) / len(years_list)


def hisfory_of_bad_years(
    init_year: int, years_back: int, intervals: int
) -> list:
    return [
        (c, fraction_of_bad_years(list(range(c, c + intervals))))
        for c in range(init_year - years_back, init_year + 1, intervals)
    ]


def main():
    # nissans_shits = nissans_history(2500, 800)
    #
    # plt.scatter(*zip(*nissans_shits))
    # plt.axhline(y=15, color="red", linestyle="--")
    # # plt.axhline(y=-15, color="red", linestyle="--")
    # plt.title("Days between the equinox and Alef Nissan")
    # plt.show()

    interval = 100
    bad_years_fracs = hisfory_of_bad_years(2500, 800, interval)
    plt.plot(*zip(*bad_years_fracs))
    plt.title(
        f"Fraction of years in which Passover wasn't in the spring month\nof every {interval} years invterval"
    )
    plt.show()


if __name__ == "__main__":
    main()
