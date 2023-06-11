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
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound


@blueprint.route('/index')
@login_required
def index():
        
    queryClientes = db.session.query(Registros.id_Registro, Proyectos.Nombre, Clientes.Nombre,
                             Registros.Concepto, Registros.Tipo, Registros.Importe,
                              Registros.Tipo_Pago, Registros.Fecha_Factura, Registros.Fecha_Vencimiento,
                               Bancos.Banco, Registros.Fact_Emit_Recib,
                               Registros.Pago_Emit_Recib, Gestores.Nombre).select_from(Registros).join(Clientes,
                               Registros.id_Cliente == Clientes.id_Cliente).join(Proyectos,
                                Registros.id_Proyecto == Proyectos.id_Proyecto).join(Bancos,
                                Registros.id_Banco == Bancos.id_Banco).join(Gestores,
                                Proyectos.id_Gestor == Gestores.id_Gestor)
    
    queryProveedores = db.session.query(Registros.id_Registro, Proyectos.Nombre, Proveedores.Nombre,
                            Registros.Concepto, Registros.Tipo, Registros.Importe,
                            Registros.Tipo_Pago, Registros.Fecha_Factura, Registros.Fecha_Vencimiento,
                            Bancos.Banco, Registros.Fact_Emit_Recib,
                            Registros.Pago_Emit_Recib, Gestores.Nombre).select_from(Registros).join(Proveedores,
                            Registros.id_Proveedor == Proveedores.id_Proveedor).join(Proyectos,
                            Registros.id_Proyecto == Proyectos.id_Proyecto).join(Bancos,
                            Registros.id_Banco == Bancos.id_Banco).join(Gestores,
                            Proyectos.id_Gestor == Gestores.id_Gestor)
    
    # queryPrueba = db.session.query(Registros.id_Registro, Registros.Concepto, Registros.Tipo,
    #                                 Registros.Importe,Registros.Fecha_Factura, Registros.Fecha_Vencimiento,
    #                                 Registros.Fact_Emit_Recib,Registros.Pago_Emit_Recib)
    # columnas_fecha = ["Fecha_Factura", "Fecha_Vencimiento"]
    # dfPrueba = pd.read_sql(queryPrueba.statement, db.session.bind, parse_dates=columnas_fecha)
    
    dfClientes = pd.read_sql(queryClientes.statement, db.session.bind) 
    dfProveedores = pd.read_sql(queryProveedores.statement, db.session.bind)
    
    df = pd.concat([dfClientes, dfProveedores], ignore_index=True)
    df.sort_values(by="id_Registro",ignore_index=True,inplace=True)
    
    columnas=[
        'id_Registro', 'Proyecto', 'Proveedor', 'Concepto', 'Tipo', 'Importe', 'Tipo_Pago', 'Fecha_Factura', 'Fecha_Vencimiento', 'Banco',
        'Fact_Emit_Recib', 'Pago_Emit_Recib', 'Gestor']
    
    df.columns = columnas
    df.to_csv("datos/df.csv", sep=";", index=False)

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
