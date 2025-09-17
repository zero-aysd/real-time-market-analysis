# Real-Time Market Analysis

This repository provides a Python-based pipeline for real-time market sentiment analysis, leveraging **Azure OpenAI**, **MLflow**, and **Exa** to fetch financial news, analyze sentiment, and track experiments.

## Table of Contents

- Overview
- Features
- Prerequisites
- Installation
- Configuration
  - Azure OpenAI
  - Exa API
  - MLflow
  - Stock Ticker Service
- Usage
  - Run the Pipeline
  - Streamlit UI
  - View MLflow Experiments
- Outputs

## Overview

The pipeline fetches real-time financial news for a specified company, performs sentiment analysis using Azure OpenAI, and logs results to MLflow. It’s designed for scalability, modularity, and robust error handling.

## Features

- **News Retrieval**: Fetches latest financial news using Exa API.
- **Sentiment Analysis**: Analyzes news sentiment with Azure OpenAI’s LLM.
- **Experiment Tracking**: Logs parameters, metrics, and artifacts in MLflow.
- **Modular Code**: Organized with reusable functions and clear configuration.
- **Stock Ticker Lookup**: Integrates with external or local stock ticker services.

## Prerequisites

- **Python**: 3.10 or higher
- **Git**: For cloning the repository
- **Azure OpenAI**: Account with API access
- **Exa API**: API key for news retrieval
- **MLflow**: Optional tracking server (local or remote)
- **Stock Ticker Service**: API or local implementation for ticker lookup

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/zero-aysd/real-time-market-analysis.git
   cd real-time-market-analysis
   ```

2. **Set Up Virtual Environment**:

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Project Structure**:

   ```
   real-time-market-analysis/
   
   ├── main_app.py      # Core pipeline logic
   ├── streamlit_ui.py      # streamlit ui for testing
   ├── get_stock_ticker.py        # Stock ticker utility
   └── prompt_experiments/
   └── prompt.py                  # Prompt templates
   ├── .env.example               # Environment variable template
   ├── requirements.txt               # Dependencies
   └── README.md                      
   ```

## Configuration

### Azure OpenAI

1. **Create Resource**:

   - In Azure Portal, create an Azure OpenAI resource.
   - Note the **Endpoint URL** and **API Key**.

2. **Deploy Model**:

   - In Azure OpenAI Model, deploy a model (e.g., `gpt-4o` or `gpt-3.5-turbo`).
   - Record the **Deployment Name**.

3. **Set Environment Variables**:

   - Copy `.env.example` to `.env`:

     ```bash
     cp .env.example .env
     ```

   - Edit `.env` with your credentials:

     ```env
     AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
     AZURE_OPENAI_API_KEY=your-api-key
     AZURE_OPENAI_API_VERSION=2024-02-15-preview
     AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
     MODEL=gpt-4o
     ```

### Exa API

1. **Obtain API Key**:

   - Sign up at Exa API and generate an API key.

2. **Add to** `.env`:

   ```env
   EXA_API_KEY=your-exa-api-key
   ```

### MLflow

####  Local Tracking

- MLflow uses local file storage by default (`./mlruns`).
- Add to `.env`:

  ```env
  MLFLOW_TRACKING_URI=http://localhost:5000
  ```

## Usage

### Run the Pipeline

Analyze sentiment for a single company (default: Microsoft):

```bash
python3 main_app.py
```

To analyze a different company, modify `main_app.py`:

```python
if __name__ == "__main__":
    try:
        result = run_pipeline("Apple")  # Change to desired company
        print(result)
    except Exception as e:
        print(f"Pipeline failed: {str(e)}")
```

### Streamlit UI

1. Start Streamlit UI:

   ```bash
   streamlit run streamlit_ui.py
   ```

### View MLflow Experiments

1. Start MLflow UI:

   ```bash
   mlflow ui
   ```

2. Open `http://localhost:5000` in your browser.

3. Navigate to the `company_sentiment_profile` experiment to view:

   - Parameters: `company_name`, `stock_code`
   - Metrics: `confidence`
   - Artifacts: `news.txt`, `raw_news.json`, `sentiment_output.json`

### Ouputs
    
    {
        "company_name":"Alphabet Inc.",
        "stock_code":"GOOG",
        "newsdesc":"Shares of Google parent Alphabet surged to a record high on news that Gemini became the No. 1 free app in the U.S. Apple Store, overtaking OpenAI's ChatGPT. The stock climbed more than 4.5% to close at 251.61, giving Google a valuation of over $3 trillion. A favorable antitrust ruling also contributed to the stock's rise.",
        "sentiment":"Positive",
        "people_names":["Justin Patterson","Sundar Pichai","Donald Trump","Amit Mehta"],
        "places_names":["U.S.","Mountain View, California"],
        "other_companies_referred":["Apple","Microsoft","Nvidia","OpenAI"],
        "related_industries":["Technology","Artificial Intelligence","Cloud Computing"],
        "market_implications":"The surge in stock price and market cap indicates strong investor confidence, particularly in Google's AI capabilities with the Gemini app. This could lead to increased investment interest and potential market share growth in AI and cloud services.",
        "confidence_score":0.9
        }
    