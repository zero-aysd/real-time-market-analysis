Real-Time Market Analysis
This repository provides a Python-based pipeline for real-time market sentiment analysis, leveraging Azure OpenAI, MLflow, and Exa to fetch financial news, analyze sentiment, and track experiments.
Table of Contents

Overview
Features
Prerequisites
Installation
Configuration
Azure OpenAI
Exa API
MLflow
Stock Ticker Service


Usage
Run the Pipeline
Batch Processing
View MLflow Experiments


Troubleshooting
Contributing
License
Support

Overview
The pipeline fetches real-time financial news for a specified company, performs sentiment analysis using Azure OpenAI, and logs results to MLflow. It’s designed for scalability, modularity, and robust error handling.
Features

News Retrieval: Fetches latest financial news using Exa API.
Sentiment Analysis: Analyzes news sentiment with Azure OpenAI’s LLM.
Experiment Tracking: Logs parameters, metrics, and artifacts in MLflow.
Modular Code: Organized with reusable functions and clear configuration.
Stock Ticker Lookup: Integrates with external or local stock ticker services.

Prerequisites

Python: 3.10 or higher
Git: For cloning the repository
Azure OpenAI: Account with API access
Exa API: API key for news retrieval
MLflow: Optional tracking server (local or remote)
Stock Ticker Service: API or local implementation for ticker lookup

Installation

Clone the Repository:
git clone https://github.com/zero-aysd/real-time-market-analysis.git
cd real-time-market-analysis


Set Up Virtual Environment:
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate


Install Dependencies:
pip install -r requirements.txt


Verify Project Structure:
real-time-market-analysis/

├── main_app.py      # Core pipeline logic
├── streamlit_ui.py      # streamlit ui for testing
├── get_stock_ticker.py        # Stock ticker utility
└── prompt_experiments/
└── prompt.py                  # Prompt templates
├── .env.example               # Environment variable template
├── requirements.txt               # Dependencies
└── README.md                      



Configuration
Azure OpenAI

Create Resource:

In Azure Portal, create an Azure OpenAI resource.
Note the Endpoint URL and API Key.


Deploy Model:

In Azure OpenAI Model, deploy a model (e.g., gpt-4o or gpt-3.5-turbo).
Record the Deployment Name.


Set Environment Variables:

Copy .env.example to .env:
cp .env.example .env


Edit .env with your credentials:
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
MODEL=gpt-4o





Exa API

Obtain API Key:

Sign up at Exa API and generate an API key.


Add to .env:
EXA_API_KEY=your-exa-api-key



MLflow
Local Tracking

MLflow uses local file storage by default (./mlruns).

Add to .env:
MLFLOW_TRACKING_URI=http://localhost:5000



Usage
Run the Pipeline
Analyze sentiment for a single company (default: Microsoft):
python3 main_app.py

To analyze a different company, modify main_app.py:
if __name__ == "__main__":
    try:
        result = run_pipeline("Apple")  # Change to desired company
        print(result)
    except Exception as e:
        print(f"Pipeline failed: {str(e)}")

Streamlit UI

Start Streamlit UI:
streamlit run streamlit_ui.py



View MLflow Experiments

Start MLflow UI:
mlflow ui


Open http://localhost:5000 in your browser.

Navigate to the company_sentiment_profile experiment to view:

Parameters: company_name, stock_code
Metrics: confidence
Artifacts: news.txt, raw_news.json, sentiment_output.json



Ouputs