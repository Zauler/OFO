import pandas as pd
import numpy as np
from dotenv import load_dotenv, find_dotenv
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent
load_dotenv(find_dotenv())


def realizar_consulta_agente(consulta,df):
    chat = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.0)
    agent = create_pandas_dataframe_agent(chat,df, verbose=True)
    promt_defecto = f"""Voy a realizarte una consulta para extraer información sobre un dataframe que se llama df.
      Este dataframe tiene la columna 'Proyecto', que corresponde a los proyectos de la empresa X, es un campo de texto donde está el nombre de los proyectos.
      Luego tenemos el campo de 'Proveedor / Cliente' aquí se almacenan los proovedores o clientes del registro y van mezclados es un campo de texto.
      Luego tenemos 'Concepto' que es otro campo de texto donde estará puesto una breve descripcioón que justifica la entrada o salida del dinero.
      Luego tendremos 'Tipo' que puede ser 'Compra' o 'Venta' si es compra significa que nosotros hemos gastado el dinero y si es venta es que nos pagan a nosotros. 
      'Importe' es la columna donde tenemos en formato de número la cantidad que nos ha costado o nos han pagado por algo. 
      Columna 'Tipo Pago' donde ponemos como recibimos el pago, 'TRANSFERENCIA' o 'CONFIRMING' normalmente. 
      'Fecha Factura' en formato de fecha cuando se hace la factura. 
      'Fecha Vencimiento' es cuando vence el pago o el cobro. 
      'Banco' es el banco donde se deposita o extrae el dinero. 
      'Fact. Emit. Recibida' es la columna donde ponemos 'True' si la factura ha sido recibida y 'False' si no. 
      'Pago Emit. Recibido' es la columna donde ponemos si el pago ha sido recibido , igual que antes True si es verdad False si no ha sido recibido. 
      'Gestor' es la columna donde ponemos la persona que lleva el Proyecto a la que se asocia la linea. 
      Si se hace referencia al dinero (normalmente se referirá a este dataframe) y otro campo que coincida con alguno de los anteriores la respuesta correcta será un número de la tabla importes (que es el dinero) con operaciones como filtros, sumas o diversas operaciones aritméticas.
      Por otro lado, voy a darte otro dataframe llamado df2, este dataframe contiene la información de los gestores, es decir en la base de datos va conectado con la columna 'Gestor',
      la relación es que un gestor puede estar en muchos registros, es decir de 1 a varios. Este dataframe contiene las siguientes columnas:
      'id_Gestor' que es el id de la columna autoincremental.
      'Nombre' que es el nombre del Gestor, es posible que algunos veces las peticiones te las pidan con el nombre y apellidos los dos al mismo tiempo, o solo el nombre o solo los apellidos. 
      'Apellidos' es el apellido del gestor, puede ser que te lo pidan con el nombre o sin el nombre.
      'DNI' es el documento de identidad español del gestor.
      'Zona_Geo' es la zona greográfica por donde estan designados los gestores o su zona de gestión. Se pueden referir a esta columna por la palabra zona.
      Si te hacen referencia a los gestores pero no incluyen el dinero o las ventas o los proyectos o los clientes lo más seguro es que se refieran a este df2. Además la mayoría de peticiones que se te realizarán se pueden gestionar con filtros de las columnas.
      Los dataframe de los que te acabo de hablar han sido pasados de la siguiente forma [df,df2]
      Con esta información resuelveme la siguiente consulta : ///{consulta}/// """
    # promt_defecto = f"""I'll be manipulating two dataframes, df and df2. In df, the columns are: 'Proyecto'- project name; 'Proveedor / Cliente'- mixed names of suppliers or clients; 'Concepto'- brief description of the transactions; 'Tipo'- 'Compra' or 'Venta', indicating if money was spent or received; 'Importe'- amount of money in number; 'Tipo Pago'- how the payment is received, typically 'TRANSFERENCIA' or 'CONFIRMING'; 'Fecha Factura'- invoice date; 'Fecha Vencimiento'- due date for payment; 'Banco'- where money is deposited or withdrawn; 'Fact. Emit. Recibida'- whether the invoice was received (True/False); 'Pago Emit. Recibido'- whether the payment was received (True/False); 'Gestor'- person in charge of the project.
    # df2 contains information about managers and is related to df through the 'Gestor' column. Its columns are: 'id_Gestor'- unique ID of the managers; 'Nombre'- manager's name; 'Apellidos'- manager's surname; 'DNI'- identity document; 'Zona_Geo'- manager's area of management.
    # I'll be performing operations such as filters, sums, or various arithmetic operations on df. Queries that don't include money, sales, projects, or clients likely refer to df2. The dataframes were provided to me as [df,df2]. Now, I'll process the following query in spanish or english, translate it but care about the names of the columns: ///{consulta}///"""
    respuesta = agent.run(promt_defecto)
    return respuesta


#import copy
#from llama_cpp import Llama #Importante

# def agente_llm(consulta,df):
#     # load the model
#     llm = Llama(model_path="./models/stable-vicuna-13B.ggml.q4_0.bin")
#     print("Model loaded!")
#     agent = create_pandas_dataframe_agent(llm,df, verbose=True)

#     result = copy.deepcopy(agent)
#     text = result["choices"][0]["text"] #El resultado es este.
#     return {"result": text}

#Para utilizar este modelo requiere de una tarjeta gráfica potente y utilizar llama_cpp y varias
#Librerías de C, lo dejamos aquí para que se vea que puede ser una opción y de hecho se ha probado y funcionaba en el momento de crear estas líneas, 
#Aunque los resultados son peores que con la API KEY de OPENAI 