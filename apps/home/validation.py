from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, DateField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class GestoresForm(FlaskForm):
    Nombre = StringField('Nombre', validators=[DataRequired(), Length(max=60)])
    Apellidos = StringField('Apellidos', validators=[DataRequired(), Length(max=60)])
    DNI = StringField('DNI', validators=[DataRequired(), Length(max=9)])
    Zona_Geo = StringField('Zona_Geo', validators=[Length(max=60)])

class ClientesForm(FlaskForm):
    CIF = StringField('CIF', validators=[DataRequired(), Length(max=9)])
    Nombre = StringField('Nombre', validators=[DataRequired(), Length(max=60)])
    Direccion = StringField('Direccion', validators=[Length(max=60)])
    Telefono = StringField('Telefono', validators=[Optional()])
    Tipo_Cliente = StringField('Tipo_Cliente', validators=[Length(max=20)])

class ProyectosForm(FlaskForm):
    Nombre = StringField('Nombre', validators=[DataRequired(), Length(max=60)])
    Direccion = StringField('Direccion', validators=[DataRequired(), Length(max=60)])
    Descripcion = StringField('Descripcion', validators=[DataRequired(), Length(max=60)])
    id_Cliente = IntegerField('id_Cliente', validators=[DataRequired()])
    id_Gestor = IntegerField('id_Gestor', validators=[DataRequired()])

class ProveedoresForm(FlaskForm):
    CIF = StringField('CIF', validators=[DataRequired(), Length(max=9)])
    Nombre = StringField('Nombre', validators=[DataRequired(), Length(max=60)])
    Direccion = StringField('Direccion', validators=[Length(max=60)])
    Telefono = StringField('Telefono', validators=[Optional()])
    Tipo_Proveedor = StringField('Tipo_Proveedor', validators=[DataRequired(), Length(max=20)])

class BancosForm(FlaskForm):
    Num_Cuenta = StringField('Num_Cuenta', validators=[DataRequired(), Length(max=24)])
    Banco = StringField('Banco', validators=[DataRequired(), Length(max=60)])
    Cash = FloatField('Cash', validators=[Optional()])
    Linea_max_confirming = FloatField('Linea_max_confirming', validators=[Optional()])


class RegistrosForm(FlaskForm):
    id_Proyecto = IntegerField('id_Proyecto', validators=[DataRequired()])
    id_Proveedor = IntegerField('id_Proveedor', validators=[Optional()])
    id_Cliente = IntegerField('id_Cliente', validators=[Optional()])
    Concepto = StringField('Concepto', validators=[DataRequired(), Length(max=60)])
    Tipo = StringField('Tipo', validators=[DataRequired(), Length(max=10)])
    Importe = FloatField('Importe', validators=[DataRequired()])
    Tipo_Pago = StringField('Tipo_Pago', validators=[DataRequired(), Length(max=10)])
    Fecha_Factura = DateField('Fecha_Factura', validators=[DataRequired()])
    Fecha_Vencimiento = DateField('Fecha_Vencimiento', validators=[DataRequired()])
    id_Banco = IntegerField('id_Banco', validators=[DataRequired()])
    Fact_Emit_Recib = BooleanField('Fact_Emit_Recib', validators=[DataRequired()])
    Pago_Emit_Recib = BooleanField('Pago_Emit_Recib', validators=[DataRequired()])