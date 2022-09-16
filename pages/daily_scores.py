import streamlit as st
import numerapi

from modules.preprocess import (
    read_config, get_models, download_daily_results,
    set_rounds_for_plot, extract_dates_for_plot
)
from modules.visualization import Plot


def select_col_to_visualize(config):
    visualize_col = st.radio(
        "column to visualize", config["metrics"]
    )
    return visualize_col


def main():
    config = read_config("config.yaml")

    st.title('Numerai Round Scores')

    napi = numerapi.NumerAPI()
    models = get_models(napi)

    default_model_idx = models.index(config["base_model"])
    model_name = st.selectbox(
        'model name', models, index=default_model_idx
    )
    df = download_daily_results(napi, model_name)

    start_round, end_round = set_rounds_for_plot(df["roundNumber"])
    df_rounds = df.loc[df["roundNumber"].between(start_round, end_round)]

    df_latest = extract_dates_for_plot(df_rounds)

    visualize_col = select_col_to_visualize(config)

    plot = Plot(df_latest)
    plot.single_metric(visualize_col)
    plot.multiple_metric_percentiles(config["metrics"])


if __name__ == '__main__':
    main()
