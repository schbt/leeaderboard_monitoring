from logging import getLogger

import pandas as pd
import streamlit as st
import numerapi

from modules.preprocess import (
    read_config, get_models, download_daily_results,
    set_rounds_for_plot, extract_dates_for_plot
)
from modules.visualization import Plot


def select_col_for_comparison(eval_vals):
    visualize_col = st.radio(
        "column to visualize", eval_vals
    )
    return visualize_col


def main():
    config = read_config("config.yaml")
    logger = getLogger(__name__)

    st.title('Numerai Round Scores')

    napi = numerapi.NumerAPI()
    models = get_models(napi, logger)

    model_names = st.multiselect(
        'model name', models, default=[config["base_model"]]
    )

    compare_col = select_col_for_comparison(config["eval_vals"])

    df_list = []
    for model_name in model_names:
        df = download_daily_results(napi, logger, model_name)

        df_latest = extract_dates_for_plot(df)
        df_latest = df_latest[["roundNumber", compare_col]]
        df_latest = df_latest.rename({compare_col: model_name}, axis=1)
        df_list.append(df_latest)

    min_round = min([df["roundNumber"].min() for df in df_list])
    max_round = max([df["roundNumber"].max() for df in df_list])
    df_rounds = pd.Series([i for i in range(min_round, max_round + 1)])
    df_rounds.name = "roundNumber"

    for df in df_list:
        df_rounds = pd.merge(df_rounds, df, on="roundNumber", how="left")

    start_round, end_round = set_rounds_for_plot(df_rounds["roundNumber"])
    df_rounds = df_rounds.loc[
        df_rounds["roundNumber"].between(start_round, end_round)
    ]

    plot = Plot(df_rounds)
    plot.compare_models(model_names)
    plot.compare_cum_val(model_names)

    st.dataframe(df_rounds[model_names].corr())


if __name__ == "__main__":
    main()
