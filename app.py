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
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain

os.environ['HUGGINGFACEHUB_API_TOKEN']=apikey

#App framework
st.title('🦜️🔗 YouTube GPT Creator')
prompt=st.text_input('Plug in your prompt here')

#Prompt templates
title_template=PromptTemplate(
    input_variables=['topic'],
    template='write me a yoututbe video title about {topic}'
)

script_template=PromptTemplate(
    input_variables=['title'],
    template='write me a yoututbe video script based on this title TITLE: {title}'
)

# Llms
llm=HuggingFaceHub(repo_id="google/flan-t5-xxl",model_kwargs={"temperature":0.9,"max_length":1024}) 
title_chain=LLMChain(llm=llm, prompt=title_template,verbose=True)
script_chain=LLMChain(llm=llm, prompt=script_template,verbose=True)
sequential_chain=SimpleSequentialChain(chains=[title_chain,script_chain],verbose=True)

#Show stuff to the screen if there is a prompt
if prompt:
    response=sequential_chain.run(prompt)
    st.write(response) #render back to screen