#required dis
import os 
import streamlit as st 
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.llms import GooglePalm 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

#env 
serp_api = os.environ.get("serp_api")
os.environ["SERPAPI_API_KEY"] = os.environ.get('SERPAPI_API_KEY')
palm_api = os.environ.get('palm_api')


#LLMs 

llm = GooglePalm(google_api_key=palm_api, temperature=0.7)

def generate_restaurant_name_and_items(cuisine):
    #Chain 1: Restaurant Name 
    prompt_template_name = PromptTemplate(
    input_variables=['cuisine'],
    template="I want to open a restaurant for {cuisine} food. Suggest a single one fancy name for this."
    )

    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")

    #Chain 2: Menu Items 
    prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="""Suggest some menu items for {restaurant_name}. Return it as comma separated string"""
    )

    food_items_chain = LLMChain(llm=llm, prompt=prompt_template_items, output_key='menu_items')


    chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', 'menu_items']
    )

    response = chain({'cuisine': cuisine})
    return response 

if __name__ == '__main__':
    print(generate_restaurant_name_and_items('Italian'))