import streamlit as st
import plotly.graph_objs as go

from plotly.subplots import make_subplots


class Plot:
    def __init__(self, df) -> None:
        self.df = df

    def single_metric(self, visualize_col):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(
                x=self.df["roundNumber"],
                y=self.df[visualize_col].round(4),
                name="value",
                yaxis="y1"
            ),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(
                x=self.df["roundNumber"],
                y=self.df[f"{visualize_col}Percentile"].round(2),
                name="percentile",
                yaxis="y2"
            ),
            secondary_y=True
        )
        fig.update_layout(
            title=f"{visualize_col}",
            xaxis_title='round',
            yaxis1_title='value',
            yaxis2_title='percentile',
            showlegend=True
        )
        st.plotly_chart(go.Figure(fig))

    def multiple_metric_percentiles(self, metrics):
        fig = make_subplots()
        for metric in metrics:
            fig.add_trace(
                go.Scatter(
                    x=self.df["roundNumber"],
                    y=self.df[f"{metric}Percentile"].round(4),
                    name=f"{metric} percentile"),
                secondary_y=False
            )
        fig.update_layout(
            title="percentiles",
            xaxis_title='round',
            yaxis_title='percentile',
            showlegend=True
        )
        st.plotly_chart(go.Figure(fig))

    def compare_models(self, model_names):
        fig = make_subplots()
        for model_name in model_names:
            fig.add_trace(
                go.Scatter(
                    x=self.df["roundNumber"],
                    y=self.df[model_name],
                    name=model_name,
                    yaxis="y1"
                ),
                secondary_y=False
            )
        fig.update_layout(
            title="model comparison",
            xaxis_title='round',
            yaxis1_title='value',
            showlegend=True
        )
        st.plotly_chart(go.Figure(fig))

    def compare_cum_val(self, model_names):
        fig = make_subplots()
        for model_name in model_names:
            fig.add_trace(
                go.Scatter(
                    x=self.df["roundNumber"],
                    y=self.df[model_name].cumsum(),
                    name=model_name,
                    yaxis="y1"
                ),
                secondary_y=False
            )
        fig.update_layout(
            title="cumulative sum comparison",
            xaxis_title='round',
            yaxis1_title='value',
            showlegend=True
        )
        st.plotly_chart(go.Figure(fig))
