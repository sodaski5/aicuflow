import os
import pandas as pd
import joblib
from celery import shared_task
from sklearn.linear_model import LinearRegression
from .models import Node

@shared_task
def run_node(node_id):
    node = Node.objects.get(id=node_id)
    node.status = 'running'
    node.save()

    try:
        os.makedirs('datasets', exist_ok=True)
        os.makedirs('models', exist_ok=True)

        # eXtRaCt NoDe
        if node.node_type == 'Extract':
            dataset_name = node.config.get('dataset', 'local')

            if dataset_name == 'local':
                # use local CSV for demo
                local_csv = 'datasets/melb_data.csv'
                if not os.path.exists(local_csv):
                    raise FileNotFoundError(
                        "Local CSV not found. Download from Kaggle and place it in datasets/"
                    )
                node.config['output'] = local_csv
            else:
                # kaggle download (requires valid kaggle.json)
                from kaggle.api.kaggle_api_extended import KaggleApi
                api = KaggleApi()
                api.authenticate()
                api.dataset_download_file(
                    dataset_name,
                    file_name="melb_data.csv",
                    path="datasets",
                    unzip=True
                )
                node.config['output'] = 'datasets/melb_data.csv'

            node.status = 'completed'

        # tRaNsFoRm NoDe
        elif node.node_type == 'Transform':
            input_node = node.inputs.first()
            if not input_node or 'output' not in input_node.config:
                raise ValueError("Transform Node missing input or input not completed")
            df = pd.read_csv(input_node.config['output'])
            # drop rows with missing values
            df = df.dropna()
            clean_csv = 'datasets/housing_clean.csv'
            df.to_csv(clean_csv, index=False)
            node.config['output'] = clean_csv
            node.status = 'completed'

        # tRaIn NoDe
        elif node.node_type == 'Train':
            input_node = node.inputs.first()
            if not input_node or 'output' not in input_node.config:
                raise ValueError("Train Node missing input or input not completed")
            df = pd.read_csv(input_node.config['output'])
            # assume last column is target
            X = df.iloc[:, :-1]
            y = df.iloc[:, -1]
            model = LinearRegression()
            model.fit(X, y)
            os.makedirs('models', exist_ok=True)
            joblib.dump(model, 'models/model.pkl')
            node.status = 'completed'

        else:
            node.status = 'idle'

    except Exception as e:
        node.status = 'failed'
        node.config['error'] = str(e)

    node.save()
