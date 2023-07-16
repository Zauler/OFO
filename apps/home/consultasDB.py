import pandas as pd
from apps import db
from apps.config import *
from apps.home.models import *
from apps.authentication.models import *
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import Session

class ConsultasDB():
    def consultaRegisClient():
        queryClientes = db.session.query(Registros.id_Registro, Proyectos.Nombre, Clientes.Nombre,
                                    Registros.Concepto, Registros.Tipo, Registros.Importe,
                                    Registros.Tipo_Pago, Registros.Fecha_Factura, Registros.Fecha_Vencimiento,
                                    Bancos.Banco, Registros.Fact_Emit_Recib,
                                    Registros.Pago_Emit_Recib, Gestores.Nombre, Gestores.Apellidos).select_from(Registros).join(Clientes,
                                    Registros.id_Cliente == Clientes.id_Cliente).join(Proyectos,
                                        Registros.id_Proyecto == Proyectos.id_Proyecto).join(Bancos,
                                        Registros.id_Banco == Bancos.id_Banco).join(Gestores,
                                        Proyectos.id_Gestor == Gestores.id_Gestor)

        dfClientes = pd.read_sql(queryClientes.statement, db.session.bind)
        dfClientes['Fact_Emit_Recib'] = dfClientes['Fact_Emit_Recib'].astype(bool)
        dfClientes['Pago_Emit_Recib'] = dfClientes['Pago_Emit_Recib'].astype(bool)
        return dfClientes


    def consultaRegisProvee(): 
        queryProveedores = db.session.query(Registros.id_Registro, Proyectos.Nombre, Proveedores.Nombre,
                                Registros.Concepto, Registros.Tipo, Registros.Importe,
                                Registros.Tipo_Pago, Registros.Fecha_Factura, Registros.Fecha_Vencimiento,
                                Bancos.Banco, Registros.Fact_Emit_Recib,
                                Registros.Pago_Emit_Recib, Gestores.Nombre, Gestores.Apellidos).select_from(Registros).join(Proveedores,
                                Registros.id_Proveedor == Proveedores.id_Proveedor).join(Proyectos,
                                Registros.id_Proyecto == Proyectos.id_Proyecto).join(Bancos,
                                Registros.id_Banco == Bancos.id_Banco).join(Gestores,
                                Proyectos.id_Gestor == Gestores.id_Gestor)
        
        dfProveedores = pd.read_sql(queryProveedores.statement, db.session.bind)
        dfProveedores['Fact_Emit_Recib'] = dfProveedores['Fact_Emit_Recib'].astype(bool)
        dfProveedores['Pago_Emit_Recib'] = dfProveedores['Pago_Emit_Recib'].astype(bool)
        return dfProveedores


    def consultaRegistros():
        dfClientes = ConsultasDB.consultaRegisClient()
        dfProveedores = ConsultasDB.consultaRegisProvee()

        df = pd.concat([dfClientes, dfProveedores], ignore_index=True)
        df.sort_values(by="id_Registro",ignore_index=True,inplace=True)
        
        columnas=[
            'id_Registro', 'Proyecto', 'Proveedor / Cliente', 'Concepto', 'Tipo', 'Importe', 'Tipo Pago', 'Fecha Factura', 'Fecha Vencimiento', 'Banco',
            'Fact. Emit. Recibida', 'Pago Emit. Recibido', 'GestorNombre', 'GestorApellidos']
        
        df.columns = columnas
        df['Gestor'] = df["GestorNombre"] + " " + df["GestorApellidos"]
        columnasDrop = ["GestorNombre","GestorApellidos"]
        df = df.drop(columnasDrop,axis=1)

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
        queryBancos = db.session.query(Bancos.id_Banco, Bancos.Banco, Bancos.Cash, Bancos.Linea_max_Confirming).select_from(Bancos)

        dfBancos = pd.read_sql(queryBancos.statement, db.session.bind)
        return dfBancos


    def consultaProyectos():
        queryProyectos = db.session.query(Proyectos.id_Proyecto, Proyectos.Nombre).select_from(Proyectos)

        dfProyectos = pd.read_sql(queryProyectos.statement, db.session.bind)
        return dfProyectos
    

    def consultaGestores():
        queryGestores = db.session.query(Gestores.id_Gestor, Gestores.Nombre, Gestores.Apellidos).select_from(Gestores)

        dfGestores = pd.read_sql(queryGestores.statement, db.session.bind)
        return dfGestores


    #-----------------ELIMINTAR REGISTROS------------------
    def eliminarRegistro(id):
        
        try:
            registro_a_eliminar = db.session.query(Registros).filter(Registros.id_Registro == id).first()

            if registro_a_eliminar is not None:
                db.session.delete(registro_a_eliminar)
                db.session.commit()
                print("Registro Eliminado: ", id) #Si queremos añadimos más info
            else:
                print("Registro no encontrado")

        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al eliminar el registro: ",e)


    #-----------------MODIFICAR REGISTROS--------------------------
    def modificarRegistro(id,datosActualizar):

        try:
            registro_a_modificar = db.session.query(Registros).filter(Registros.id_Registro == id).first()

            if registro_a_modificar is not None:
                for campo, nuevo_valor in datosActualizar.items():
                    setattr(registro_a_modificar, campo, nuevo_valor) #Esta función cambia el atributo de la clase.
                db.session.commit()
                print("Registro modificado: ", id)
            else:
                print("Registro no encontrado")
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al actualizar el registro: ",e)




