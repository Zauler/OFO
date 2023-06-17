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
        
    # queryClientes = db.session.query(Registros.id_Registro, Proyectos.Nombre, Clientes.Nombre,
    #                          Registros.Concepto, Registros.Tipo, Registros.Importe,
    #                           Registros.Tipo_Pago, Registros.Fecha_Factura, Registros.Fecha_Vencimiento,
    #                            Bancos.Banco, Registros.Fact_Emit_Recib,
    #                            Registros.Pago_Emit_Recib, Gestores.Nombre).select_from(Registros).join(Clientes,
    #                            Registros.id_Cliente == Clientes.id_Cliente).join(Proyectos,
    #                             Registros.id_Proyecto == Proyectos.id_Proyecto).join(Bancos,
    #                             Registros.id_Banco == Bancos.id_Banco).join(Gestores,
    #                             Proyectos.id_Gestor == Gestores.id_Gestor)
    
    # queryProveedores = db.session.query(Registros.id_Registro, Proyectos.Nombre, Proveedores.Nombre,
    #                         Registros.Concepto, Registros.Tipo, Registros.Importe,
    #                         Registros.Tipo_Pago, Registros.Fecha_Factura, Registros.Fecha_Vencimiento,
    #                         Bancos.Banco, Registros.Fact_Emit_Recib,
    #                         Registros.Pago_Emit_Recib, Gestores.Nombre).select_from(Registros).join(Proveedores,
    #                         Registros.id_Proveedor == Proveedores.id_Proveedor).join(Proyectos,
    #                         Registros.id_Proyecto == Proyectos.id_Proyecto).join(Bancos,
    #                         Registros.id_Banco == Bancos.id_Banco).join(Gestores,
    #                         Proyectos.id_Gestor == Gestores.id_Gestor)
    
    # queryPrueba = db.session.query(Registros.id_Registro, Registros.Concepto, Registros.Tipo,
    #                                 Registros.Importe,Registros.Fecha_Factura, Registros.Fecha_Vencimiento,
    #                                 Registros.Fact_Emit_Recib,Registros.Pago_Emit_Recib)
    # columnas_fecha = ["Fecha_Factura", "Fecha_Vencimiento"]
    # dfPrueba = pd.read_sql(queryPrueba.statement, db.session.bind, parse_dates=columnas_fecha)
    
    # dfClientes = pd.read_sql(queryClientes.statement, db.session.bind) 
    # dfProveedores = pd.read_sql(queryProveedores.statement, db.session.bind)
    
    # df = pd.concat([dfClientes, dfProveedores], ignore_index=True)
    # df.sort_values(by="id_Registro",ignore_index=True,inplace=True)
    
    # columnas=[
    #     'id_Registro', 'Proyecto', 'Proveedor', 'Concepto', 'Tipo', 'Importe', 'Tipo_Pago', 'Fecha_Factura', 'Fecha_Vencimiento', 'Banco',
    #     'Fact_Emit_Recib', 'Pago_Emit_Recib', 'Gestor']
    
    # df.columns = columnas
    # df.to_csv("datos/df.csv", sep=";", index=False)

    
    # sesion = Session()

    # query = sesion.query(Registros).all

    # gestor = Gestores.query.filter_by(Nombre="Federico").first()
    #registros = Registros.query.get(5)
    #print(f"Concepto de Registro: {registros.Concepto}")
    # banco_asignado = registros.banco
    # print(f"Banco del Registro: {banco_asignado.Banco}")


    # motor = Config.SQLALCHEMY_DATABASE_URI
    # print(type(motor))

   # registros = Registros.query.select_from(Registros)
   # for registro in registros:
   #     if registro.proveedor != None:
   #         print(f"{registro.id_Registro} - {registro.proyecto.Nombre} - {registro.proveedor.Nombre}")

    # print("N REGISTROS: ", registros.count())
    # print(type(registros))

    #print(f"El gestor es: {gestor.Nombre}")
    #print(registros.Concepto)
    #print(dir(gestor.query))

    # proyecto = Proyectos.query.get(1)
    # print(f"Proyecto: {proyecto.Nombre}")
    # gestor_asignado = proyecto.gestor
    # print(f"Gestor del Proyecto: {gestor_asignado.Nombre}")



    #---------------CONSULTAR REGISTROS----------------
    #query = db.session.query(Proyectos.id_Proyecto, Gestores.Nombre).join(Gestores)
    #df = pd.read_sql(query.statement, db.session.bind)
    #print(df.head(2))

    #query = db.session.query(Registros.id_Registro, Clientes.Nombre ,Clientes.Telefono ).join(Clientes)
    #df = pd.read_sql(query.statement, db.session.bind)
    #print(df.head(20))

    #-----------------ELIMINTAR REGISTROS------------------
