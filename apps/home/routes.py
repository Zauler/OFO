# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import pandas as pd
import time
import pygal
import json

from pygal.style import Style
from apps import db
from apps.config import *
from apps.home import blueprint
from apps.home.models import *
from sqlalchemy import join
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from datetime import datetime
from apps.home.consultasDB import *
from apps.home.validation import *
from datetime import datetime
from apps.home.funciones import *
from apps.home.funciones2 import *
from apps.home.consultasMoneda import *
from apps.home.agente import realizar_consulta_agente

def graficoFlujoDisponible():
    custom_style = Style(colors=('#008b9e','#c7483f'))

    dfFlujo = creaDFTesoAgregadaDisponible()
    dfFlujoPrevi = creaDFTesoAgregadaPrevista()
    chart = pygal.Line(height=300, legend_at_bottom=True, x_label_rotation=90,dots_size=0.4,fill=True, show_minor_x_labels=False,
                        x_labels_major_count=20, style=custom_style)
    chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), dfFlujo['Fecha Vencimiento'])
    chart.add('Previsible',dfFlujoPrevi['Importe'].tolist())
    chart.add('Disponible',dfFlujo['Importe'].tolist())
    chart.render_to_file(f'apps/static/assets/img/bar_chart_flujo_disponible.svg')
    img_url = f'static/assets/img/bar_chart_flujo_disponible.svg?cache=' + str(time.time())   # Lo usamos para que no exista problemas con las cookies

    return img_url

def grafico(meses,listMeses):
    df = pd.DataFrame(calculaConfirming(meses))
    df.columns = listMeses
    custom_style = Style(colors=('#c7483f', '#008b9e', '#179bd7', '#be9717','#662f01','#007a53','#ea1d25'))

    chart = pygal.Bar(height=300, legend_at_bottom=True, style=custom_style)
    #chart.title = 'FLUJO DE CAJA: CONFIRMING'
    chart.x_labels = df.columns.values
    for i in range(len(df)):
        chart.add(df.iloc[i].name, df.iloc[i].values, rounded_bars=4)


    chart.render_to_file(f'apps/static/assets/img/bar_chart_bar_chart_Confirming.svg')
    img_url = f'static/assets/img/bar_chart_Confirming.svg?cache=' + str(time.time())   # Lo usamos para que no exista problemas con las cookies

    return img_url


@blueprint.route('/index', methods=('GET', 'POST', 'PUT'))
@login_required
def index():

    df = ConsultasDB.consultaRegistros()
    print(df.head())
    meses = 5   # Son los meses a analizar en las gráficas
    dictConfir = calculaConfirming(meses)
    dictTeso, dictTesoDis, listMeses = calculaTesoreria(meses)
    dfBancos = ConsultasDB.consultaBancos()
    dfLineaConfirming = dfBancos['Linea_max_Confirming'] # Es el crédito actual de las líneas de confirming que tenemos concedido
    dfLineaConfirming = dfLineaConfirming.to_json()
    image_url_conf = grafico(meses,listMeses)
    image_url_flujo_Disponible = graficoFlujoDisponible()
    valorMonedas = Monedas.consulta_api()


         # METODO PUT
    if request.method == 'PUT':
        respuesta = request.get_json()
        if respuesta:
            print(respuesta['question'])
            pregunta = respuesta['question']
            pregunta_respondida=realizar_consulta_agente(pregunta,df)
            print(pregunta_respondida)
            return jsonify({'status': pregunta_respondida}), 200
        else:
            return jsonify({'status': 'error', 'message': 'No data received'}), 400

    return render_template('home/index.html', segment='index', image_url_flujo = image_url_flujo_Disponible, listConfirming = dfLineaConfirming, dictTeso = dictTeso,
                           dictTesoDis = dictTesoDis, dictConfir = dictConfir, listMeses = listMeses, image_url_config = image_url_conf,
                           datosConsultaMonedas=valorMonedas)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    valorMonedas = Monedas.consulta_api()

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, datosConsultaMonedas=valorMonedas)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500



