import pandas as pd


def make_data():

    data = pd.read_csv(
        "data/compas-scores-two-years.csv",
        usecols=[
            "age",
            "c_charge_degree",
            "race",
            "age_cat",
            "score_text",
            "sex",
            "priors_count",
            "days_b_screening_arrest",
            "decile_score",
            "is_recid",
            "two_year_recid",
            "c_jail_in",
            "c_jail_out",
        ],
    )

    return data[
        (data["days_b_screening_arrest"] <= 30)
        & (data["days_b_screening_arrest"] >= -30)
        & (data["is_recid"] is not 1)
        & (data["c_charge_degree"] is not "O")
        & (data["score_text"] is not "N/A")
    ]
