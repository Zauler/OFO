# -*- encoding: utf-8 -*-

from apps import db
from sqlalchemy import CheckConstraint


class Gestores(db.Model):
    __tablename__ = 'Gestores'
    id_Gestor = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(60), nullable=False)
    Apellidos = db.Column(db.String(60), nullable=False)
    DNI = db.Column(db.String(9), unique=True, nullable=False)
    Zona_Geo = db.Column(db.String(60))

class Clientes(db.Model):
    __tablename__ = 'Clientes'
    id_Cliente = db.Column(db.Integer, primary_key=True)
    CIF = db.Column(db.String(9), unique=True, nullable=False)
    Nombre = db.Column(db.String(60), nullable=False)
    Direccion = db.Column(db.String(60))
    Telefono = db.Column(db.Numeric)
    Tipo_Cliente = db.Column(db.String(20))

class Proyectos(db.Model):
    __tablename__ = 'Proyectos'
    id_Proyecto = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(60), nullable=False)
    Direccion = db.Column(db.String(60), nullable=False)
    Descripcion = db.Column(db.String(60), nullable=False)
    id_Cliente = db.Column(db.Integer, db.ForeignKey('Clientes.id_Cliente'), nullable=False)
    id_Gestor = db.Column(db.Integer, db.ForeignKey('Gestores.id_Gestor'), nullable=False)
    cliente = db.relationship('Clientes')
    gestor = db.relationship('Gestores')

class Proveedores(db.Model):
    __tablename__ = 'Proveedores'
    id_Proveedor = db.Column(db.Integer, primary_key=True)
    CIF = db.Column(db.String(9), unique=True, nullable=False)
    Nombre = db.Column(db.String(60), nullable=False)
    Direccion = db.Column(db.String(60))
    Telefono = db.Column(db.Numeric)
    Tipo_Proveedor = db.Column(db.String(20), nullable=False)

class Bancos(db.Model):
    __tablename__ = 'Bancos'
    id_Banco = db.Column(db.Integer, primary_key=True)
    Num_Cuenta = db.Column(db.String(24), unique=True, nullable=False)
    Banco = db.Column(db.String(60), nullable=False)
    Cash = db.Column(db.Float)
    Linea_max_confirming = db.Column(db.Float)

class Registros(db.Model):
    __tablename__ = 'Registros'
    id_Registro = db.Column(db.Integer, primary_key=True)
    id_Proyecto = db.Column(db.Integer, db.ForeignKey('Proyectos.id_Proyecto'), nullable=False)
    id_Proveedor = db.Column(db.Integer, db.ForeignKey('Proveedores.id_Proveedor'))
    id_Cliente = db.Column(db.Integer, db.ForeignKey('Clientes.id_Cliente'))
    Concepto = db.Column(db.String(60), nullable=False)
    Tipo = db.Column(db.String(10), nullable=False)
    Importe = db.Column(db.Float, nullable=False)
    Tipo_Pago = db.Column(db.String(10), nullable=False)
    Fecha_Factura = db.Column(db.Date, nullable=False)
    Fecha_Vencimiento = db.Column(db.Date, nullable=False)
    id_Banco = db.Column(db.Integer, db.ForeignKey('Bancos.id_Banco'), nullable=False)
    Fact_Emit_Recib = db.Column(db.Boolean, nullable=False)
    Pago_Emit_Recib = db.Column(db.Boolean, nullable=False)
    proyecto = db.relationship('Proyectos')
    banco = db.relationship('Bancos')
    proveedor = db.relationship('Proveedores')
    cliente = db.relationship('Clientes')

    __table_args__ = (
        CheckConstraint(
            '(id_Proveedor IS NULL AND id_Cliente IS NOT NULL) OR (id_Proveedor IS NOT NULL AND id_Cliente IS NULL)',
            name='check_proveedor_cliente'
        ),
    )

