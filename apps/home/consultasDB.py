import pandas as pd
from apps import db
from apps.config import *
from apps.home.models import *

class ConsultasDB():
    def consultaRegisClient():
        queryClientes = db.session.query(Registros.id_Registro, Proyectos.Nombre, Clientes.Nombre,
                                    Registros.Concepto, Registros.Tipo, Registros.Importe,
                                    Registros.Tipo_Pago, Registros.Fecha_Factura, Registros.Fecha_Vencimiento,
                                    Bancos.Banco, Registros.Fact_Emit_Recib,
                                    Registros.Pago_Emit_Recib, Gestores.Nombre).select_from(Registros).join(Clientes,
                                    Registros.id_Cliente == Clientes.id_Cliente).join(Proyectos,
                                        Registros.id_Proyecto == Proyectos.id_Proyecto).join(Bancos,
                                        Registros.id_Banco == Bancos.id_Banco).join(Gestores,
                                        Proyectos.id_Gestor == Gestores.id_Gestor)

        dfClientes = pd.read_sql(queryClientes.statement, db.session.bind)
        return dfClientes


    def consultaRegisProvee(): 
        queryProveedores = db.session.query(Registros.id_Registro, Proyectos.Nombre, Proveedores.Nombre,
                                Registros.Concepto, Registros.Tipo, Registros.Importe,
                                Registros.Tipo_Pago, Registros.Fecha_Factura, Registros.Fecha_Vencimiento,
                                Bancos.Banco, Registros.Fact_Emit_Recib,
                                Registros.Pago_Emit_Recib, Gestores.Nombre).select_from(Registros).join(Proveedores,
                                Registros.id_Proveedor == Proveedores.id_Proveedor).join(Proyectos,
                                Registros.id_Proyecto == Proyectos.id_Proyecto).join(Bancos,
                                Registros.id_Banco == Bancos.id_Banco).join(Gestores,
                                Proyectos.id_Gestor == Gestores.id_Gestor)
        
        dfProveedores = pd.read_sql(queryProveedores.statement, db.session.bind)
        return dfProveedores


    def consultaRegistros():
        dfClientes = ConsultasDB.consultaRegisClient()
        dfProveedores = ConsultasDB.consultaRegisProvee()

        df = pd.concat([dfClientes, dfProveedores], ignore_index=True)
        df.sort_values(by="id_Registro",ignore_index=True,inplace=True)
        
        columnas=[
            'id_Registro', 'Proyecto', 'Proveedor / Cliente', 'Concepto', 'Tipo', 'Importe', 'Tipo Pago', 'Fecha Factura', 'Fecha Vencimiento', 'Banco',
            'Fact. Emit. Recibida', 'Pago Emit. Recibido', 'Gestor']
        
        df.columns = columnas
        return df


    def consultaClientes():
        queryClientes = db.session.query(Clientes.id_Cliente, Clientes.Nombre).select_from(Clientes)

        dfClientes = pd.read_sql(queryClientes.statement, db.session.bind)
        return dfClientes


    def consultaProveedores():
        queryProve = db.session.query(Proveedores.id_Proveedor, Proveedores.Nombre, Proveedores.Condiciones_confirming).select_from(Proveedores)

        dfProve = pd.read_sql(queryProve.statement, db.session.bind)
        return dfProve


    def consultaBancos():
        queryBancos = db.session.query(Bancos.id_Banco, Bancos.Banco).select_from(Bancos)

        dfBancos = pd.read_sql(queryBancos.statement, db.session.bind)
        return dfBancos


    def consultaProyectos():
        queryProyectos = db.session.query(Proyectos.id_Proyecto, Proyectos.Nombre).select_from(Proyectos)

        dfProyectos = pd.read_sql(queryProyectos.statement, db.session.bind)
        return dfProyectos