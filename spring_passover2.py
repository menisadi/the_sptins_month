import datetime
from convertdate import hebrew, julianday
from ephem import next_spring_equinox
import matplotlib.pyplot as plt


def hebrew_equinox(year: str) -> float:
    """
    Calculates the Julian Day of the next spring equinox in a given Hebrew year.
    """
    gregorian_equinox = next_spring_equinox(year).datetime()
    hebrew_date = hebrew.from_gregorian(
        gregorian_equinox.year, gregorian_equinox.month, gregorian_equinox.day
    )
    return julianday.from_gregorian(*hebrew.to_gregorian(*hebrew_date))


def distance_from_years_end2(year: int) -> int:
    gregorian_equinox = next_spring_equinox(str(year))
    dt_equinox = datetime.datetime(*gregorian_equinox.tuple()[:5])
    jd_equinox = julianday.from_datetime(dt_equinox)
    hebrew_year_jd = hebrew.from_jd(jd_equinox)[0]
    alef_nissan_julian_day = hebrew.to_jd(hebrew_year_jd, 1, 1)

    distance = alef_nissan_julian_day - jd_equinox
    return distance


def distance_from_years_end(date: tuple) -> int:
    hebrew_julian_day = julianday.from_gregorian(*hebrew.to_gregorian(*date))
    alef_nissan_julian_day = julianday.from_gregorian(date[0], 1, 1)

    distance = alef_nissan_julian_day - hebrew_julian_day
    return int(distance)


# def nissans_shift(year: int) -> int:
#     return distance_from_years_end(hebrew_equinox(str(year)))


def nissans_history(init_year: int, years_back: int) -> list:
    return [
        (y, distance_from_years_end2(y))
        for y in range(init_year - years_back, init_year + 1)
    ]


def fraction_of_bad_years(years_list: list) -> float:
    return sum([distance_from_years_end2(y) > 15 for y in years_list]) / len(
        years_list
    )


def hisfory_of_bad_years(
    init_year: int, years_back: int, intervals: int
) -> list:
    return [
        (c, fraction_of_bad_years(list(range(c, c + intervals))))
        for c in range(init_year - years_back, init_year + 1, intervals)
    ]


def main():
    nissans_shits = nissans_history(2024, 2000)
    max_year, max_gap = max(nissans_shits, key=lambda x: x[1])
    print(hebrew_equinox(str(max_year)))
    print(distance_from_years_end2(max_year))
    print(max_year)
    print(max_gap)

    # print([hebrew_equinox(str(i)) for i in range(1565, 1585)])
    # print([julianday.from_gregorian(i, 1, 1) for i in range(5325, 5345)])

    # plt.scatter(*zip(*nissans_shits))
    # plt.axhline(y=15, color="red", linestyle="--")
    # # plt.axhline(y=-15, color="red", linestyle="--")
    # plt.title("Days between the equinox and Alef Nissan")
    # plt.show()

    # interval = 100
    # bad_years_fracs = hisfory_of_bad_years(2500, 800, interval)
    # plt.plot(*zip(*bad_years_fracs))
    # plt.title(
    #     f"Fraction of years in which Passover wasn't in the spring month\nof every {interval} years invterval"
    # )
    # plt.show()


if __name__ == "__main__":
    main()
