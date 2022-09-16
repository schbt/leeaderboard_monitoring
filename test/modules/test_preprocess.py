import datetime
from logging import getLogger

import numerapi
import pandas as pd
import pandera as pa

from modules.preprocess import download_daily_results, extract_dates_for_plot


def test_download_daily_results():
    napi = numerapi.NumerAPI()
    logger = getLogger(__name__)
    model_name = "integration_test_7"
    output = download_daily_results(napi, logger, model_name)

    schema = pa.DataFrameSchema(
        {
            "roundNumber": pa.Column(int),
            "date": pa.Column(pd.DatetimeTZDtype(tz="UTC")),
            "corr": pa.Column(float, nullable=True),
            "corrPercentile": pa.Column(float, checks=[pa.Check.le(1), pa.Check.ge(0)], nullable=True),
            "fnc": pa.Column(float, nullable=True),
            "fncPercentile": pa.Column(float, checks=[pa.Check.le(1), pa.Check.ge(0)], nullable=True),
            "mmc": pa.Column(float, nullable=True),
            "mmcPercentile": pa.Column(float, checks=[pa.Check.le(1), pa.Check.ge(0)], nullable=True),
            "tc": pa.Column(float, nullable=True),
            "tcPercentile": pa.Column(float, checks=[pa.Check.le(1), pa.Check.ge(0)], nullable=True),
            "correlationWithMetamodel": pa.Column(float, checks=[pa.Check.le(1), pa.Check.ge(0)], nullable=True),
        }, strict=True
    )

    validated_df = schema(output)

    assert output.equals(validated_df)


def test_extract_dates_for_plot():
    dates = (
        [datetime.datetime(2022, 5, 1) + datetime.timedelta(days=i) for i in range(1, 29)] +
        [datetime.datetime(2022, 5, 2) + datetime.timedelta(days=i) for i in range(1, 29)] +
        [datetime.datetime(2022, 5, 3) + datetime.timedelta(days=i) for i in range(1, 28)] +
        [datetime.datetime(2022, 5, 4) + datetime.timedelta(days=i) for i in range(1, 27)]
    )
    round_numbers = (
        [301 for _ in range(28)] +
        [302 for _ in range(28)] +
        [303 for _ in range(27)] +
        [304 for _ in range(26)]
    )
    input = pd.DataFrame({
        "date": dates,
        "roundNumber": round_numbers
    })
    output = extract_dates_for_plot(input)

    expectation = pd.DataFrame({
        "date": [datetime.datetime(2022, 5, 28) + datetime.timedelta(days=i) for i in [1, 2, 2, 2]],
        "roundNumber": [301, 302, 303, 304]
    })
    expectation["date"] = expectation["date"].dt.strftime("%Y-%m-%d")
    assert output.equals(expectation)