@blueprint.route('/table.html', methods=('GET', 'POST', 'PUT'))
@login_required
def table():
    
    # METODO PUT
    if request.method == 'PUT':
        respuesta = request.get_json()

        if len(respuesta) == 3: # SI LA RESPUESTA QUE RECIBIMOS SOLO TIENE 3 PARÁMETROS
            indice = (respuesta['indice'] ) # para que coincida con el indice de la base de datos
            estado = (respuesta['estado'])
            tipo = (respuesta['tipo'])
            print(indice,estado,tipo)

            #MODIFICAR VALOR DE UN CHECBOX
            if tipo == "cobrado":   # Si es un checkbox de cobrado
                datos = { "Fact_Emit_Recib": estado}
            elif tipo == "pagoEmitido":   # Si es un checkbox de cobrado
                datos = { "Pago_Emit_Recib": estado}
            print(datos)
            print(type(datos.values()))
            # Actualizamos el registro del pedido seleccionado
            ConsultasDB.modificarRegistro(indice,datos)
                

        elif len(respuesta) == 11:  # MODIFICAR UN REGISTRO
            indiceM = (respuesta[0])  # para que coincida con el indice de la base de datos
            proyectoM = (respuesta[1])
            tipoM = (respuesta[2])
            proveedorM = (respuesta[3])
            conceptoM = (respuesta[4])
            importeM = float((respuesta[5]))
            fechaF = (respuesta[6])
            tipoPagoM = (respuesta[7])
            fechaV = (respuesta[8])
            entidadM = (respuesta[9])
            #gestorM = (respuesta[10])

            # Convertimos los datos de string a date para que lo admita la BD
            fechaF = datetime.strptime(fechaF, '%Y-%m-%d')
            fechaV = datetime.strptime(fechaV, '%Y-%m-%d')

            # Comprobamos si es compra o venta para rellenar el cliente o el proveedor
            if tipoM == "Compra":
                proveedorM = proveedorM
                clienteM = None
            else:
                clienteM = proveedorM
                proveedorM = None

            # Actualizamos el registro del pedido seleccionado
            # datos = {"id_Proyecto": proyectoM, "id_Proveedor": proveedorM, "id_Cliente": clienteM, "Concepto": conceptoM, "Tipo": tipoM,
            #         "Importe": importeM, "Tipo_Pago": tipoPagoM, "Fecha_Factura": fechaF, "Fecha_Vencimiento": fechaV, "id_Banco": entidadM, "gestor": gestorM}
            
            datos = {"id_Proyecto":proyectoM, "id_Proveedor":proveedorM, "id_Cliente":clienteM, "Concepto": conceptoM,"Importe": importeM, "Tipo_Pago": tipoPagoM, "id_Banco": entidadM, "Fecha_Factura": fechaF, "Fecha_Vencimiento": fechaV}
            print("El índice es: ", indiceM)
            print(datos)
            ConsultasDB.modificarRegistro(indiceM,datos)


        elif len(respuesta) == 1:   # ELIMINAR UN REGISTRO
            indiceM = int(respuesta['indice'])  # para que coincida con el indice de la base de datos
            ConsultasDB.eliminarRegistro(indiceM)


    # METODO GET            
    df = ConsultasDB.consultaRegistros()
    df.set_index('id_Registro')
    dfProveedores = ConsultasDB.consultaProveedores()
    dfBancos = ConsultasDB.consultaBancos()
    dfClientes = ConsultasDB.consultaClientes()
    dfProyectos = ConsultasDB.consultaProyectos()
    dfGestores = ConsultasDB.consultaGestores()
    dfGestores["NombreGestor"] = dfGestores["Nombre"] + " " + dfGestores["Apellidos"]
    valorMonedas = Monedas.consulta_api()


    # Convertimos el dataframe en una lista para pasarlo al template donde lo recogerá javascript
    lista_condiciones_proveedores = (dfProveedores['Condiciones_confirming'].values).tolist()
    clientes = dfClientes.set_index('id_Cliente')['Nombre'].to_dict()
    listaProyectos = dfProyectos.set_index('id_Proyecto')['Nombre'].to_dict()
    proveedores = dfProveedores.set_index('id_Proveedor')['Nombre'].to_dict()
    bancos = dfBancos.set_index('id_Banco')['Banco'].to_dict()
    gestores = dfGestores.set_index('id_Gestor')['NombreGestor'].to_dict()
    form = RegistrosForm()
    return render_template("home/table.html", segment='table', tables=[df.to_html(header=True, classes='table table-hover table-striped table-bordered',
                table_id="tabla_registros", index=False)],
                proveedores = proveedores, 
                bancos = bancos,
                condicionesProve=lista_condiciones_proveedores,
                listaProyectos = listaProyectos,
                listaContact=clientes, gestores = gestores, form = form, datosConsultaMonedas=valorMonedas)


