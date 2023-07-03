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
    Linea_max_Confirming = FloatField('Linea_max_Confirming', validators=[Optional()])


class RegistrosForm(FlaskForm):
    proyecto = IntegerField('proyecto', validators=[DataRequired()])
    proveedor = IntegerField('proveedor', validators=[Optional()])
    cliente = IntegerField('cliente', validators=[Optional()])
    concepto = StringField('concepto', validators=[DataRequired(), Length(max=60)])
    tipo = StringField('tipo', validators=[DataRequired(), Length(max=10)])
    importe = FloatField('importe', validators=[DataRequired()])
    tipoPago = StringField('tipoPago', validators=[DataRequired(), Length(max=20)])
    fechaFactura = DateField('fechaFactura', validators=[DataRequired()])
    #fechaVencimiento = DateField('fechaVencimiento', validators=[Optional()])
    fechaVencimientoDate = DateField('fechaVencimientoDate', validators=[Optional()])
    entidad = IntegerField('entidad', validators=[DataRequired()])
