import datetime

import yaml
import pandas as pd
import numpy as np
import streamlit as st


def read_config(config_path):
    with open(config_path) as file:
        config = yaml.safe_load(file)

    return config


@st.cache
def get_models(napi, logger):
    query = "query {v2Leaderboard {username}}"
    models = napi.raw_query(query)
    logger.info('downloaded model names from numerai leaderboard')

    models = [list(m.values())[0] for m in models["data"]["v2Leaderboard"]]
    return sorted(models)


@st.cache
def download_daily_results(napi, logger, model_name):
    df = pd.DataFrame(napi.daily_submissions_performances(model_name))
    logger.info(f'downloaded daily submmision perfomrances ({model_name})')

    df = df.sort_values(["roundNumber", "date"])
    df = df.rename({"correlation": "corr"}, axis=1)
    return df


def set_rounds_for_plot(round_number):
    min_round = int(round_number.min())
    max_round = int(round_number.max())
    if min_round == max_round:
        raise ValueError("not enough period to plot")

    start_round = st.slider(
        'start round',
        min_value=min_round,
        max_value=max_round,
        value=max([min_round, max_round - 20]),
        step=1,
    )
    end_round = st.slider(
        'end round',
        min_value=min_round,
        max_value=max_round,
        value=max_round,
        step=1,
    )

    return start_round, end_round


def extract_dates_for_plot(_df):
    df = _df.copy()
    start_dates = df.groupby(["roundNumber"])["date"].min()
    latest_dates = start_dates + datetime.timedelta(days=27)
    latest_dates = latest_dates.reset_index()

    df["date"] = df["date"].dt.date
    latest_dates["date"] = latest_dates["date"].dt.date

    latest_dates["date"] = np.where(
        latest_dates["date"] > df["date"].max(), df["date"].max(), latest_dates["date"]
    )

    df_latest = df.merge(latest_dates, on=["roundNumber", "date"], how="inner")
    df_latest["date"] = df_latest["date"].astype(str)

    return df_latest
