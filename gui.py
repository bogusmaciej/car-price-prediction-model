import PySimpleGUI as sg
from otomoto_predict import predict_price
import pandas as pd

sg.theme("DarkGrey5")
common_margin = ((0, 10), (0, 10))
voivodeships_list = [
    "Małopolskie", "Lubelskie", "Dolnośląskie", "Kujawsko-pomorskie",
    "Lubuskie", "Łódzkie", "Mazowieckie", "Opolskie", "Podkarpackie", 
    "Podkarpackie", "Pomorskie", "Śląskie", "Świętokrzyskie", 
    "Warmińsko-mazurskie", "Wielkopolskie", "Zachodniopomorskie"
]

label_column = [
    [sg.Text("Seller Type", size=(15, 1), pad=common_margin)],
    [sg.Text("Vehicle Brand", size=(15, 1), pad=common_margin)],
    [sg.Text("Vehicle Model", size=(15, 1), pad=common_margin)],
    [sg.Text("Production Year", size=(15, 1), pad=common_margin)],
    [sg.Text("Mileage", size=(15, 1), pad=common_margin)],
    [sg.Text("Fuel Type", size=(15, 1), pad=common_margin)],
    [sg.Text("Color", size=(15, 1), pad=common_margin)],
    [sg.Text("Air Conditioning", size=(15, 1), pad=common_margin)],
    [sg.Text("ABS", size=(15, 1), pad=common_margin)],
    [sg.Text("No Accident", size=(15, 1), pad=common_margin)],
    [sg.Text("Voivodeship", size=(15, 1), pad=common_margin)],
]

input_column = [
    [sg.InputCombo(["Private Person", "Dealer"], key="seller_type", size=(16, 1), readonly=True, pad=common_margin)],
    [sg.InputText(key="vehicle_brand", size=(18, 1), pad=common_margin)],
    [sg.InputText(key="vehicle_model", size=(18, 1), pad=common_margin)],
    [sg.InputText(key="production_year", size=(18, 1), pad=common_margin)],
    [sg.InputText(key="mileage", size=(10, 1), pad=common_margin), sg.InputCombo(["km", "mil"], key="units", size=(4, 1), readonly=True, pad=common_margin)],
    [sg.InputCombo(["Diesel", "Gasoline", "Gasoline + LPG"], key="fuel_type", size=(16, 1), readonly=True, pad=common_margin)],
    [sg.InputText(key="color", size=(18, 1), pad=common_margin)],
    [sg.Radio("True", "radio_air_conditioning", key="automatic_air_conditioning", default=True, pad=common_margin), sg.Radio("False", "radio_air_conditioning", key="automatic_air_conditioning", pad=common_margin)],
    [sg.Radio("True", "radio_abs", key="abs", default=True, pad=common_margin), sg.Radio("False", "radio_abs", key="abs", pad=common_margin)],
    [sg.Radio("True", "radio_no_accident", key="no_accident", default=True, pad=common_margin), sg.Radio("False", "radio_no_accident", key="no_accident", pad=common_margin)],
    [sg.InputCombo(voivodeships_list, key="voivodship", size=(16, 1), readonly=True, pad=common_margin)],
]

button_column = [
    [sg.Button("Calculate Price", size=(15, 1), button_color=("white", "green"), pad=common_margin)],
    [sg.Text("", key="price_text", size=(20, 1), pad=common_margin, font=('',16))],
]

layout = [
    [
        sg.Column(label_column, justification="left", vertical_alignment="top"),
        sg.Column(input_column, vertical_alignment="top"),
    ],
    [sg.Column(button_column, justification="right")],
    [sg.Column([[sg.Text("", size=(20, 1), text_color="red", key="validation_error", pad=common_margin)]], justification="right")],
]

window = sg.Window('Window Title', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "Calculate Price":
        if any(values[key] == "" for key in ["vehicle_brand", "vehicle_model", "production_year", "mileage", "units", "fuel_type", "color", "automatic_air_conditioning", "abs", "no_accident", "voivodship"]):
            window["validation_error"].update("Fill in all fields!", text_color="red")
        elif any(not values[key].isnumeric() for key in ["production_year", "mileage"]):
            window["validation_error"].update("Incorrect data!", text_color="red")
        else:
            window["validation_error"].update("")

            car_info = pd.DataFrame({'seller_type' : [values['seller_type']],
                        'vehicle_brand' : [values['vehicle_brand']],
                        'vehicle_model' : [values['vehicle_model']],
                        'production_year' : [values['production_year']],
                        'mileage' : [int(values['mileage'])],
                        'units' : [values['units']],
                        'fuel_type' : [values['fuel_type']],
                        'color' : [values['color']],
                        'automatic_air_conditioning' : [values['automatic_air_conditioning']],
                        'abs' : [values['abs']],
                        'no_accident' : [values['no_accident']],
                        'voivodship' : [values['voivodship']],
                        "mileage_is_not_set" : [False],
                        "automatic_air_conditioning_is_not_set" : [False],
                        "abs_is_not_set" : [False],
                        "no_accident_is_not_set" : [False]
            })
        
            price = predict_price(car_info)
            window["price_text"].update(f'{price[0]} PLN')
window.close()