import vertexai
import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel

def get_model():
    credentials = service_account.Credentials.from_service_account_info({
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"],
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"],
        "universe_domain": st.secrets["universe_domain"]
    })
    vertexai.init(project="997948407242", location="us-central1", credentials=credentials)
    return GenerativeModel("projects/997948407242/locations/us-central1/endpoints/2036231762966740992")
