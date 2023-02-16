import pandas as pd
from datetime import datetime


def preprocess(filepath):
    df = pd.read_csv(filepath)
    df.drop_duplicates(subset=["link"], inplace=True)
    df = pd.concat([df, pd.get_dummies(df.make)], axis=1)
    df["is_diesel"] = df["fuel"] == "Dízel"
    df["year_old"] = datetime.now().year - df["year"]
    # add avg
    # df["avg_price"] = df.apply(lambda x: similar_avg(x, df), axis=1)
    df.to_csv("../data/interim/training_data.csv", index=False)


def similar_avg(row, df):
    l = df.query(
        "make==@row.make and model==@row.model and year<=(@row.year+1) and year>=(@row.year-1) and mileage<=(@row.mileage+20000) and mileage>=(@row.mileage-20000) and fuel==@row.fuel and engine_power==@row.engine_power"
    )
    return l.price.mean()