#    id_del_registro_eliminar = 1
#    
#    try:
#        registro_a_eliminar = db.session.query(Registros).filter(Registros.id_Registro == id_del_registro_eliminar).first()
#
#        if registro_a_eliminar is not None:
#            db.session.delete(registro_a_eliminar)
#            db.session.commit()
#            print("Registro Eliminado: ", id_del_registro_eliminar) #Si queremos añadimos más info
#        else:
#            print("Registro no encontrado")
#
#    except SQLAlchemyError as e:
#        db.session.rollback()
#        print("Ocurrió un error al eliminar el registro: ",e)


    #-----------------MODIFICAR REGISTROS--------------------------
    #id_del_registro_modificar = 2
    
    #nueva_id_Proyecto=113 #antes 112
    #nueva_id_Proveedor=202 #Abtes 201
    #nueva_id_Cliente= None
    #nuevo_concepto=  "MANO DE OBRA"
    #nuevo_tipo="Venta" #Compra

    #Ejemplo de datos.
    #nuevo_importe=11349.8	
    #nuevo_tipo_pago="CONFIRMING"	
    #nueva_fecha_factura_str = "2022-12-24" #antes 2022-11-24
    #nueva_fecha_factura= datetime.strptime(nueva_fecha_factura_str, "%Y-%m-%d").date()
    #nueva_fecha_vencimiento_str = "2023-01-19" #antes 2023-02-19
    #nueva_fecha_vencimiento = datetime.strptime( nueva_fecha_vencimiento_str, "%Y-%m-%d").date()
    #nueva_id_banco = 1
    #nuevo_fact_emit_recib = True
    #nuevo_pago_emit_recib = True

    #nuevos_registros = {
    #"id_Proyecto": nueva_id_Proyecto,
    #"id_Proveedor": nueva_id_Proveedor,
    #"id_Cliente": nueva_id_Cliente,
    #"Concepto": nuevo_concepto,
    #"Tipo": nuevo_tipo,
    #"Importe": nuevo_importe,
    #"Tipo_Pago": nuevo_tipo_pago,
    #"Fecha_Factura": nueva_fecha_factura,
    #"Fecha_Vencimiento": nueva_fecha_vencimiento,
    #"id_Banco": nueva_id_banco,
    #"Fact_Emit_Recib": nuevo_fact_emit_recib,
    #"Pago_Emit_Recib": nuevo_pago_emit_recib,
    #}

    #try:
    #    registro_a_modificar = db.session.query(Registros).filter(Registros.id_Registro == id_del_registro_modificar).first()

    #    if registro_a_modificar is not None:
    #        for campo, nuevo_valor in nuevos_registros.items():
    #            setattr(registro_a_modificar, campo, nuevo_valor) #Esta función cambia el atributo de la clase.

    #        db.session.commit()
    #        print("Resistro modificado: " , id_del_registro_modificar)

        
    #    else:
    #        print("Registro no encontrado")
    
    #except SQLAlchemyError as e:
    #    db.session.rollback()
    #    print("Ocurrió un error al eliminar el registro: ",e)


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
    
    # # METODO POST
    # if request.method == 'POST':
    #     proyecto = request.form['proyecto']
    #     proveedor = request.form['proveedor']
    #     concepto = request.form['concepto']
    #     importe = request.form['importe']
    #     modalidad = request.form['tipo']
    #     tipoPago = request.form['tipoPago']
    #     fecha_fact = request.form['fechaFactura']
    #     banco = request.form['entidad']

    #     if modalidad == "Compra":
    #         fecha_venc = request.form['fechaVencimiento']
    #     else:
    #         fecha_venc = request.form['fechaVencimientoDate']
    #         ano,mes,dia = fecha_venc.split("-")
    #         fecha_venc = (f"{dia}/{mes}/{ano}")


    #     # Le cambiamos el formato a la fecha de factura para aparezca como DD-MM-YYYY
    #     ano,mes,dia = fecha_fact.split("-")
    #     fecha_fact = (f"{dia}/{mes}/{ano}")
        
    #     lista_datos = [proyecto,proveedor,concepto,modalidad,importe,tipoPago,fecha_fact,fecha_venc,banco,'False','False','False',False]  # Los 4 últimos "False" corresponden a los checkbox

    #     with open('datos/pedidos.csv', 'a', newline='', encoding='utf-8') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(lista_datos)


    # # METODO PUT
    # if request.method == 'PUT':
    #     respuesta = request.get_json()

    #     if len(respuesta) == 3: # SI LA RESPUESTA QUE RECIBIMOS SOLO TIENE 3 PARÁMETROS
    #         indice = (respuesta['indice'])
    #         estado = (respuesta['estado'])
    #         tipo = (respuesta['tipo'])

    #         #MODIFICAR VALOR DE UN CHECBOX
    #         if tipo == "anticipo":  # Si es un checkbox de anticipo
    #             dfTemporal = pd.read_csv('datos/pedidos.csv')
    #             dfTemporal.iloc[indice,9] = estado
    #             dfTemporal.to_csv('datos/pedidos.csv',index=False)
    #         elif tipo == "recompra":   # Si es un checkbox de cobrado
    #             dfTemporal = pd.read_csv('datos/pedidos.csv')
    #             dfTemporal.iloc[indice,10] = estado
    #             dfTemporal.to_csv('datos/pedidos.csv',index=False)
    #         elif tipo == "cobrado":   # Si es un checkbox de cobrado
    #             dfTemporal = pd.read_csv('datos/pedidos.csv')
    #             dfTemporal.iloc[indice,11] = estado
    #             dfTemporal.to_csv('datos/pedidos.csv',index=False)
    #         elif tipo == "pagoEmitido":   # Si es un checkbox de cobrado
    #             dfTemporal = pd.read_csv('datos/pedidos.csv')
    #             dfTemporal.iloc[indice,12] = estado
    #             dfTemporal.to_csv('datos/pedidos.csv',index=False)
                

    #     elif len(respuesta) == 10:  # MODIFICAR UN REGISTRO
    #         indiceM = (respuesta[0])
    #         proyectoM = (respuesta[1])
    #         tipoM = (respuesta[2])
    #         proveedorM = (respuesta[3])
    #         conceptoM = (respuesta[4])
    #         importeM = float((respuesta[5]))
    #         fechaF = (respuesta[6])
    #         tipoPagoM = (respuesta[7])
    #         fechaV = (respuesta[8])
    #         entidadM = (respuesta[9])

    #         # Actualizamos el registro del pedido seleccionado
    #         dfTemporal = pd.read_csv('datos/pedidos.csv')
    #         dfTemporal.iloc[indiceM,0] = proyectoM
    #         dfTemporal.iloc[indiceM,1] = proveedorM
    #         dfTemporal.iloc[indiceM,2] = conceptoM
    #         dfTemporal.iloc[indiceM,3] = tipoM
    #         dfTemporal.iloc[indiceM,4] = importeM
    #         dfTemporal.iloc[indiceM,5] = tipoPagoM
    #         dfTemporal.iloc[indiceM,6] = fechaF
    #         dfTemporal.iloc[indiceM,7] = fechaV
    #         dfTemporal.iloc[indiceM,8] = entidadM
    #         dfTemporal.to_csv('datos/pedidos.csv',index=False)


    #     elif len(respuesta) == 1:   # ELIMINAR UN REGISTRO
    #         indiceM = int(respuesta['indice'])
    #         dfTemporal = pd.read_csv('datos/pedidos.csv')
    #         dfTemporal.drop([indiceM], axis=0, inplace=True)
    #         dfTemporal.to_csv('datos/pedidos.csv',index=False)

    # METODO GET            
    df = ConsultasDB.consultaRegistros().drop('id_Registro',axis=1)
    dfProveedores = ConsultasDB.consultaProveedores()
    dfBancos = ConsultasDB.consultaBancos()
    dfClientes = ConsultasDB.consultaClientes()
    dfProyectos = ConsultasDB.consultaProyectos()

    # # Vamos a crear un hilo nuevo que compruebe si hay cambios en los clientes de holded y si es así que actualice el dfClientes
    # hilo1 = threading.Thread(target=fn.consultaContactos)
    # hilo1.start()

    # Convertimos el dataframe en una lista para pasarlo al template donde lo recogerá javascript
    lista_condiciones_proveedores = (dfProveedores['Condiciones_confirming'].values).tolist()
    listaContactos = (dfClientes['Nombre'].values).tolist()
    listaProveedores = (dfProveedores['Nombre'].values).tolist()
    listaProyectos = (dfProyectos['Nombre'].values).tolist()


    return render_template("home/table.html", segment='table', tables=[df.to_html(header=True, classes='table table-hover table-striped table-bordered',
                table_id="tabla_registros", index=True)],
                proveedores = dfProveedores['Nombre'].values, bancos = dfBancos['Banco'],
                condicionesProve=lista_condiciones_proveedores,
                listaProyectos = listaProyectos,
                listaContact=listaContactos, listaProve = listaProveedores)


