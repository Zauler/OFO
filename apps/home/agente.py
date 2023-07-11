import pandas as pd
import numpy as np
from dotenv import load_dotenv, find_dotenv
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent
load_dotenv(find_dotenv())


def realizar_consulta_agente(consulta,df):
    chat = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.0)
    agent = create_pandas_dataframe_agent(chat,df, verbose=False)
    respuesta = agent.run(consulta)
    return respuesta
