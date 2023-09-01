#Insert library installation here
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('langchain')
install('huggingface_hub')
install('wikipedia')
# Bring in deps
import os
from apikey import apikey

import streamlit as st
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

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
    input_variables=['title','wikipedia_research'],
    template='write me a yoututbe video script based on this title TITLE: {title} while leveraging this wikipedia research: {wikipedia_research}'
)

#Memory
title_memory=ConversationBufferMemory(input_key='topic' ,memory_key='chat_history')
script_memory=ConversationBufferMemory(input_key='title' ,memory_key='chat_history')

# Llms
llm=HuggingFaceHub(repo_id="google/flan-t5-xxl",model_kwargs={"temperature":0.9,"max_length":1024}) 
title_chain=LLMChain(llm=llm, prompt=title_template,verbose=True,output_key='title',memory=title_memory)
script_chain=LLMChain(llm=llm, prompt=script_template,verbose=True,output_key='script',memory=script_memory)

wiki=WikipediaAPIWrapper()

#sequential_chain=SimpleSequentialChain(chains=[title_chain,script_chain],verbose=True)
#sequential_chain=SequentialChain(chains=[title_chain,script_chain],input_variables=['topic'],output_variables=['title','script'],verbose=True)

#Show stuff to the screen if there is a prompt
if prompt:
    #response=sequential_chain({'topic':prompt})
    title=title_chain.run(prompt)
    wiki_research=wiki.run(prompt)
    script=script_chain.run(title=title,wikipedia_research=wiki_research)


    st.write(title) #render back to screen
    st.write(script)
    
    with st.expander('Title History'):
        st.info(title_memory.buffer)

    with st.expander('Script History'):
        st.info(script_memory.buffer)

    with st.expander('Wikipedia Research History'):
        st.info(wiki_research)