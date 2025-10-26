import pandas as pd
from sklearn.linear_model import LinearRegression
import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_from_kaggle(dataset_name):
    api = KaggleApi()
    api.authenticate()
    dataset_dir = f'data/{dataset_name.replace("/", "_")}'
    os.makedirs(dataset_dir, exist_ok=True)
    api.dataset_download_files(dataset_name, path=dataset_dir, unzip=True)
    # return first CSV found
    for file in os.listdir(dataset_dir):
        if file.endswith('.csv'):
            return os.path.join(dataset_dir, file)
    return None

def transform_data(file_path):
    df = pd.read_csv(file_path)
    # data cleaning: drop missing values
    df = df.dropna()
    return df

def train_model(df):
    # predict first numeric column using others
    y = df.select_dtypes(include='number').iloc[:, 0]
    X = df.select_dtypes(include='number').iloc[:, 1:]
    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_model(model, input_data=None):
    # use first few rows if no input
    if input_data is None:
        input_data = [[0]*len(model.coef_)] # fallback
    predictions = model.predict(input_data)
    return predictions.tolist()


