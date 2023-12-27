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
                "vehicle_model", "production_year", "mileage", "fuel_type", "power",
                "number_of_doors", "number_of_seats", "electric_front_windows",
                "color", "automatic_air_conditioning", "abs", "no_accident", "drive_type",
                "damaged"]

    df = df[features]

    to_lower_features = ['vehicle_brand','vehicle_model', 'color']

    for future in to_lower_features:
        df[future] = df[future].str.lower()

    df.replace({'no_accident':{"Tak": True}, 'damaged':{"Tak": True}}, inplace=True)
    df[['power', 'KM']] = df['power'].str.rsplit(' ', n=1, expand=True)
    df = df.drop('KM', axis=1)
    
    columns_with_nan = df.columns[df.isna().any()].tolist()

    for column in columns_with_nan:
        ratio = df[column].isna().sum()/df.shape[0]*100
        if(ratio<20):
            df = df.dropna(subset=[column])
        elif(ratio>80):
            df[column].fillna(False,inplace=True)
        else:
            label = column+"_is_not_set"
            df[label]=df[column].isna()
            df[column].fillna(False,inplace=True)

    df['voivodship'] = df['location'].apply(extract_voivodeship)
    df = df.drop(["currency", "location"], axis=1)
    
    df[['mileage', 'units']] = df['mileage'].str.rsplit(' ', n=1, expand=True)
    df['mileage'] = df['mileage'].str.replace(' ', '')
    df['power'] = df['power'].str.replace(' ', '')
    df['mileage'] = pd.to_numeric(df['mileage'])
    df['power'] = df['power'].astype('int')
    df.to_csv("data/otomoto_new.csv", sep=",",index=False)
    print("new file created!")