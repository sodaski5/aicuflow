# AICUFlow Mini Prototype

A small Django-based prototype inspired by AICUFlow's node-based AI platform.

## Features

- Node-based workflow: Extract → Transform → Train → Predict
- Kaggle dataset integration
- ETL pipeline
- Asynchronous execution with Celery + Redis
- REST API for workflow control and model predictions

## Requirements

- Python 3.9+
- Django
- Django REST Framework
- Celery
- Redis
- pandas, scikit-learn, joblib
- Kaggle API configured (`~/.kaggle/kaggle.json`)

## Setup

1. Create virtual environment and install packages: 2. Apply migrations and create superuser:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Apply migrations and create superuser:

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

3. Start services:

python manage.py runserver
celery -A aicuflow_core worker -l info
redis-server