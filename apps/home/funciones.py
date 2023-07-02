import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.home.consultasDB import *


# CALCULA LA CUANTIA DE TESORERIA POR MESES EN CADA BANCO
def calculaTesoreria(meses):
    nombre_meses = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]
    hoy = datetime.today()
    mesActual = datetime.today().month
    list_meses = [] # Serán los meses que estamos analizando (enero, febrero, marzo, etc.)

    df = ConsultasDB.consultaRegistros()
    df['Fecha Vencimiento'] = pd.to_datetime(df['Fecha Vencimiento'])
    df = df.drop(df[df['Fecha Vencimiento']<=hoy].index)
    dfTrans = df.loc[df["Tipo Pago"]=="TRANSFERENCIA"]
    dfConfir = df.loc[df["Tipo Pago"]=="CONFIRMING"]

    dfBancos = ConsultasDB.consultaBancos()

    # TESORERIA
    dictMes = {}
    dictTeso = {}
    dictTesoDispo = {}

    # Tesoreria Inicial que tenemos el día que estamos haciendo la consulta
    for i in range(len(dfBancos['Banco'])):
        dictMes[dfBancos.iloc[i]['Banco']] = dfBancos.iloc[i]['Cash']

    for j in range(0,meses): #VAMOS A RECORRER TODOS LOS MESES
        bbva = dictMes['BBVA']
        cajamar = dictMes['CAJAMAR']
        caixa = dictMes['CAIXA']
        sabadell = dictMes['SABADELL']
        ibercaja = dictMes['IBERCAJA']
        cajarural = dictMes['CAJARURAL']
        santander = dictMes['SANTANDER']

        # VAMOS A AÑADIR EL ESTADO ACTUAL "HOY" DE LA TESORERIA. j=0 -> estado actual se refiere al estado el día que se está realizando la consulta
        if j == 0:
                dictTeso[j]=dictMes

        else:
            # CALCULAMOS LOS VALORES DE LAS TRANSFERENCIAS
            for i in range(len(dfTrans)):  
                fechaVenc = dfTrans.iloc[i]["Fecha Vencimiento"]

                if  (dfTrans.iloc[i]["Pago Emit. Recibido"] == True) and (fechaVenc < (hoy + relativedelta(months=j))):
                    if dfTrans.iloc[i]["Tipo"] == "Compra": # MODELO COMPRAS
                        if dfTrans.iloc[i]["Banco"] == "BBVA":
                            bbva -= float(dfTrans.iloc[i]["Importe"])
                        elif dfTrans.iloc[i]["Banco"] == "CAJAMAR":
                            cajamar -= float(dfTrans.iloc[i]["Importe"])
                        elif dfTrans.iloc[i]["Banco"] == "CAIXA":
                            caixa -= float(dfTrans.iloc[i]["Importe"])
                        elif dfTrans.iloc[i]["Banco"] == "SABADELL":
                            sabadell -= float(dfTrans.iloc[i]["Importe"])
                        elif dfTrans.iloc[i]["Banco"] == "IBERCAJA":
                            ibercaja -= float(dfTrans.iloc[i]["Importe"])
                        elif dfTrans.iloc[i]["Banco"] == "CAJARURAL":
                            cajarural -= float(dfTrans.iloc[i]["Importe"])
                        elif dfTrans.iloc[i]["Banco"] == "SANTANDER":
                            santander -= float(dfTrans.iloc[i]["Importe"])
                    else: # MODELO VENTAS
                        if dfTrans.iloc[i]["Banco"] == "BBVA":
                            bbva += float(dfTrans.iloc[i]["Importe"])
                        elif dfTrans.iloc[i]["Banco"] == "CAJAMAR":
                            cajamar += float(dfTrans.iloc[i]["Importe"])
                        elif dfTrans.iloc[i]["Banco"] == "CAIXA":
                            caixa += dfTrans.iloc[i]["Importe"]
                        elif dfTrans.iloc[i]["Banco"] == "SABADELL":
                            sabadell += dfTrans.iloc[i]["Importe"]
                        elif dfTrans.iloc[i]["Banco"] == "IBERCAJA":
                            ibercaja += float(dfTrans.iloc[i]["Importe"])
                        elif dfTrans.iloc[i]["Banco"] == "CAJARURAL":
                            cajarural += float(dfTrans.iloc[i]["Importe"])
                        elif dfTrans.iloc[i]["Banco"] == "SANTANDER":
                            santander += float(dfTrans.iloc[i]["Importe"])

            # Agregamos los valores de ese mes al diccionario
            dictTeso[j]={"BBVA":round(bbva,2), "CAJAMAR":round(cajamar,2), "CAIXA":round(caixa,2), "SABADELL":round(sabadell,2),
                        "IBERCAJA":round(ibercaja,2), "CAJARURAL":round(cajarural,2), "SANTANDER":round(santander,2)}


        # VAMOS A CALCULAR LAS FACTURAS EMITIDAS DE VENTA QUE SON CONFIRMING PARA SABER LO QUE HABRÍA DISPONIBLE CADA MES
        bbva_disponible = 0
        cajamar_disponible = 0
        caixa_disponible = 0
        sabadell_disponible = 0
        ibercaja_disponible = 0
        cajarural_disponible = 0
        santander_disponible = 0

        for i in range(len(dfConfir)):
            fechaVenc = dfConfir.iloc[i]["Fecha Vencimiento"]

            # CALCULAMOS EL DISPONIBLE RESTO DE MESES 0,1,2,3,4
            if (fechaVenc > (hoy + relativedelta(months=j))) and (dfConfir.iloc[i]["Pago Emit. Recibido"] == True):
                if dfConfir.iloc[i]["Tipo"] == "Venta": # MODELO FACT. EMITIDAS
                    if dfConfir.iloc[i]["Banco"] == "BBVA":
                        bbva_disponible += float(dfConfir.iloc[i]["Importe"])
                    elif dfConfir.iloc[i]["Banco"] == "CAJAMAR":
                        cajamar_disponible += float(dfConfir.iloc[i]["Importe"])
                    elif dfConfir.iloc[i]["Banco"] == "CAIXA":
                        caixa_disponible += float(dfConfir.iloc[i]["Importe"])
                    elif dfConfir.iloc[i]["Banco"] == "SABADELL":
                        sabadell_disponible += dfConfir.iloc[i]["Importe"]
                    elif dfConfir.iloc[i]["Banco"] == "IBERCAJA":
                        ibercaja_disponible += float(dfConfir.iloc[i]["Importe"])
                    elif dfConfir.iloc[i]["Banco"] == "CAJARURAL":
                        cajarural_disponible += float(dfConfir.iloc[i]["Importe"])
                    elif dfConfir.iloc[i]["Banco"] == "SANTANDER":
                        santander_disponible += float(dfConfir.iloc[i]["Importe"])
        
        # AÑADIMOS EL DISPONIBLE A FECHA DE "HOY"
        dictTesoDispo[j]={"BBVA":round(bbva_disponible,2), "CAJAMAR":round(cajamar_disponible,2), "CAIXA":round(caixa_disponible,2),
                        "SABADELL":round(sabadell_disponible,2), "IBERCAJA":round(ibercaja_disponible,2),
                        "CAJARURAL":round(cajarural_disponible,2), "SANTANDER":round(santander_disponible,2)}
        

        if (mesActual + j) > 12:    #Si el valor se pasa de 12 volvemos a 1 para empezar otra vez por enero
            indice = ((mesActual + j)-12)-1
        else:
            indice = (mesActual + j)-1
        list_meses.append(f"{nombre_meses[indice]}")


    return dictTeso, dictTesoDispo, list_meses


