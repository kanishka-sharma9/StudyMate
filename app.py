from dotenv import load_dotenv
load_dotenv()
import os
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
import google.generativeai as genai
import streamlit as st

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(diff,topic,material):
    prompt = f"""You are an expert teaching AI model with advanced knowledge of all programming languages.
    Your task is to generate 10 open-ended questions of {diff} difficulty on the topic:{topic}.
    The answer to these questions must be present in the following: {material}.\n\n
    
    <MESSAGE>:|"rate your responses on a scale on 1-10 based on your knowledge. if score is less than 4 generate
    a new response. do not display the rating." """
    # template = PromptTemplate(template=prompt,input_variables=['diff','topic','material'])
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(prompt)
    return response.text


st.set_page_config(page_title="Study Mate")

col1,col2,col3=st.columns(3)
with col1:
    st.subheader("select difficulty")
    diff=st.selectbox(" ",options=['Easy','Medium','Hard'])

with col2:
    st.subheader("Enter Topic")
    topic=st.text_input("Enter topic of interest:")

with col3:
    st.subheader("upload study material:")
    material=st.file_uploader('daldo bc kuch bhi isme:',type="pdf")
text=""
if material is not None:
    # text=''
    reader=PdfReader(material)
    for page in reader.pages:
        text+=page.extract_text()
if st.button("generate"):
    response=get_gemini_response(diff,topic,text)
    print(response)
    st.write(response)
