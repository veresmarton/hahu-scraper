import pandas as pd
from datetime import datetime

cols = ['adcode', 'query_name', 'make', 'model', 'link', 'price', 'fuel',
       'year', 'engine_size', 'engine_power', 'mileage',"is_diesel","year_old", 'create_date', 'update_date']

def upsert(original, df):
    not_old_mask = ~df.index.isin(original.index)
    updated = pd.concat([original, df[not_old_mask]]) # add new rows
    updated.update(df) # update old rows
    updated['create_date'].fillna(updated['update_date'], inplace=True) # set new rows create_date
    return updated

def preprocess(filepath):
    original = pd.read_csv("../data/interim/cars.csv")

    df = pd.read_csv(filepath)
    df["is_diesel"] = df["fuel"] == "Dízel"
    df["year_old"] = datetime.now().year - df["year"]
    df.rename(columns={'run_datetime':'update_date'}, inplace=True)

    df = df.set_index('adcode')

    updated = upsert(original, df)
    updated.to_csv("../data/interim/cars.csv")

    updated = pd.concat([updated, pd.get_dummies(updated.make)], axis=1)
    updated.to_csv("../data/interim/training_data.csv", index=True)
