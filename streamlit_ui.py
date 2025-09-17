import streamlit as st
import json
from main_app import run_pipeline  

st.title("Company Sentiment Analysis")

company_name = st.text_input("Enter Company Name", value="Microsoft")

if st.button("Analyze Sentiment"):
    if company_name.strip() == "":
        st.error("Please enter a valid company name.")
    else:
        with st.spinner(f"Running sentiment analysis for {company_name}..."):
            try:
                result = run_pipeline(company_name)
                st.success("Analysis completed!")
               
                st.json(result)
            except Exception as e:
                st.error(f"Error running pipeline: {str(e)}")