# CALCULA EL VALOR DE LOS CONFIRMING POR MESES EN TODOS LOS BANCOS
def calculaConfirming(meses):
    hoy =datetime.today()
    df = ConsultasDB.consultaRegistros()
    df['Fecha Vencimiento'] = pd.to_datetime(df['Fecha Vencimiento'])
    df['Fecha Factura'] = pd.to_datetime(df['Fecha Factura'])
    df = df.drop(df[df['Fecha Vencimiento']<=hoy].index)
    dfConf = df.loc[df["Tipo Pago"]=="CONFIRMING"]
    dfBancos = ConsultasDB.consultaBancos()

    dictLineaConfirming = {}

    # Línea de Confirming que tenemos concedida por la entidad bancaria
    for i in range(len(dfBancos['Banco'])):
        dictLineaConfirming[dfBancos.iloc[i]['Banco']] = dfBancos.iloc[i]['Linea_max_confirming']

    dictConfir = {}


    for j in range(0,meses):    #VAMOS A RECORRER TODOS LOS MESES
        bbva = dictLineaConfirming["BBVA"]
        cajamar = dictLineaConfirming["CAJAMAR"]
        caixa = dictLineaConfirming["CAIXA"]
        sabadell = dictLineaConfirming["SABADELL"]
        ibercaja = dictLineaConfirming["IBERCAJA"]
        cajarural = dictLineaConfirming["CAJARURAL"]
        santander = dictLineaConfirming["SANTANDER"]


        for i in range(len(dfConf)):
            fecha = dfConf.iloc[i]["Fecha Vencimiento"]
            fechaFact = dfConf.iloc[i]["Fecha Factura"]

            if dfConf.iloc[i]["Tipo"] == "Compra":
                if (fecha > (hoy + relativedelta(months=j))) and fechaFact <= (hoy + relativedelta(months=j)):
                    if dfConf.iloc[i]["Banco"] == "BBVA":
                        bbva -= float(dfConf.iloc[i]["Importe"])
                    elif dfConf.iloc[i]["Banco"] == "CAJAMAR":
                        cajamar -= float(dfConf.iloc[i]["Importe"])
                    elif dfConf.iloc[i]["Banco"] == "CAIXA":
                        caixa -= float(dfConf.iloc[i]["Importe"])
                    elif dfConf.iloc[i]["Banco"] == "SABADELL":
                        sabadell -= float(dfConf.iloc[i]["Importe"])
                    elif dfConf.iloc[i]["Banco"] == "IBERCAJA":
                        ibercaja -= float(dfConf.iloc[i]["Importe"])
                    elif dfConf.iloc[i]["Banco"] == "CAJARURAL":
                        cajarural -= float(dfConf.iloc[i]["Importe"])
                    elif dfConf.iloc[i]["Banco"] == "SANTANDER":
                        santander -= float(dfConf.iloc[i]["Importe"])
            
        # Agregamos los valores de ese mes al diccionario
        dictConfir[j]={"BBVA":round(bbva,2), "CAJAMAR":round(cajamar,2), "CAIXA":round(caixa,2), "SABADELL":round(sabadell,2),
                    "IBERCAJA":round(ibercaja,2), "CAJARURAL":round(cajarural,2), "SANTANDER":round(santander,2)}


    return dictConfir
    

def calFecha(fecha, meses=0):
   dia = datetime.strptime(fecha, '%Y-%m-%d')
   return (dia + relativedelta(months=meses))