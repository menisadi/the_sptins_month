import datetime
from datetime import timedelta
from convertdate import hebrew
from ephem import next_spring_equinox
import matplotlib.pyplot as plt


def hebrew_equinox(year: str) -> tuple:
    """
    Calculate the Hebrew date for the spring equinox of a given Gregorian year.

    Args:
    year (str): The Gregorian year to compute the equinox for.

    Returns:
    tuple: Hebrew date of the equinox in (year, month, day) format.
    """
    gregorian_equinox = next_spring_equinox(year).datetime()
    if int(year) <= 1582:
        gregorian_equinox = gregorian_equinox + timedelta(days=13)
    hebrew_equinox = hebrew.from_gregorian(
        gregorian_equinox.year, gregorian_equinox.month, gregorian_equinox.day
    )

    return hebrew_equinox


def distance_from_years_end(date: tuple) -> int:
    """
    Calculates the distance from the end of the Hebrew year to the given Hebrew date.

    Args:
    date (tuple): The Hebrew date in (year, month, day) format.

    Returns:
    int: Number of days from the given Hebrew date to the end of its year.
    """
    gregorian_date = datetime.date(*hebrew.to_gregorian(*date))
    alef_nissan_gregorianed = datetime.date(
        *hebrew.to_gregorian(date[0], 1, 1)
    )

    distance = alef_nissan_gregorianed - gregorian_date

    return distance.days


def nissans_shift(year: int) -> int:
    """
    Computes the day shift for Alef Nissan from the equinox.

    Args:
    year (int): Gregorian year.

    Returns:
    int: Number of days between the equinox and Alef Nissan.
    """
    return distance_from_years_end(hebrew_equinox(str(year)))


def nissans_history(init_year: int, years_back: int) -> list:
    """
    Generates a history of Nissan shifts for a range of years.

    Args:
    init_year (int): Initial year of the history.
    years_back (int): How many years back the history should go.

    Returns:
    list: List of tuples with year and Nissan shift.
    """
    return [
        (y, nissans_shift(y))
        for y in range(init_year - years_back, init_year + 1)
    ]


def fraction_of_bad_years(years_list: list) -> float:
    """
    Calculates the fraction of years where Passover was too early or too late.

    Args:
    years_list (list): List of years to evaluate.

    Returns:
    float: Fraction of 'bad' years.
    """
    return sum(
        [nissans_shift(y) < -15 or nissans_shift(y) > 15 for y in years_list]
    ) / len(years_list)


def history_of_bad_years(
    init_year: int, years_back: int, intervals: int
) -> list:
    """
    Analyze periods over given intervals to find fraction of bad Passover timings.

    Args:
    init_year (int): Start year for the analysis.
    years_back (int): How many years back to start from.
    intervals (int): Interval size to analyze the data in chunks.

    Returns:
    list: List of tuples with starting year of the interval and fraction of bad years.
    """
    return [
        (c, fraction_of_bad_years(list(range(c, c + intervals))))
        for c in range(init_year - years_back, init_year + 1, intervals)
    ]


def plot_nissan_shifts(nissans_shits):
    """
    Plots Nissan shifts over the years.
    """
    plt.scatter(*zip(*nissans_shits))
    plt.axhline(y=15, color="red", linestyle="--")
    plt.axhline(y=-15, color="red", linestyle="--")
    plt.title("Days between the equinox and Alef Nissan")
    plt.show()


def plot_bad_years_history(bad_years_fracs, interval):
    """
    Plots the fraction of bad years over intervals.
    """
    plt.plot(*zip(*bad_years_fracs))
    plt.title(
        f"Fraction of years in which Passover wasn't in the spring month\nof every {interval} years interval"
    )
    plt.show()


def main():
    nissans_shits = nissans_history(2024, 2000)
    plot_nissan_shifts(nissans_shits)

    # interval = 100
    # bad_years_fracs = history_of_bad_years(2500, 2000, interval)
    # plot_bad_years_history(bad_years_fracs, interval)


if __name__ == "__main__":
    main()
