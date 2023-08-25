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
from langchain.llms import HuggingFacePipeline

os.environ['HUGGINGFACEHUB_API_TOKEN']=apikey

#App framework
st.title('🦜️🔗 YouTube GPT Creator')
prompt=st.text_input('Plug in your prompt here')

# Llms
llm=HuggingFacePipeline(temperature=0.9 ) #How creative the llm to be

#Show stuff to the screen if there is a prompt
if prompt:
    response=llm(prompt)
    st.write(prompt) #render back to screen