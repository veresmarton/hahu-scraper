import pandas as pd
from datetime import datetime

cols = ['adcode', 'query_name', 'make', 'model', 'link', 'price', 'fuel',
       'year', 'engine_size', 'engine_power', 'mileage',"is_diesel","year_old", 'create_date', 'update_date']

join_cols = ['adcode', 'query_name', 'make', 'model', 'link', 'price', 'fuel',
       'year', 'engine_size', 'engine_power', 'mileage',"is_diesel","year_old"]

def preprocess(filepath):
    original = pd.read_csv("../data/interim/cars.csv")

    df = pd.read_csv(filepath)
    df["is_diesel"] = df["fuel"] == "Dízel"
    df["year_old"] = datetime.now().year - df["year"]
    
    new_mask = df.adcode not in original.adcode
    new = df[new_mask]
    new.rename(columns={'run_datetime':'create_date'}, inplace=True)
    new['update_date'] = new['create_date']

    old = df[~new_mask]
    old = old.join(original, how='inner', on=join_cols)
    old.drop('update_date', axis=1, inplace=True)
    old.rename(columns={'run_datetime':'update_date'}, inplace=True)

    df = pd.concat([original[original.adcode not in new.adcode and original.adcode not in old.adcode],
                    old,
                    new])

    df.to_csv("../data/interim/training_data.csv", index=False)


def similar_avg(row, df):
    l = df.query(
        "make==@row.make and model==@row.model and year<=(@row.year+1) and year>=(@row.year-1) and mileage<=(@row.mileage+20000) and mileage>=(@row.mileage-20000) and fuel==@row.fuel and engine_power==@row.engine_power"
    )
    return l.price.mean()
