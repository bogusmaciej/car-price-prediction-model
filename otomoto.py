from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from joblib import dump
import pandas as pd
from otomoto_create_dataset import create_dataset
import os


def create_model():
    try:
        df = pd.read_csv("data/otomoto_new.csv")
    except FileNotFoundError:
        print("Dataset file does not exist!")

        if(os.path.isfile("data/otomoto_offers_eng_23-04-2023.csv")):
            create_from_file = input("Create dataset from 'otomoto_offers_eng_23-04-2023.csv' file? (y/n): ")
            if create_from_file.lower() == 'y':
                create_dataset()
                df = pd.read_csv("data/otomoto_new.csv")  
            else:
                return
            
    
    X = df.drop(["price"], axis=1)
    y = df["price"]

    categorical_features = ['seller_type','vehicle_brand',
                            'vehicle_model', 'units','fuel_type', 'color', 'automatic_air_conditioning',
                            'abs', 'no_accident','automatic_air_conditioning_is_not_set',
                            'no_accident_is_not_set','voivodship']
    numerical_features = ['production_year', 'mileage']

    categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state = 0)
    
    n_estimators = 0
    max_samples = 0
    
    print("MODEL CREATOR")
    n_estimators = input("n_estimators (e.g. 50): ")
    max_samples = input("max_samples (e.g. 5000): ")
    model = RandomForestRegressor(n_estimators=int(n_estimators), random_state=42, max_samples=int(max_samples), verbose=2, n_jobs=-1)
    
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                ('model', model)],verbose=2)

    pipeline.fit(train_X, train_y)
    score = pipeline.score(val_X, val_y)
    print(f"Model trained, score: {score}")
    if not os.path.exists('./model'):
        os.mkdir('./model')
    dump(pipeline, 'model/otomoto_price_prediction_model.joblib')