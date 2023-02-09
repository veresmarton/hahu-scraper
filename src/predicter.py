import pickle
import pandas as pd

def predict(filepath="../data/interim/training_data.csv"):
    df = pd.read_csv(filepath)
    X = df[
        [
            "engine_size",
            "engine_power",
            "mileage",
            "ford",
            "hyundai",
            "kia",
            "skoda",
            "volkswagen",
            "is_diesel",
            "year_old",
        ]
    ]
    y = df.price
    loaded_model = pickle.load(open("../data/processed/model.pkl", 'rb'))
    prediction = loaded_model.predict(X)
    prediction = pd.Series(prediction, name="prediction")
    result = pd.concat([df, y, prediction], axis=1)
    result.to_csv("../data/processed/predicted_price.csv", index=False)