@blueprint.route('/registrar_r', methods=['POST'])
@login_required
def registrar_registros():

    form = RegistrosForm(request.form)
    print("FORMULARIO HTML")
    print(request.form)
    print("FORMULARIO VALIDACIÓN")
    print(form.data)

    if request.form["tipo"] =="Compra":
        fechavencimiento_str = request.form["fechaVencimiento"]
        fechavencimiento = datetime.strptime(fechavencimiento_str, "%d/%m/%Y")
        fechavencimiento = fechavencimiento.strftime('%Y-%m-%d')
        fechavencimiento = datetime.strptime(fechavencimiento, '%Y-%m-%d').date()
        form.fechaVencimientoDate.data = fechavencimiento
        form.cliente.data = None

    if request.form["tipo"] == "Venta":
        form.cliente.data = form.proveedor.data
        form.proveedor.data = None 


    if form.validate_on_submit():
        nuevo_registro = Registros(
            id_Proyecto = form.proyecto.data,
            id_Proveedor = form.proveedor.data,
            id_Cliente = form.cliente.data,
            Concepto = form.concepto.data,
            Tipo = form.tipo.data,
            Importe = form.importe.data,
            Tipo_Pago = form.tipoPago.data,
            Fecha_Factura = form.fechaFactura.data,
            Fecha_Vencimiento = form.fechaVencimientoDate.data,
            id_Banco = form.entidad.data,
            Fact_Emit_Recib = False,
            Pago_Emit_Recib = False,
        )

        try:
            db.session.add(nuevo_registro)
            db.session.commit()
            return redirect(url_for('home_blueprint.table'))  # redirige al usuario a la página principal después de registrar
        
        except SQLAlchemyError as e:
            
            db.session.rollback()
            return f'Error en la base de datos: {str(e)}'  # si ocurre un error en la base de datos, devuelve este error
        
    else:
        print('Errores en el formulario: ', form.errors)  # imprime los errores de validación
        return 'Error en el formulario'  # si el formulario no es válido, devuelve este error


@blueprint.route('/bancos.html', methods=('GET', 'POST', 'PUT'))
@login_required
def bancos():
    
    # METODO PUT
    if request.method == 'PUT':
        respuesta = request.get_json()
                
        if len(respuesta) == 5:  # MODIFICAR UN REGISTRO
            indiceM = (respuesta[0])  # para que coincida con el indice de la base de datos
            bancoM = (respuesta[1])
            cuentaM = (respuesta[2])
            cashM = (respuesta[3])
            confirmingM = (respuesta[4])

            datos = {"Num_cuenta":cuentaM, "Banco":bancoM, "Cash":cashM,"Linea_max_Confirming":confirmingM}

            ConsultasDBBancos.modificarRegistro(indiceM,datos)

        elif len(respuesta) == 1:   # ELIMINAR UN REGISTRO
            indiceM = int(respuesta['indice'])  # para que coincida con el indice de la base de datos
            ConsultasDBBancos.eliminarRegistro(indiceM)


    # METODO GET            
    dfBancos = ConsultasDBBancos.consultaBancosCompleta()
    dfBancos.set_index('id_Banco')
    valorMonedas = Monedas.consulta_api()

    form = BancosForm()
    return render_template("home/bancos.html", segment='bancos', tables=[dfBancos.to_html(header=True, classes='table table-hover table-striped table-bordered',
                table_id="tabla_bancos", index=False)], form = form, datosConsultaMonedas=valorMonedas)


