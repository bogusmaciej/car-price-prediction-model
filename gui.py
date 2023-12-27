import tkinter as tk
from tkinter import ttk
import pandas as pd
from otomoto_predict import predict_price

class CarPricePredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Price Prediction")

        self.create_widgets()

    def create_widgets(self):
        inputs_width = 25
        combobox_width = inputs_width - 3
        checkbox_default_value = False
        input_marign_right = 30
        label_marign_right = 30

        title_label = tk.Label(self.root, text="Car Price Prediction", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        # Labels and Entry widgets
        self.labels = ["Seller Type", "Vehicle Brand", "Vehicle Model", "Production Year", "Mileage", "Fuel Type",
                       "Power", "Numbers of doors", "Numbers of seats", "Electric front window", "Color",
                       "Air Conditioning", "ABS", "No Accident", "Drive type", "Damaged", "Voivodeship"]

        self.entries = {}
        for label_text in self.labels:
            label = tk.Label(self.root, text=label_text + ":")
            label.grid(row=self.labels.index(label_text)+1, column=0, sticky="e", pady=5, padx=label_marign_right)

            if label_text == "Seller Type":
                entry = ttk.Combobox(self.root, values=["Private Person", "Dealer"], width=combobox_width, state="readonly")
                entry.grid(row=self.labels.index(label_text)+1, column=1, pady=5, padx=(0, input_marign_right), sticky="w")
                self.entries[label_text] = entry
            elif label_text == "Mileage":
                entry = ttk.Entry(self.root, width=inputs_width-7)
                entry.grid(row=self.labels.index(label_text)+1, column=1, pady=5, sticky="w")
                unit_combobox = ttk.Combobox(self.root, values=["km", "mi"], width=3, state="readonly")
                unit_combobox.grid(row=self.labels.index(label_text)+1, column=1, padx=(0, input_marign_right), sticky="e")
                self.entries[label_text] = (entry, unit_combobox)
            elif label_text == "Fuel Type":
                entry = ttk.Combobox(self.root, values=['Diesel', 'Gasoline', 'Gasoline + LPG', 'Electric', 'Hybrid', 'Gasoline + CNG', 'Hydrogen'], width=combobox_width, state="readonly")
                entry.grid(row=self.labels.index(label_text)+1, column=1, columnspan=2, pady=5, padx=(0, input_marign_right), sticky="w")
                self.entries[label_text] = entry
            elif label_text == "Drive type":
                entry = ttk.Combobox(self.root, values=['4x4 (manually attached)', 'Front wheels', '4x4 (fixed)', '4x4 (attached automatically)', 'Rear wheels'], width=combobox_width, state="readonly")
                entry.grid(row=self.labels.index(label_text)+1, column=1, columnspan=2, pady=5, padx=(0, input_marign_right), sticky="w")
                self.entries[label_text] = entry
            elif label_text == "Voivodeship":
                entry = ttk.Combobox(self.root, values=[
                    "Małopolskie", "Lubelskie", "Dolnośląskie", "Kujawsko-pomorskie",
                    "Lubuskie", "Łódzkie", "Mazowieckie", "Opolskie", "Podkarpackie",
                    "Podkarpackie", "Pomorskie", "Śląskie", "Świętokrzyskie",
                    "Warmińsko-mazurskie", "Wielkopolskie", "Zachodniopomorskie"
                ], width=combobox_width, state="readonly")
                entry.grid(row=self.labels.index(label_text)+1, column=1, columnspan=2, pady=5, padx=(0, input_marign_right), sticky="w")
                self.entries[label_text] = entry
            elif label_text in ["Electric front window", "Air Conditioning", "ABS", "No Accident", "Damaged"]:
                var = tk.BooleanVar(value=checkbox_default_value)
                checkbox = ttk.Checkbutton(self.root, variable=var, onvalue=True, offvalue=False)
                checkbox.grid(row=self.labels.index(label_text)+1, column=1, pady=5, padx=(0, input_marign_right), sticky="w")
                self.entries[label_text] = var
            else:
                entry = ttk.Entry(self.root, width=inputs_width)
                entry.grid(row=self.labels.index(label_text)+1, column=1, columnspan=2, pady=5, padx=(0, input_marign_right), sticky="w")
                self.entries[label_text] = entry

        # Button for prediction
        predict_button = tk.Button(self.root, text="Predict Price", command=self.predict_price, bg="lightblue", fg="black", font=("Arial", 12))
        predict_button.grid(row=len(self.labels)+1, column=0, columnspan=3, pady=10)

        # Display predicted price
        predicted_price_label = tk.Label(self.root, text="Predicted Price:")
        predicted_price_label.grid(row=len(self.labels) + 2, column=0, pady=5, padx=10, sticky="e")

        self.predicted_price_value = tk.Label(self.root, text="", font=("Helvetica", 14, "bold"))
        self.predicted_price_value.grid(row=len(self.labels) + 2, column=1, pady=(25, 25), padx=(0, 10), sticky="w")

    def predict_price(self):
        to_skip = ["Electric front window", "Air Conditioning", "ABS", "No Accident", "Damaged"]
        for label_text in self.labels:
            if label_text in to_skip: continue

            if label_text in ["Mileage"]:
                if not self.entries[label_text][0].get() or not self.entries[label_text][1].get():
                    self.show_error("Please fill in all fields.")
                    return
            else:
                if not self.entries[label_text].get():
                    self.show_error("Please fill in all fields.")
                    return 
        
        seller_type = self.entries["Seller Type"].get()
        vehicle_brand = self.entries["Vehicle Brand"].get()
        vehicle_model = self.entries["Vehicle Model"].get()
        production_year = int(self.entries["Production Year"].get())

        mileage_entry, mileage_unit_combobox = self.entries["Mileage"]
        mileage = float(mileage_entry.get())
        mileage_unit = mileage_unit_combobox.get()

        fuel_type = self.entries["Fuel Type"].get()
        power = float(self.entries["Power"].get())
        num_doors = float(self.entries["Numbers of doors"].get())
        num_seats = float(self.entries["Numbers of seats"].get())

        electric_window = self.entries["Electric front window"].get()
        color = self.entries["Color"].get()
        air_conditioning = self.entries["Air Conditioning"].get()
        abs_system = self.entries["ABS"].get()
        no_accident = self.entries["No Accident"].get()
        drive_type = self.entries["Drive type"].get()
        damaged = self.entries["Damaged"].get()
        voivodeship = self.entries["Voivodeship"].get()

        car_params = pd.DataFrame({
            'seller_type' : [seller_type],
            'vehicle_brand' : [vehicle_brand.lower()],
            'vehicle_model' : [vehicle_model.lower()],
            'production_year' : [production_year],
            'mileage' : [mileage],
            'fuel_type' : [fuel_type],
            'power' : [power],
            'number_of_doors' : [num_doors],
            'number_of_seats' : [num_seats],
            'electric_front_windows' : [electric_window],
            'color' : [color.lower()],
            'automatic_air_conditioning' : [air_conditioning],
            'abs' : [abs_system],
            'no_accident' : [no_accident],
            'drive_type' : [drive_type],
            'damaged' : [damaged],
            "automatic_air_conditioning_is_not_set" : [False],
            "no_accident_is_not_set" : [False],
            'voivodship' : [voivodeship],
            'units' : [mileage_unit],
        })
        print(car_params.to_json())

        predicted_price = predict_price(car_params)
        self.predicted_price_value.config(text=f"{predicted_price[0]}PLN",fg="black")
        pass

    def show_error(self, message):
        self.predicted_price_value.config(text=message ,fg="red")