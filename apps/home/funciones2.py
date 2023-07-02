import pandas as pd
import numpy as np
# import funciones as fn
from apps.home.consultasDB import *
from datetime import datetime
from dateutil.relativedelta import relativedelta


def creaDFRegistros():
    df = ConsultasDB.consultaRegistros()
    df = df.sort_values(by='Fecha Vencimiento')   #Ordenamos el dataframe de menor a mayor por fecha de vencimiento

    return df


def rangoFechas():  #Crea un dataframe con fechas desde la fecha mínima hasta la fecha máxima
    df = creaDFRegistros()
    fechaMin = df["Fecha Vencimiento"].min()   #Fecha más antigua que contemple el archivo de pedidos
    fechaMax = df["Fecha Vencimiento"].max()   #Fecha máxima que contemple el archivo de pedidos
    dfFechas = pd.date_range(start=fechaMin, end=fechaMax)

    return dfFechas


def creaDataFlujo():    # Crea un dataset con los datos de todos los registros y completa con valores "0" para los días en los que no exista registro
    dfn = creaDFRegistros()
    dfn['Fecha Vencimiento'] = pd.to_datetime(dfn['Fecha Vencimiento']) # Convertimos los datos de la columna date en datetime para poder compararlos con dfFechas
    dfFechas = rangoFechas()
    registros = []
    columnasEliminar=['id_Registro', 'Proyecto', 'Proveedor / Cliente', 'Concepto', 'Gestor']
    dfn = dfn.drop(columnasEliminar,axis=1)

    indice = 0
    for i in dfFechas:
        
        if dfn.iloc[indice]["Fecha Vencimiento"] == i: # Si la fecha coincide entramos en el condicional
            while dfn.iloc[indice]["Fecha Vencimiento"] == i:
                registros.append([dfn.iloc[indice]['Banco'], dfn.iloc[indice]['Tipo'], dfn.iloc[indice]['Tipo Pago'],
                                    dfn.iloc[indice]['Fecha Factura'], dfn.iloc[indice]['Fecha Vencimiento'], round(dfn.iloc[indice]['Importe'],2),
                                    dfn.iloc[indice]['Fact. Emit. Recibida'], dfn.iloc[indice]['Pago Emit. Recibido']])
            
                if indice<dfn['Banco'].count()-1: # Para que el bucle while no de problemas con el indice. Le restamos 1 porque el DF empieza en 0
                    indice += 1 # Actualizamos el valor del indice
                else:
                    break

        else:
            registros.append(['','','',i,i,0,'',''])  #Añadimos una tupla "cero" si no hay datos en ese día

    
    columnas=['Banco', 'Tipo', 'Tipo Pago', 'Fecha Factura', 'Fecha Vencimiento', 'Importe',
            'Fact. Emit. Recibida', 'Pago Emit. Recibido']
    dfCompleto = pd.DataFrame(registros,columns=columnas)

    return dfCompleto


def creaDFTesoAgregadaPrevista():   # Tendremos en cuenta todos los registros incluso los que no se hayan facturado todavía (sean pedidos o certificaciones)
    fechaInicio = datetime.now() - relativedelta(months=3)
    fechaFin = datetime.now()
    df = creaDataFlujo()    # Recibimos una dataframe ordenado por fecha y con valores "cero" en los días en los que no existiese datos
    registros = []

    df = df.drop(df[df['Fecha Vencimiento']<=fechaInicio].index) # Vamos a analizar los datos a partir de la fecha "hoy"
    dfSignoPrevisto = df    #Creamos un nuevo dataframe
    dfSignoPrevisto.loc[dfSignoPrevisto['Tipo'] == 'Compra', 'Importe'] *= -1 # Cambiamos el signo a las compras
    df_grouped_Previsto = dfSignoPrevisto.groupby('Fecha Vencimiento')['Importe'].sum()  # Sumamos todos los valores de cada día
    df_grouped_Previsto=df_grouped_Previsto.round(2) # Redondeamos a 2 decimales para no tener problemas

    dfFechas = dfSignoPrevisto['Fecha Vencimiento'].unique()

    # Partimos de la tesoreria de los bancos
    df_bancos = ConsultasDB.consultaBancos()
    tesoreria = df_bancos['Cash'].sum()
    
    for i in range (0,len(dfFechas)):
        tesoreria += df_grouped_Previsto[i]
        registros.append([dfFechas[i],round(tesoreria,2)])

    dfAgregadoPrevisto = pd.DataFrame(registros,columns=['Fecha Vencimiento','Importe'])
    dfAgregadoPrevisto.to_csv("datos/dfAgregadoPrevisto.csv", index=False)

    return dfAgregadoPrevisto


def creaDFTesoAgregadaDisponible(): #Tendremos en cuenta sólo lo que esté facturado y con previsión de cobro o pago
    fechaInicio = datetime.now() - relativedelta(months=3)
    df = creaDataFlujo()
    registros = []

    df = df.drop(df[df['Fecha Vencimiento']<=fechaInicio].index) # Vamos a analizar los datos a partir de la fecha "hoy"
    dfSigno = df    #Creamos un nuevo dataframe
    dfSigno.loc[dfSigno['Tipo'] == 'Compra', 'Importe'] *= -1 # Cambiamos el signo a las compras

    # Hacemos "cero" los valores que ya estén cobrados
    dfSigno.loc[((dfSigno['Pago Emit. Recibido'] == False) & (dfSigno['Tipo'] == 'Venta')) , 'Importe'] *= 0


    df_grouped = dfSigno.groupby('Fecha Vencimiento')['Importe'].sum()  # Sumamos todos los valores de cada día
    df_grouped=df_grouped.round(2) # Redondeamos a 2 decimales para no tener problemas

    dfFechas = dfSigno['Fecha Vencimiento'].unique()

    # Partimos de la tesoreria de los bancos
    df_bancos = ConsultasDB.consultaBancos()
    tesoreria = df_bancos['Cash'].sum()
    
    for i in range (0,len(dfFechas)):
        tesoreria += df_grouped[i]
        registros.append([dfFechas[i],round(tesoreria,2),df_grouped[i]])

    dfAgregado = pd.DataFrame(registros,columns=['Fecha Vencimiento','Importe','unico'])
    dfAgregado.to_csv('datos/agregadofinalDisponible.csv',index=None)

    return dfAgregado
