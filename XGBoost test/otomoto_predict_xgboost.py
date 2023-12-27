import pandas as pd
from joblib import load

new_data = pd.DataFrame({
    'seller_type' : ["Private person"],
    'vehicle_brand' : ["Ford"],
    'vehicle_model' : ["Fiesta"],
    'production_year' : [2006],
    'mileage' : [170000],
    'fuel_type' : ["Gasoline"],
    'power' : [75],
    'number_of_doors' : [5.0],
    'number_of_seats' : [5.0],
    'electric_front_windows' : [False],
    'color' : ["navy blue"],
    'automatic_air_conditioning' : [False],
    'abs' : [True],
    'no_accident' : [True],
    'drive_type' : ['Front wheels'],
    'damaged' : [False],
    "automatic_air_conditioning_is_not_set" : [False],
    "no_accident_is_not_set" : [False],
    'voivodship' : ["Małopolskie"],
    'units' : ["km"],
})

def predict_price(new_data):
    pipeline = load('model/otomoto_price_prediction_model.joblib')
    predictions = pipeline.predict(new_data)
    return predictions

print(predict_price(new_data))