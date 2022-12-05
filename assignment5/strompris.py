#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime

import altair as alt
import pandas as pd
import requests
import requests_cache

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()

# alt.renderers.enable('notebook')

# task 5.1:


def make_url(date: datetime.date = None, location: str = "NO1") -> str:
    """Function creates an URL string for querying the hvakosterstrommen.no API.
        URL example: https://www.hvakosterstrommen.no/api/v1/prices/[year]/[month]-[day]_[location].json

    Args:
        date (datetime.date, optional): date for which data must be collected. Defaults to None.
        location (str, optional): location for which data must be collected. Defaults to "NO1".

    Raises:
        ValueError: the `date` must be after 2nd of October 2022.

    Returns:
        str: URL string for querying the hvakosterstrommen.no API.
    """
    # check if the date's value is good
    if date < datetime.date(2022, 10, 2):
        raise ValueError("Date must be after 2nd of October 2022.")
        return None

    locations = ["NO1", "NO2", "NO3", "NO4", "NO5"]

    # check if the location's data is good
    if location not in locations:
        raise ValueError(f"Location must be one of {locations}")
        return None

    url_header = "https://www.hvakosterstrommen.no/api/v1/prices/"

    year = str(date.year)
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)

    url = url_header + f"{year}/{month}-{day}_{location}.json"

    return url


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API.

    Args:
        date (datetime.date, optional): day's date for fetching prices. If not provided, defaults to today's date.
        location (str, optional): location for fetching prices. Defaults to "NO1".

    Returns:
        pd.DataFrame: ["NOK_per_kWh", "time_start"] data from the API for given date and location.
    """

    if date is None:
        # if date is not given, fetch data for
        # the date of function call
        date = datetime.date.today()

    # make url and GET data
    url = make_url(date, location)
    response = requests.get(url)

    # create a dataframe with data from the response
    df = pd.DataFrame.from_dict(response.json())

    # keep only necessary columns
    df = df[["NOK_per_kWh", "time_start"]]

    # correcting the time column as instructed
    # in the assignment description
    df["time_start"] = pd.to_datetime(df["time_start"], utc=True).dt.tz_convert(
        "Europe/Oslo"
    )

    return df


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen",
}

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations=list(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame.

    Args:
        end_date (datetime.date, optional): last date for data to be collected.
            Defaults to None.
        days (int, optional): number of days until `end_date`. Defaults to 7.
        locations (list, optional): locations for data collection.
            Defaults to list(LOCATION_CODES.keys()).

    Returns:
        pd.DataFrame: table with data collected for given dates and locations.
    """
    if end_date is None:
        end_date = datetime.date.today()

    # list of dates from (end_date-days) until end_date
    # this sequence order make it convenient to compute df.diff() in future
    dates = [end_date - datetime.timedelta(days=x) for x in range(days-1, -1, -1)]

    # final dataframe for output
    df = pd.DataFrame()

    for location in locations:
        for date in dates:
            temp_df = fetch_day_prices(date, location)
            temp_df["location_code"] = location
            temp_df["location"] = LOCATION_CODES[location]

            df = pd.concat([df, temp_df], ignore_index=True)

    return df


# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plots energy prices obtained from hvakosterstrommen.no API over time.
        * x-axis = time_start
        * y-axis = price in NOK
        * location gets its own line

    Args:
        df (pd.DataFrame): data with prices over time

    Returns:
        alt.Chart: altair chart
    """

    # the price difference from the previous hour (2 points)
    df["price_diff_1hour"] = df.groupby("location")["NOK_per_kWh"].diff()

    # the difference from the same hour on the previous day (2 points)
    df["price_diff_1day"] = df.groupby("location")["NOK_per_kWh"].diff(24)

    # the difference from the same hour on the same day of the previous week (1 points).
    df["price_diff_1week"] = df.groupby("location")["NOK_per_kWh"].diff(24 * 7)

    # altair chart with requirements on x- and y-axis and location
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x="time_start",
            y="NOK_per_kWh",
            color="location",
            tooltip=[
                "location",
                "NOK_per_kWh",
                "price_diff_1hour",
                "price_diff_1day",
                "price_diff_1week",
            ],
        )
        .interactive()
    )

    return chart


# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    ...


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
