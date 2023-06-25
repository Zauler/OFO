# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import pandas as pd

from apps import db
from apps.config import *
from apps.home import blueprint
from apps.home.models import *
from sqlalchemy import join
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from flask import render_template, redirect, url_for, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from datetime import datetime
from apps.home.consultasDB import *
from apps.home.validation import *



@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500



@blueprint.route('/table.html', methods=('GET', 'POST', 'PUT'))
@login_required
def table():
    
    # METODO POST
    if request.method == 'POST':
        proyecto = request.form['proyecto']
        proveedor = request.form['proveedor']
        cliente = ""
        concepto = request.form['concepto']
        importe = request.form['importe']
        modalidad = request.form['tipo']
        tipoPago = request.form['tipoPago']
        fecha_fact = request.form['fechaFactura']
        banco = request.form['entidad']
        gestor = request.form['gestor']

    # Le cambiamos el formato a la fecha de factura para aparezca como YYYY-MM-DD
        ano,mes,dia = fecha_fact.split("-")
        fecha_fact = (f"{ano}/{mes}/{dia}")

        if modalidad == "Compra":
            fecha_venc = request.form['fechaVencimiento']
            ano,mes,dia = fecha_venc.split("-")
            fecha_venc = (f"{ano}/{mes}/{dia}")
            cliente = ""
        else:
            fecha_venc = request.form['fechaVencimientoDate']
            ano,mes,dia = fecha_venc.split("-")
            fecha_venc = (f"{ano}/{mes}/{dia}")
            cliente = proveedor
            proveedor = ""
        
        lista_datos = [proyecto,proveedor,cliente,concepto,modalidad,importe,tipoPago,fecha_fact,fecha_venc,banco,gestor,'False',False]  # Los 2 últimos "False" corresponden a los checkbox

        # with open('datos/pedidos.csv', 'a', newline='', encoding='utf-8') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(lista_datos)


    # METODO PUT
    if request.method == 'PUT':
        respuesta = request.get_json()

        if len(respuesta) == 3: # SI LA RESPUESTA QUE RECIBIMOS SOLO TIENE 3 PARÁMETROS
            indice = (respuesta['indice'])
            estado = (respuesta['estado'])
            tipo = (respuesta['tipo'])

            #MODIFICAR VALOR DE UN CHECBOX
            if tipo == "cobrado":   # Si es un checkbox de cobrado
                dfTemporal = pd.read_csv('datos/pedidos.csv')
                dfTemporal.iloc[indice,11] = estado
                dfTemporal.to_csv('datos/pedidos.csv',index=False)
            elif tipo == "pagoEmitido":   # Si es un checkbox de cobrado
                dfTemporal = pd.read_csv('datos/pedidos.csv')
                dfTemporal.iloc[indice,12] = estado
                dfTemporal.to_csv('datos/pedidos.csv',index=False)
                

        elif len(respuesta) == 11:  # MODIFICAR UN REGISTRO
            indiceM = (respuesta[0]) + 1 # para que coincida con el indice de la base de datos
            proyectoM = (respuesta[1])
            tipoM = (respuesta[2])
            proveedorM = (respuesta[3])
            conceptoM = (respuesta[4])
            importeM = float((respuesta[5]))
            fechaF = (respuesta[6])
            tipoPagoM = (respuesta[7])
            fechaV = (respuesta[8])
            entidadM = (respuesta[9])
            gestorM = (respuesta[10])

            # Comprobamos si es compra o venta para rellenar el cliente o el proveedor
            if tipoM == "Compra":
                proveedorM = proveedorM
                clienteM = ""
            else:
                clienteM = proveedorM
                proveedorM = ""

            # Actualizamos el registro del pedido seleccionado
            datos = {"id_Proyecto": proyectoM, "id_Proveedor": proveedorM, "id_Cliente": clienteM, "Concepto": conceptoM, "Tipo": tipoM,
                    "Importe": importeM, "Tipo_Pago": tipoPagoM, "Fecha_Factura": fechaF, "Fecha_Vencimiento": fechaV, "id_Banco": entidadM, "gestor": gestorM}
            
            ConsultasDB.modificarRegistro(indiceM,datos)


        elif len(respuesta) == 1:   # ELIMINAR UN REGISTRO
            indiceM = int(respuesta['indice']) + 1  # para que coincida con el indice de la base de datos
            ConsultasDB.eliminarRegistro(indiceM)


    # METODO GET            
    df = ConsultasDB.consultaRegistros().drop('id_Registro',axis=1)
    dfProveedores = ConsultasDB.consultaProveedores()
    dfBancos = ConsultasDB.consultaBancos()
    dfClientes = ConsultasDB.consultaClientes()
    dfProyectos = ConsultasDB.consultaProyectos()
    dfGestores = ConsultasDB.consultaGestores()
    dfGestores["NombreGestor"] = dfGestores["Nombre"] + " " + dfGestores["Apellidos"]


    # Convertimos el dataframe en una lista para pasarlo al template donde lo recogerá javascript
    lista_condiciones_proveedores = (dfProveedores['Condiciones_confirming'].values).tolist()
    clientes = dfClientes[['Nombre']].to_dict(orient='dict')
    listaProyectos = dfProyectos['Nombre'].to_dict()
    proveedores = dfProveedores[['Nombre']].to_dict(orient='dict')
    bancos = dfBancos['Banco'].to_dict()
    gestores = dfGestores['NombreGestor'].to_dict()
    
    return render_template("home/table.html", segment='table', tables=[df.to_html(header=True, classes='table table-hover table-striped table-bordered',
                table_id="tabla_registros", index=True)],
                proveedores = proveedores, 
                bancos = bancos,
                condicionesProve=lista_condiciones_proveedores,
                listaProyectos = listaProyectos,
                listaContact=clientes, gestores = gestores)


# @app.route('/registrar_r', methods=['POST'])

# def registrar():
#     form = RegistrosForm(request.form)

#     if form.validate_on_submit():
#         nuevo_registro = Registros(
#             id_Proyecto = form.id_Proyecto.data,
#             id_Proveedor = form.id_Proveedor.data,
#             id_Cliente = form.id_Cliente.data,
#             Concepto = form.Concepto.data,
#             Tipo = form.Tipo.data,
#             Importe = form.Importe.data,
#             Tipo_Pago = form.Tipo_Pago.data,
#             Fecha_Factura = form.Fecha_Factura.data,
#             Fecha_Vencimiento = form.Fecha_Vencimiento.data,
#             id_Banco = form.id_Banco.data,
#             Fact_Emit_Recib = form.Fact_Emit_Recib.data,
#             Pago_Emit_Recib = form.Pago_Emit_Recib.data
#         )

#         try:
#             db.session.add(nuevo_registro)
#             db.session.commit()
#             return redirect(url_for('home_blueprint.table'))  # redirige al usuario a la página principal después de registrar
        
#         except SQLAlchemyError as e:
            
#             db.session.rollback()
#             return f'Error en la base de datos: {str(e)}'  # si ocurre un error en la base de datos, devuelve este error
        
#     else:
#         return 'Error en el formulario'  # si el formulario no es válido, devuelve este error




# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
