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
       Si se hace referencia al dinero y otro campo que coincida con alguno de los anteriores la respuesta correcta será un número de la tabla importes (que es el dinero) con operaciones como filtros, sumas o diversas operaciones aritméticas
       Con esta información resuelveme la siguinte consulta : ///{consulta}/// """
    respuesta = agent.run(promt_defecto)
    return respuesta
