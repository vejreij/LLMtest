#Insert library installation here
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('langchain')
# Bring in deps
import os
from apikey import apikey

import streamlit as st
from langchain.llms import HuggingFaceHub

os.environ['HUGGINGFACEHUB_API_TOKEN']=apikey

#App framework
st.title('🦜️🔗 YouTube GPT Creator')
prompt=st.text_input('Plug in your prompt here')

# Llms
llm=HuggingFaceHub(repo_id="google/flan-t5-xl",model_kwargs={"temperature":0.9}) 

#Show stuff to the screen if there is a prompt
if prompt:
    response=llm(prompt)
    st.write(prompt) #render back to screen