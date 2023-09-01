#Insert library installation here
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('langchain')
install('huggingface_hub')
# Bring in deps
import os
from apikey import apikey

import streamlit as st
from langchain.llms import HuggingFaceHub
from langchain.prompt import PromptTemplate
from langchain.chains import LLMChain

os.environ['HUGGINGFACEHUB_API_TOKEN']=apikey

#App framework
st.title('🦜️🔗 YouTube GPT Creator')
prompt=st.text_input('Plug in your prompt here')

#Prompt templates
title_template=PromptTemplate(
    input_variable=['topic'],
    template='write me a yoututbe video title about {topic}'
)

# Llms
llm=HuggingFaceHub(repo_id="google/flan-t5-xxl",model_kwargs={"temperature":0.9}) 
title_chain=LLMChain(llm=llm, prompt=title_template,verbose=True)

#Show stuff to the screen if there is a prompt
if prompt:
    response=title_chain.run(topic=prompt)
    st.write(response) #render back to screen