class ConsultasDBBancos():
    def consultaBancosCompleta():
        queryBancos = db.session.query(Bancos.id_Banco, Bancos.Banco, Bancos.Num_Cuenta, Bancos.Cash, Bancos.Linea_max_Confirming).select_from(Bancos)

        dfBancos = pd.read_sql(queryBancos.statement, db.session.bind)
        return dfBancos
    

    #-----------------ELIMINTAR REGISTROS DE BANCOS------------------
    def eliminarRegistro(id):
        
        try:
            registro_a_eliminar = db.session.query(Bancos).filter(Bancos.id_Banco == id).first()

            if registro_a_eliminar is not None:
                db.session.delete(registro_a_eliminar)
                db.session.commit()
                print("Registro Eliminado: ", id) #Si queremos añadimos más info
            else:
                print("Registro no encontrado")

        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al eliminar el registro: ",e)


    #-----------------MODIFICAR REGISTROS--------------------------
    def modificarRegistro(id,datosActualizar):

        try:
            registro_a_modificar = db.session.query(Bancos).filter(Bancos.id_Banco == id).first()

            if registro_a_modificar is not None:
                for campo, nuevo_valor in datosActualizar.items():
                    setattr(registro_a_modificar, campo, nuevo_valor) #Esta función cambia el atributo de la clase.
                db.session.commit()
                print("Registro modificado: ", id)
            else:
                print("Registro no encontrado")
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al actualizar el registro: ",e)



class ConsultasDBProveedores():
     # --------------------CONSULTA --------------------
    def consultaProveedoresCompleta():
        queryProveedores = db.session.query(Proveedores.id_Proveedor, Proveedores.CIF, Proveedores.Nombre, Proveedores.Direccion, Proveedores.Telefono, Proveedores.Tipo_Proveedor, Proveedores.Condiciones_confirming).select_from(Proveedores)
        dfProveedores = pd.read_sql(queryProveedores.statement, db.session.bind)
        
        return dfProveedores
     


    #-----------------ELIMINTAR REGISTROS------------------
    def eliminarRegistro(id):
        
        try:
            registro_a_eliminar = db.session.query(Proveedores).filter(Proveedores.id_Proveedor == id).first()

            if registro_a_eliminar is not None:
                db.session.delete(registro_a_eliminar)
                db.session.commit()
                print("Registro Eliminado: ", id) #Si queremos añadimos más info
            else:
                print("Registro no encontrado")

        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al eliminar el registro: ",e)


    #-----------------MODIFICAR REGISTROS--------------------------
    def modificarRegistro(id,datosActualizar):

        try:
            registro_a_modificar = db.session.query(Proveedores).filter(Proveedores.id_Proveedor == id).first()

            if registro_a_modificar is not None:
                for campo, nuevo_valor in datosActualizar.items():
                    setattr(registro_a_modificar, campo, nuevo_valor) #Esta función cambia el atributo de la clase.
                db.session.commit()
                print("Registro modificado: ", id)
            else:
                print("Registro no encontrado")
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al actualizar el registro: ",e)




class ConsultaDBClientes():

    # --------------------CONSULTA --------------------
    def consultaClientesCompleta():
        queryClientes = db.session.query(Clientes.id_Cliente, Clientes.CIF, Clientes.Nombre, Clientes.Direccion, Clientes.Telefono, Clientes.Tipo_Cliente).select_from(Clientes)
        dfClientes = pd.read_sql(queryClientes.statement, db.session.bind)

        dfClientes['Direccion'] = dfClientes['Direccion'].str.encode('utf-8', 'ignore').str.decode('utf-8')

        return dfClientes

    #-----------------ELIMINTAR REGISTROS------------------
    def eliminarRegistro(id):
        
        try:
            registro_a_eliminar = db.session.query(Clientes).filter(Clientes.id_Cliente == id).first()

            if registro_a_eliminar is not None:
                db.session.delete(registro_a_eliminar)
                db.session.commit()
                print("Registro Eliminado: ", id) #Si queremos añadimos más info
            else:
                print("Registro no encontrado")

        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al eliminar el registro: ",e)


    #-----------------MODIFICAR REGISTROS--------------------------
    def modificarRegistro(id,datosActualizar):

        try:
            registro_a_modificar = db.session.query(Clientes).filter(Clientes.id_Cliente == id).first()

            if registro_a_modificar is not None:
                for campo, nuevo_valor in datosActualizar.items():
                    setattr(registro_a_modificar, campo, nuevo_valor) #Esta función cambia el atributo de la clase.
                db.session.commit()
                print("Registro modificado: ", id)
            else:
                print("Registro no encontrado")
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al actualizar el registro: ",e)