@blueprint.route('/registrar_b', methods=['POST'])
@login_required
def registrar_bancos():

    form = BancosForm(request.form)

    if form.validate_on_submit():
        nuevo_registro = Bancos(
            Num_Cuenta = form.Num_Cuenta.data,
            Banco = form.Banco.data,
            Cash = form.Cash.data,
            Linea_max_Confirming = form.Linea_max_Confirming.data,
        )

        try:
            db.session.add(nuevo_registro)
            db.session.commit()
            return redirect(url_for('home_blueprint.bancos'))  # redirige al usuario a la página principal después de registrar
        
        except SQLAlchemyError as e:
            
            db.session.rollback()
            return f'Error en la base de datos: {str(e)}'  # si ocurre un error en la base de datos, devuelve este error
        
    else:
        print('Errores en el formulario: ', form.errors)  # imprime los errores de validación
        return 'Error en el formulario'  # si el formulario no es válido, devuelve este error


@blueprint.route('/proveedores.html', methods=('GET', 'POST', 'PUT'))
@login_required
def proveedores():
    
    # METODO PUT
    if request.method == 'PUT':
        respuesta = request.get_json()
                
        if len(respuesta) == 7:  # MODIFICAR UN REGISTRO
            indiceM = (respuesta[0])  # para que coincida con el indice de la base de datos
            CifM = (respuesta[1])
            NombreM = (respuesta[2])
            DireccionM = (respuesta[3])
            TelefonoM = (respuesta[4])
            Tipo_ProveedorM = (respuesta[5])
            Condiciones_confirmingM = (respuesta[6])

            datos = {"CIF":CifM, "Nombre":NombreM, "Direccion":DireccionM, "Tipo_Proveedor":Tipo_ProveedorM ,"Condiciones_confirming":Condiciones_confirmingM }

            # Valida el número de teléfono
            if isinstance(TelefonoM, int) and len(str(TelefonoM)) == 9:
                datos["Telefono"] = TelefonoM

            print(indiceM)
            print(datos)
            ConsultasDBProveedores.modificarRegistro(indiceM,datos)


        elif len(respuesta) == 1:   # ELIMINAR UN REGISTRO
            indiceM = int(respuesta['indice'])  # para que coincida con el indice de la base de datos
            ConsultasDBProveedores.eliminarRegistro(indiceM)


    # METODO GET            
    dfProveedores = ConsultasDBProveedores.consultaProveedoresCompleta()
    dfProveedores.set_index('id_Proveedor')
    dfProveedores['Telefono'] = dfProveedores['Telefono'].fillna(0).astype(int)
    dfProveedores['Telefono'] = dfProveedores['Telefono'].astype(int) #Forzamos tipo para lectura en página
    print(dfProveedores.dtypes)
    form = ProveedoresForm()
    valorMonedas = Monedas.consulta_api()

    return render_template("home/proveedores.html", segment='proveedores', tables=[dfProveedores.to_html(header=True, classes='table table-hover table-striped table-bordered',
                table_id="tabla_proveedores", index=False)], form = form, datosConsultaMonedas=valorMonedas)


