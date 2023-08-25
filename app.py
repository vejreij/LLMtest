# Bring in deps
import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI

os.environ['HUGGINGFACEHUB_API_TOKEN']=apikey

#App framework
st.title('🦜️🔗 YouTube GPT Creator')
prompt=st.text_input('Plug in your prompt here')