class ConsultasDBProyectos():
    def consultaProyectosCompleta():
        queryProyectos = db.session.query(Proyectos.id_Proyecto, Proyectos.Nombre, Proyectos.Direccion, Proyectos.Descripcion,
                                          Clientes.Nombre, Gestores.Nombre, Gestores.Apellidos).select_from(Proyectos).join(Gestores,
                                Proyectos.id_Gestor == Gestores.id_Gestor).join(Clientes,
                                    Proyectos.id_Cliente == Clientes.id_Cliente)

        dfProyectos = pd.read_sql(queryProyectos.statement, db.session.bind)

        columnas=[
            'id_Proyecto', 'Proyecto', 'Direccion', 'Descripcion', 'Cliente', 'GestorNombre', 'GestorApellidos']
        
        dfProyectos.columns = columnas

        dfProyectos['Gestor'] = dfProyectos["GestorNombre"] + " " + dfProyectos["GestorApellidos"]
        columnasDrop = ["GestorNombre","GestorApellidos"]
        dfProyectos = dfProyectos.drop(columnasDrop,axis=1)

        return dfProyectos

    #-----------------ELIMINTAR REGISTROS DE BANCOS------------------
    def eliminarRegistro(id):
        
        try:
            registro_a_eliminar = db.session.query(Proyectos).filter(Proyectos.id_Proyecto == id).first()

            if registro_a_eliminar is not None:
                db.session.delete(registro_a_eliminar)
                db.session.commit()
                print("Registro Eliminado: ", id) #Si queremos añadimos más info
            else:
                print("Registro no encontrado")

        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al eliminar el registro: ",e)


    #-----------------MODIFICAR REGISTROS--------------------------
    def modificarRegistro(id,datosActualizar):

        try:
            registro_a_modificar = db.session.query(Proyectos).filter(Proyectos.id_Proyecto == id).first()

            if registro_a_modificar is not None:
                for campo, nuevo_valor in datosActualizar.items():
                    setattr(registro_a_modificar, campo, nuevo_valor) #Esta función cambia el atributo de la clase.
                db.session.commit()
                print("Registro modificado: ", id)
            else:
                print("Registro no encontrado")
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al actualizar el registro: ",e)


class ConsultasDBUsuarios():
     # --------------------CONSULTA --------------------
    def consultaUsuariosCompleta():
        queryUsuarios = db.session.query(Users.id, Users.username, Users.Rol, Users.Nombre, Users.Apellidos, Users.Direccion, Users.email).select_from(Users)
        dfUsuarios = pd.read_sql(queryUsuarios.statement, db.session.bind)
        
        return dfUsuarios
    

    def consultaUsuarioActual(id):
        queryUsuario = db.session.query(Users).filter(Users.id == id).first()
        
        return queryUsuario
     


    #-----------------ELIMINTAR REGISTROS------------------
    def eliminarRegistro(id):
        
        try:
            registro_a_eliminar = db.session.query(Users).filter(Users.id == id).first()

            if registro_a_eliminar is not None:
                db.session.delete(registro_a_eliminar)
                db.session.commit()
                print("Registro Eliminado: ", id) #Si queremos añadimos más info
            else:
                print("Registro no encontrado")

        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al eliminar el registro: ",e)


    #-----------------MODIFICAR REGISTROS--------------------------
    def modificarRegistro(id,datosActualizar):

        try:
            registro_a_modificar = db.session.query(Users).filter(Users.id == id).first()

            if registro_a_modificar is not None:
                for campo, nuevo_valor in datosActualizar.items():
                    setattr(registro_a_modificar, campo, nuevo_valor) #Esta función cambia el atributo de la clase.
                db.session.commit()
                print("Registro modificado: ", id)
            else:
                print("Registro no encontrado")
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al actualizar el registro: ",e)



class ConsultaDBGestores():

    # --------------------CONSULTA --------------------
    def consultaCompleta():
        queryGestores = db.session.query(Gestores.id_Gestor, Gestores.Nombre, Gestores.Apellidos, Gestores.DNI, Gestores.Zona_Geo).select_from(Gestores)
        dfGestores = pd.read_sql(queryGestores.statement, db.session.bind)

        return dfGestores

    #-----------------ELIMINTAR REGISTROS------------------
    def eliminarRegistro(id):
        
        try:
            registro_a_eliminar = db.session.query(Gestores).filter(Gestores.id_Gestor == id).first()

            if registro_a_eliminar is not None:
                db.session.delete(registro_a_eliminar)
                db.session.commit()
                print("Registro Eliminado: ", id) #Si queremos añadimos más info
            else:
                print("Registro no encontrado")

        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al eliminar el registro: ",e)


    #-----------------MODIFICAR REGISTROS--------------------------
    def modificarRegistro(id,datosActualizar):

        try:
            registro_a_modificar = db.session.query(Gestores).filter(Gestores.id_Gestor == id).first()

            if registro_a_modificar is not None:
                for campo, nuevo_valor in datosActualizar.items():
                    setattr(registro_a_modificar, campo, nuevo_valor) #Esta función cambia el atributo de la clase.
                db.session.commit()
                print("Registro modificado: ", id)
            else:
                print("Registro no encontrado")
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Ocurrió un error al actualizar el registro: ",e)