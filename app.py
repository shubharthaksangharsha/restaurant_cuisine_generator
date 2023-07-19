#required dis
import os 
import streamlit as st 
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.llms import GooglePalm 
import langchain_helper
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

#env 
serp_api = os.environ.get("serp_api")
os.environ["SERPAPI_API_KEY"] = os.environ.get('SERPAPI_API_KEY')
palm_api = os.environ.get('palm_api')


#Prompt template 
prompt = PromptTemplate(
  input_variables=['cuisine'],
  template="I want to open a restaurant for {cuisine} food. Suggest me single fency name for this and don't provide any description just give me the single name of it nothing else."
)
#LLMs
llm = GooglePalm(google_api_key=palm_api, temperature=0.9)
chain = LLMChain(llm=llm, prompt=prompt)


# App framework
st.title('🦜🔗Restaurant Name Generator')
cuisine = st.sidebar.selectbox("Pick a Cuisine", ("", "Arabic",  "American", "British",  "Chinese", "French", "Korean", "Indian", "Italian", "Mexican", "Thai", "Afgani"), index=0)



#if there's a prompt
if cuisine: 
  response = langchain_helper.generate_restaurant_name_and_items(cuisine=cuisine)
  st.header(response['restaurant_name'].strip())
  menu_items = response['menu_items'].strip().split(",")
  st.write("**Menu Items**")
  for item in menu_items:
    st.write("-", item)