@app.route('/registrar_r', methods=['POST'])

def registrar():
    form = RegistrosForm(request.form)

    if form.validate_on_submit():
        nuevo_registro = Registros(
            id_Proyecto = form.id_Proyecto.data,
            id_Proveedor = form.id_Proveedor.data,
            id_Cliente = form.id_Cliente.data,
            Concepto = form.Concepto.data,
            Tipo = form.Tipo.data,
            Importe = form.Importe.data,
            Tipo_Pago = form.Tipo_Pago.data,
            Fecha_Factura = form.Fecha_Factura.data,
            Fecha_Vencimiento = form.Fecha_Vencimiento.data,
            id_Banco = form.id_Banco.data,
            Fact_Emit_Recib = form.Fact_Emit_Recib.data,
            Pago_Emit_Recib = form.Pago_Emit_Recib.data
        )

        try:
            db.session.add(nuevo_registro)
            db.session.commit()
            return redirect(url_for('home_blueprint.table'))  # redirige al usuario a la página principal después de registrar
        
        except SQLAlchemyError as e:
            
            db.session.rollback()
            return f'Error en la base de datos: {str(e)}'  # si ocurre un error en la base de datos, devuelve este error
        
    else:
        return 'Error en el formulario'  # si el formulario no es válido, devuelve este error




# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
