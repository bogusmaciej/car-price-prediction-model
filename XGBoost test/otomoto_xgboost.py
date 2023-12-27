import os
import pandas as pd
from joblib import dump

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from xgboost import XGBRegressor

from otomoto_create_dataset import create_dataset



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
    numeric_features = ['production_year', 'mileage']

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean'))
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Kompozycja transformerów
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)

    model =  XGBRegressor(
        n_estimators=95,
        max_depth=12,
        learning_rate=0.4
    )

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])

    pipeline.fit(X_train, y_train)

    predictions  = pipeline.predict(X_test)
    print("Model created, score:", r2_score(predictions, y_test))
        
    if not os.path.exists('./model'):
        os.mkdir('./model')
    dump(pipeline, 'model/otomoto_price_prediction_model.joblib')

create_model()