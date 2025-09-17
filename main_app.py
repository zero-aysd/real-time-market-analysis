import os
from typing import Optional, Dict, Any
import mlflow
from langchain_openai import AzureChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from get_stock_ticker import get_stock_ticker
from langchain_exa import ExaSearchResults
from prompt_experiments.prompt import react_prompt_template
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configuration class for better maintainability
class Config:
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    MODEL = os.getenv("MODEL")
    EXA_API_KEY = os.getenv("EXA_API_KEY")

# Sentiment schema definition
class SentimentSchema(BaseModel):
    company_name: str = Field(description="Name of the company")
    stock_code: str = Field(description="Stock ticker symbol")
    newsdesc: str = Field(description="Summary of news content")
    sentiment: str = Field(description="Overall sentiment (positive/negative/neutral)")
    people_names: list[str] = Field(description="Key people mentioned")
    places_names: list[str] = Field(description="Locations mentioned")
    other_companies_referred: list[str] = Field(description="Other companies mentioned")
    related_industries: list[str] = Field(description="Related industries")
    market_implications: str = Field(description="Potential market impact")
    confidence_score: float = Field(description="Confidence in sentiment analysis")

def setup_mlflow() -> None:
    """Configure MLflow experiment settings."""
    mlflow.set_experiment("company_sentiment_profile")
    mlflow.langchain.autolog()

def initialize_llm() -> AzureChatOpenAI:
    """Initialize and return AzureChatOpenAI instance."""
    try:
        return AzureChatOpenAI(
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            api_key=Config.AZURE_OPENAI_API_KEY,
            api_version=Config.AZURE_OPENAI_API_VERSION,
            azure_deployment=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
            model=Config.MODEL,
            temperature=0.2
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize LLM: {str(e)}")

def fetch_company_news(company_name: str) -> Dict[str, Any]:
    """Fetch latest financial news for a company."""
    try:
        tool = ExaSearchResults(exa_api_key=Config.EXA_API_KEY)
        return tool._run(
            query=f"Latest financial news about {company_name}",
            num_results=5,
            text_contents_options=True,
            highlights=True
        )
    except Exception as e:
        raise RuntimeError(f"Failed to fetch news for {company_name}: {str(e)}")

def process_news_articles(news: Any) -> str:
    """Convert news results into a single string for analysis."""
    if not hasattr(news, "results") or not news.results:
        return ""
    
    articles = []
    for result in news.results:
        print(result, dir(result))
        text = result.text
        highlights = result.highlights
        article_content = f"Article: {text}\nHighlights: {' '.join(highlights)}\n" if highlights else f"Article: {text}\n"
        articles.append(article_content)
    
    return "\n".join(articles) if articles else ""

def analyze_sentiment(
    company_name: str,
    stock_code: str,
    news: str,
    llm: AzureChatOpenAI
) -> SentimentSchema:
    """Analyze sentiment of company news."""
    try:
        prompt_template = ChatPromptTemplate.from_template(react_prompt_template)
        parser = PydanticOutputParser(pydantic_object=SentimentSchema)
        
        runnable = (prompt_template | llm | parser).with_config({
            "run_name": "sentiment_chain",
            "metadata": {
                "company": company_name,
                "stock_code": stock_code,
                "news_length": len(news),
            }
        })
        print(prompt_template)
        
        return runnable.invoke(
            {"company_name": company_name, "stock_code": stock_code, "news": news},
            config={"metadata": {"stage": "sentiment_analysis"}}
        )
    except Exception as e:
        raise RuntimeError(f"Sentiment analysis failed for {company_name}: {str(e)}")

def run_pipeline(company_name: str) -> Dict[str, Any]:
    """
    Run the complete sentiment analysis pipeline for a company.
    
    Args:
        company_name: Name of the company to analyze
        
    Returns:
        Dictionary containing sentiment analysis results
    """
    setup_mlflow()
    
    with mlflow.start_run(run_name=f"pipeline_{company_name}") as run:
        try:
            # Get stock ticker
            stock_code = get_stock_ticker(company_name)
            mlflow.log_param("company_name", company_name)
            mlflow.log_param("stock_code", stock_code)
            
            # Fetch and process news
            news = fetch_company_news(company_name)
            news_text = process_news_articles(news)
            if not news_text:
                raise ValueError(f"No valid news content found for {company_name}")
            mlflow.log_text(news_text, "news.txt")
            # mlflow.log_dict({"articles": [dict(r) for r in news.results]}, "raw_news.json")
            
            # Initialize LLM and analyze sentiment
            llm = initialize_llm()
            sentiment_output = analyze_sentiment(company_name, stock_code, news_text, llm)
            
            # Convert to dict and log results
            sentiment_dict = (
                sentiment_output.dict() 
                if hasattr(sentiment_output, "dict") 
                else sentiment_output
            )
            
            mlflow.log_dict(sentiment_dict, "sentiment_output.json")
            mlflow.log_metric("confidence", sentiment_dict.get("confidence_score", 0.0))
            
            return sentiment_dict
            
        except Exception as e:
            mlflow.log_param("error", str(e))
            raise

if __name__ == "__main__":
    try:
        result = run_pipeline("Microsoft")
        print(result)
    except Exception as e:
        print(f"Pipeline failed: {str(e)}")