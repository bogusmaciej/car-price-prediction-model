import pandas as pd
from otomoto import create_model
from joblib import load

new_data = pd.DataFrame({
    'seller_type' : ["Private person"],
    'vehicle_brand' : ["Mini"],
    'vehicle_model' : ["Cooper S"],
    'units' : ["km"],
    'fuel_type' : ["Gasoline"],
    'color' : ["Gray"],
    'automatic_air_conditioning' : [True],
    'abs' : [True],
    'no_accident' : [True],
    'voivodship' : ["Warmińsko-mazurskie"],
    'production_year' : [2016],
    'mileage' : [130000],
    "mileage_is_not_set" : [False],
    "automatic_air_conditioning_is_not_set" : [False],
    "abs_is_not_set" : [False],
    "no_accident_is_not_set" : [False]
})

def predict_price(new_data):
    try:
        pipeline = load('model/otomoto_price_prediction_model.joblib')
    except FileNotFoundError:
        print("Model not found.")
        if input("Create model? (y/n): ").lower() == 'y':
            try:
                create_model()
            except:
                print("Model creation failed!")
                return
        else:
            return
    pipeline = load('model/otomoto_price_prediction_model.joblib')
    predictions = pipeline.predict(new_data)
    return predictions