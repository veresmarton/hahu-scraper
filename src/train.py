import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
from datetime import datetime
from matplotlib import pyplot as plt
import pickle



def train(filepath="../data/interim/training_data.csv"):
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
            "price"
        ]
    ]
    X = X.dropna(how='any')
    y = X.price
    X = X.drop("price", axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=111)

    predictions = {}
    ## Define Grid 
    grid = { 
        'n_estimators': [10,50,100],
        'max_features': [1.0, 'sqrt','log2'],
        'max_depth' : [2,4,6],
        'random_state' : [111]
    }
    print(datetime.now())
    CV_rfr = GridSearchCV(estimator=RandomForestRegressor(), param_grid=grid, cv=3)
    CV_rfr.fit(X_train, y_train)
    print(datetime.now())

    best_regr = CV_rfr.best_estimator_
    prediction = best_regr.predict(X_test)
    mse = mean_squared_error(y_test, prediction)
    rmse = mse**.5
    print(f"RF - MSE: {mse}, RMSE: {rmse}")

    predictions["RF"] = [best_regr, rmse]

    ## Define Grid 
    grid = { 
        'n_neighbors': [3,5,7,11, 13],
        'weights': ['uniform', 'distance'],
        'leaf_size' : [10,20,30,50],
        'metric' : ['cosine', 'l1', 'l2', 'minkowski'],
        'p' : [1,2,4,6]
    }
    print(datetime.now())
    CV_rfr = GridSearchCV(estimator=KNeighborsRegressor(), param_grid=grid, cv=3)
    CV_rfr.fit(X_train, y_train)
    print(datetime.now())

    best_knn = CV_rfr.best_estimator_
    prediction = best_knn.predict(X_test)
    mse = mean_squared_error(y_test, prediction)
    rmse = mse**.5
    print(f"KNN - MSE: {mse}, RMSE: {rmse}")

    predictions["KNN"] = [best_knn, rmse]
    model = sorted(predictions.values(), key = lambda x: x[1])[0][0]

    pickle.dump(model, open("../data/processed/model.pkl", 'wb'))





