import streamlit as st 
import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import json
from lida import Manager, TextGenerationConfig , llm  
from dotenv import load_dotenv
import os
import openai
from PIL import Image
from io import BytesIO
import base64
from langchain_core.prompts import PromptTemplate

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def csv_agent(data,query):
    df=pd.read_csv(data)
    agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    )
    response=agent.run(query)
    return response


def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)
    
    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))


def decode_json_to_natural_language(data):
    template = """Convert the following  data to a natural language description suitable for exploratory data analysis (EDA):\n\n {json_data} \n\nAfter analyzing the dataset, provide a summary of the main observations, including key statistics, trends, and any interesting patterns or anomalies."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
    prompt = PromptTemplate(
        input_variables=["json_data"],
        template=template,
    )
    response = llm.invoke(prompt.format(json_data=data))
    return response.content


def auto_summarizer():
    lida = Manager(text_gen = llm("openai"))
    textgen_config = TextGenerationConfig(n=1, temperature=0.1, model="gpt-3.5-turbo-0301", use_cache=True)
    summary = lida.summarize("filename.csv",summary_method="default", textgen_config=textgen_config)
    # st.write(summary)
    goals = lida.goals(summary, n=2, textgen_config=textgen_config)
    goals_and_imgs=[]
    for i,goal in enumerate(goals):
        charts = lida.visualize(summary=summary, goal=goals[i], textgen_config=textgen_config, library="seaborn")  
        img_base64_string = charts[0].raster
        img = base64_to_image(img_base64_string)
        goals_and_imgs.append([goal.question,goal.visualization,goal.rationale,img])
        # st.write(goals_and_imgs)
    return goals_and_imgs,summary


def get_suggestions():
    lida = Manager(text_gen = llm("openai"))
    textgen_config = TextGenerationConfig(n=1, temperature=0.1, model="gpt-3.5-turbo-0301", use_cache=True)
    summary = lida.summarize("filename.csv",summary_method="default", textgen_config=textgen_config)
    goals = lida.goals(summary, n=3, textgen_config=textgen_config)
    return goals


def auto_visualazier(text_area):
    lida = Manager(text_gen = llm("openai")) 
    textgen_config = TextGenerationConfig(n=2, temperature=0.2, use_cache=True)
    summary = lida.summarize("filename1.csv", summary_method="default", textgen_config=textgen_config)
    user_query = text_area
    # goals = lida.goals(summary, n=2, textgen_config=textgen_config)
    charts = lida.visualize(summary=summary, goal=user_query, textgen_config=textgen_config)
    # st.write(charts)
    try:
        # charts[0]
        image_base64_1 = charts[0].raster
        image_base64_2 = charts[1].raster
        img1 = base64_to_image(image_base64_1)
        img2 = base64_to_image(image_base64_2)
        return img1,img2
    except:
        return None
        


#---------------------------------------------------------------------------------------------------------
if __name__=="__main__":

    menu = st.sidebar.selectbox("Choose an Option", ["Summarize", "Question based Graph"])

    if menu == "Summarize":
        st.subheader("Summarization of your Data")
        file_uploader = st.file_uploader("Upload your CSV", type="csv")
        button=st.button('summarize')
        if (file_uploader is not None) and button:
            path_to_save = "filename.csv"
            with open(path_to_save, "wb") as f:
                f.write(file_uploader.getvalue())
            
            goals_and_imgs=auto_summarizer()
            for goal_and_img in goals_and_imgs:
                st.write(goal_and_img[0])
                st.write(goal_and_img[1])
                st.write(goal_and_img[2])
                st.image(goal_and_img[3])
            
    elif menu == "Question based Graph":
        st.subheader("Query your Data to Generate Graph")
        file_uploader = st.file_uploader("Upload your CSV", type="csv")

        if file_uploader is not None:
            path_to_save = "filename1.csv"
            with open(path_to_save, "wb") as f:
                f.write(file_uploader.getvalue())
            if st.button("Are you confused , about what to query for generate, click here to get suggesions",type='secondary'):
                goals=get_suggestions()
                for i,goal in enumerate(goals):
                    st.markdown(f"{i+1}. {goal.question}  \n{goal.visualization}.  \n{goal.rationale}")
            
            text_area = st.text_area(label="**Enter Your Query**",placeholder="Ex: What is the relationship between credit_score and account_balance?" ,height=200)
            
            if st.button("Generate Graph",type='primary'):
                if len(text_area) > 0:
                    st.info("Your Query: " + text_area)
                    
                    imgs=auto_visualazier(text_area)
                    if imgs==None:
                        st.write("encounter some error")
                    else:
                        img1,img2=imgs
                        col1, col2 = st.columns(2)
                        with col1:
                            st.image(img1)
                        with col2:
                            st.image(img2)


