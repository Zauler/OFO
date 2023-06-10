# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps.config import *
from apps.home import blueprint
from apps.home.models import *
from sqlalchemy.orm import Session
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound


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

    registros = Registros.query.select_from(Registros)
    for registro in registros:
        if registro.proveedor != None:
            print(f"{registro.id_Registro} - {registro.proyecto.Nombre} - {registro.proveedor.Nombre}")

    # print("N REGISTROS: ", registros.count())
    # print(type(registros))

    #print(f"El gestor es: {gestor.Nombre}")
    #print(registros.Concepto)
    #print(dir(gestor.query))

    # proyecto = Proyectos.query.get(1)
    # print(f"Proyecto: {proyecto.Nombre}")
    # gestor_asignado = proyecto.gestor
    # print(f"Gestor del Proyecto: {gestor_asignado.Nombre}")




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