@blueprint.route('/registrar_prove', methods=['POST'])
@login_required
def registrar_proveedores():

    form = ProveedoresForm(request.form)
    print("FORMULARIO HTML")
    print(request.form)
    print("FORMULARIO VALIDACIÓN")
    print(form.data)


    if form.validate_on_submit():
        nuevo_registro = Proveedores(
            CIF = form.CIF.data,
            Nombre = form.Nombre.data,
            Direccion = form.Direccion.data,
            Telefono = form.Telefono.data,
            Tipo_Proveedor = form.Tipo_Proveedor.data,
            Condiciones_confirming = form.Condiciones_confirming.data
        )

        try:
            db.session.add(nuevo_registro)
            db.session.commit()
            return redirect(url_for('home_blueprint.proveedores'))  # redirige al usuario a la página principal después de registrar
        
        except SQLAlchemyError as e:
            
            db.session.rollback()
            return f'Error en la base de datos: {str(e)}'  # si ocurre un error en la base de datos, devuelve este error
        
    else:
        print('Errores en el formulario: ', form.errors)  # imprime los errores de validación
        return 'Error en el formulario'  # si el formulario no es válido, devuelve este error



@blueprint.route('/proyectos.html', methods=('GET', 'POST', 'PUT'))
@login_required
def proyectos():
    
    # METODO PUT
    if request.method == 'PUT':
        respuesta = request.get_json()
                
        if len(respuesta) == 6:  # MODIFICAR UN REGISTRO
            indiceM = (respuesta[0])  # para que coincida con el indice de la base de datos
            proyectoM = (respuesta[1])
            direccionM = (respuesta[2])
            descripcionM = (respuesta[3])
            clienteM = (respuesta[4])
            gestorM = (respuesta[5])

            datos = {"Nombre":proyectoM, "Direccion":direccionM, "Descripcion":descripcionM,"id_Cliente":clienteM, "id_Gestor":gestorM}

            ConsultasDBProyectos.modificarRegistro(indiceM,datos)


        elif len(respuesta) == 1:   # ELIMINAR UN REGISTRO
            indiceM = int(respuesta['indice'])  # para que coincida con el indice de la base de datos
            ConsultasDBProyectos.eliminarRegistro(indiceM)


    # METODO GET            
    dfProyectos = ConsultasDBProyectos.consultaProyectosCompleta()
    dfProyectos.set_index('id_Proyecto')
    dfClientes = ConsultasDB.consultaClientes()
    dfGestores = ConsultasDB.consultaGestores()
    dfGestores["NombreGestor"] = dfGestores["Nombre"] + " " + dfGestores["Apellidos"]

    # Convertimos el dataframe en una lista para pasarlo al template donde lo recogerá javascript
    clientes = dfClientes.set_index('id_Cliente')['Nombre'].to_dict()
    gestores = dfGestores.set_index('id_Gestor')['NombreGestor'].to_dict()
    valorMonedas = Monedas.consulta_api()

    form = ProyectosForm()
    return render_template("home/proyectos.html", segment='proyectos', tables=[dfProyectos.to_html(header=True, classes='table table-hover table-striped table-bordered',
                table_id="tabla_proyectos", index=False)], clientes=clientes, gestores = gestores, form = form, datosConsultaMonedas=valorMonedas)


@blueprint.route('/registrar_p', methods=['POST'])
@login_required
def registrar_proyectos():

    form = ProyectosForm(request.form)
    print("FORMULARIO HTML")
    print(request.form)
    print("FORMULARIO VALIDACIÓN")
    print(form.data)

    if form.validate_on_submit():
        nuevo_registro = Proyectos(
            Nombre = form.Nombre.data,
            Direccion = form.Direccion.data,
            Descripcion = form.Descripcion.data,
            id_Cliente = form.id_Cliente.data,
            id_Gestor = form.id_Gestor.data,
        )

        try:
            db.session.add(nuevo_registro)
            db.session.commit()
            return redirect(url_for('home_blueprint.proyectos'))  # redirige al usuario a la página principal después de registrar
        
        except SQLAlchemyError as e:
            
            db.session.rollback()
            return f'Error en la base de datos: {str(e)}'  # si ocurre un error en la base de datos, devuelve este error
        
    else:
        print('Errores en el formulario: ', form.errors)  # imprime los errores de validación
        return 'Error en el formulario'  # si el formulario no es válido, devuelve este error


