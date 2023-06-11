# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import pandas as pd

from apps import db
from apps.config import *
from apps.home import blueprint
from apps.home.models import *
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from datetime import datetime


@blueprint.route('/index')
@login_required
def index():
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


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
