import pandas as pd 

voivodeships = ["Małopolskie", "Lubelskie", "Dolnośląskie", "Kujawsko-pomorskie",
                "Lubuskie", "Łódzkie", "Mazowieckie", "Opolskie", "Podkarpackie", 
                "Podkarpackie", "Pomorskie", "Śląskie", "Świętokrzyskie", 
                "Warmińsko-mazurskie", "Wielkopolskie", "Zachodniopomorskie"]


def extract_voivodeship(location):
    for voivodeship in voivodeships:
        if voivodeship in location:
            return voivodeship
    return "no_voivodeship"

def create_dataset():
    try:
        print("reading old file...")
        df = pd.read_csv("data/otomoto_offers_eng_23-04-2023.csv", on_bad_lines='skip', delimiter=";", low_memory=False)
    except FileNotFoundError:
        print("dataset file does not exist!")
        return    
        
    print("creating new file...")
    df = df[df["currency"]=="PLN"]

    features = ["price", "currency", "seller_type", "location", "vehicle_brand",
                "vehicle_model", "production_year", "mileage", "fuel_type", 
                "color", "automatic_air_conditioning", "abs", "no_accident"]

    df = df[features]
    df.replace({'no_accident':{"Tak": True}}, inplace=True)
    columns_with_nan = df.columns[df.isna().any()].tolist()
    for column in columns_with_nan:
        label = column+"_is_not_set"
        df[label]=df[column].isna()
        df[column].fillna(False,inplace=True)

    df['voivodship'] = df['location'].apply(extract_voivodeship)
    df = df.drop(["currency", "location"], axis=1)

    df[['mileage', 'units']] = df['mileage'].str.rsplit(' ', n=1, expand=True)
    df['mileage'] = df['mileage'].str.replace(' ', '')
    df['mileage'] = pd.to_numeric(df['mileage'])

    df.to_csv("data/otomoto_new.csv", sep=",",index=False)
    print("new file created!")
    