@blueprint.route('/clientes.html', methods=('GET', 'POST', 'PUT'))
@login_required
def clientes():
    
    # METODO PUT
    if request.method == 'PUT':
        respuesta = request.get_json()
                
        if len(respuesta) == 6:  # MODIFICAR UN REGISTRO
            indiceM = (respuesta[0])  # para que coincida con el indice de la base de datos
            CifM = (respuesta[1])
            NombreM = (respuesta[2])
            DireccionM = (respuesta[3])
            TelefonoM = (respuesta[4])
            Tipo_clienteM = (respuesta[5])


            datos = {"CIF":CifM, "Nombre":NombreM, "Direccion":DireccionM, "Tipo_Cliente":Tipo_clienteM }


            # Valida el número de teléfono
            if isinstance(TelefonoM, int) and len(str(TelefonoM)) == 9:
                datos["Telefono"] = TelefonoM

            print(indiceM)
            print(datos)
            ConsultaDBClientes.modificarRegistro(indiceM,datos)


        elif len(respuesta) == 1:   # ELIMINAR UN REGISTRO
            indiceM = int(respuesta['indice'])  # Indice de la base de datos
            ConsultaDBClientes.eliminarRegistro(indiceM)


    # METODO GET            
    dfClientes = ConsultaDBClientes.consultaClientesCompleta()
    dfClientes.set_index('id_Cliente')
    dfClientes['Telefono'] = dfClientes['Telefono'].fillna(0).astype(int)
    dfClientes['Telefono'] = dfClientes['Telefono'].astype(int) #Forzamos tipo para lectura en página
    print(dfClientes.dtypes)
    form = ClientesForm()
    valorMonedas = Monedas.consulta_api()

    return render_template("home/clientes.html", segment='clientes', tables=[dfClientes.to_html(header=True, classes='table table-hover table-striped table-bordered',
                table_id="tabla_clientes", index=False)], form = form, datosConsultaMonedas=valorMonedas)


@blueprint.route('/registrar_cliente', methods=['POST'])
@login_required
def registrar_clientes():

    form = ClientesForm(request.form)
    print("FORMULARIO HTML")
    print(request.form)
    print("FORMULARIO VALIDACIÓN")
    print(form.data)


    if form.validate_on_submit():
        nuevo_registro = Clientes(
            CIF = form.CIF.data,
            Nombre = form.Nombre.data,
            Direccion = form.Direccion.data,
            Telefono = form.Telefono.data,
            Tipo_Cliente = form.Tipo_Cliente.data,
        )

        try:
            db.session.add(nuevo_registro)
            db.session.commit()
            return redirect(url_for('home_blueprint.clientes'))  # redirige al usuario a la página principal después de registrar
        
        except SQLAlchemyError as e:
            
            db.session.rollback()
            return f'Error en la base de datos: {str(e)}'  # si ocurre un error en la base de datos, devuelve este error
        
    else:
        print('Errores en el formulario: ', form.errors)  # imprime los errores de validación
        return 'Error en el formulario'  # si el formulario no es válido, devuelve este error



@blueprint.route('/user.html', methods=('GET', 'POST', 'PUT'))
@login_required
def user():
    
    # METODO GET    
    # usuario = current_user

    # indice = usuario.id
    # username = usuario.username
    # email = usuario.email
    # nombre = usuario.Nombre
    # apellidos = usuario.Apellidos
    # direccion = usuario.Direccion
    # rol = usuario.Rol

    # datos = {"id": indice, "username":username, "email":email, "Nombre": nombre, "Apellidos": apellidos, "Direccion":direccion, "Rol": rol}

    valorMonedas = Monedas.consulta_api()

    return render_template("home/user.html", segment='user', datosConsultaMonedas=valorMonedas)


