from gui import CarPricePredictionApp
import tkinter as tk
from joblib import load
from otomoto import create_model

if __name__ == "__main__":
    try:
        pipeline = load('model/otomoto_price_prediction_model.joblib')
    except FileNotFoundError:
        print("Model not found.")
        if input("Create model? (y/n): ").lower() == 'y':
            try:
                create_model()
            except:
                print("Model creation failed!")
    root = tk.Tk()
    app = CarPricePredictionApp(root)
    root.mainloop()