@blueprint.route('/actualizar_usuario', methods=['POST'])
@login_required
def actualizar_usuario():

    form = request.form
    print ("pulsado boton de formulario usuario")
    print(form)

    # indiceM = (form[0])  # para que coincida con el indice de la base de datos
    # usernameM = (form[1])
    # emailM = (form[2])
    # nombreM = (form[3])
    # apellidosM = (form[4])
    # direccionM = (form[5])

    # datos = {"username":usernameM, "email":emailM, "Nombre": nombreM, "Apellidos": apellidosM, "Direccion":direccionM}

    # print(indiceM)
    # print(datos)
    # ConsultasDBUsuarios.modificarRegistro(indiceM,datos)































    # @blueprint.route('/gestores.html', methods=('GET', 'POST', 'PUT'))
    # @login_required
    # def gestores():
        
    #     # METODO PUT
    #     if request.method == 'PUT':
    #         respuesta = request.get_json()
                    
    #         if len(respuesta) == 6:  # MODIFICAR UN REGISTRO
    #             indiceM = (respuesta[0])  # para que coincida con el indice de la base de datos
    #             NombreM = (respuesta[1])
    #             ApellidosM = (respuesta[3])
    #             DniM = (respuesta[4])
    #             Zona_GeoM = (respuesta[5])


    #             datos = {"Nombre":NombreM, "Apellidos":ApellidosM ,"Zona_Geo":Zona_GeoM }

    #             # Valida el DNI
    #             if validar_dni(DniM): #Función en el archivo de validaciones
    #                 datos["DNI"] = DniM

    #             print(indiceM)
    #             print(datos)
    #             ConsultaDBGestores.modificarRegistro(indiceM,datos)


    #         elif len(respuesta) == 1:   # ELIMINAR UN REGISTRO
    #             indiceM = int(respuesta['indice'])  # Indice de la base de datos
    #             ConsultaDBGestores.eliminarRegistro(indiceM)


    #     # METODO GET            
    #     dfGestores = ConsultaDBGestores.consultaCompleta()
    #     dfGestores.set_index('id_Gestor')
    #     print(dfGestores.dtypes)
    #     form = GestoresForm()
    #     valorMonedas = Monedas.consulta_api()

    #     return render_template("home/gestores.html", segment='gestores', tables=[dfGestores.to_html(header=True, classes='table table-hover table-striped table-bordered',
    #                 table_id="tabla_gestores", index=False)], form = form, datosConsultaMonedas=valorMonedas)



    # @blueprint.route('/registrar_gestor', methods=['POST'])
    # @login_required
    # def registrar_clientes():

    #     form = GestoresForm(request.form)
    #     print("FORMULARIO HTML")
    #     print(request.form)
    #     print("FORMULARIO VALIDACIÓN")
    #     print(form.data)


    #     if form.validate_on_submit():
    #         nuevo_registro = GestoresForm(
    #             Nombre = form.Nombre.data,
    #             Apellidos = form.Apellidos.data,
    #             DNI = form.DNI.data,
    #             Zona_Geo = form.Zona_Geo.data,
    #         )

    #         try:
    #             db.session.add(nuevo_registro)
    #             db.session.commit()
    #             return redirect(url_for('home_blueprint.gestores'))  # redirige al usuario a la página principal después de registrar
            
    #         except SQLAlchemyError as e:
                
    #             db.session.rollback()
    #             return f'Error en la base de datos: {str(e)}'  # si ocurre un error en la base de datos, devuelve este error
            
    #     else:
    #         print('Errores en el formulario: ', form.errors)  # imprime los errores de validación
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



