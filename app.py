# Se importa flask


import re
from data import usuario
from data.usuario import Usuario
from itertools import product
from flask import Flask, request, render_template, session, redirect, url_for
from flask import json
from flask.helpers import flash
from flask.json import jsonify


# # se importa la libreria bcrypt para la encriptacion 
import bcrypt 

#  Se importa los objetos

# from usuario import Usuario
# from admin import Admin
# from data import Usuario
from data import Admin, admin


from db_user_admin import usuarios,admins,saldo_limite,usuarios_encontrados

app = Flask('tenderos')


#  ..................................


simbolo_peso = "$"


# ###########################################
# RUTAS SOLAMENTE PARA MOSTRAR EN PANTALLA --> GET
# ###########################################

@app.route('/')
def interfaz_navegacion():
    if "usuarios" in session:
        return redirect(url_for('interfaz_workspace'))
    return render_template('landing.html')

@app.route('/login')
def interfaz_login():
    return render_template('login.html')

@app.route('/signUp')
def interfaz_signUp():
    return render_template('signUp.html')

@app.route('/crear_usuario')
def interfaz_crear_usuario():
    return render_template('crear-usuario.html')

@app.route('/edit_saldo')
def interfaz_saldo():
    return render_template('editar-saldo.html')

@app.route('/editar_usuario/<id>')
def interfaz_editar_usuario(id):
    
    usuario_encontrado = tuple(usuario for usuario in usuarios if usuario.documento == id)

    if len(usuario_encontrado) > 0:
        # Encuentro el usuario
        usuario = usuario_encontrado[0]
        return render_template('edit_user.html', usuario=usuario)
    else:
        return {'mensaje': f'No se ha encontrado el usuario con el id {id}'}

@app.route('/workspace/usuarios')
def interfaz_workspace():
    # Verificamos las cookies si el usuario ya ha iniciado sesion
    # if not "usuario" in session:
    #     return redirect(url_for('interfaz_navegacion'))
    

    # Obtengo todos los usuarios que estan registrados
    #  Se crea una lista para guardar los usuarios registrados y poderlos imprimir

    long = len(usuarios)
    print(f"{long=}")
    # mensaje1 = documento 
    
    # obtendo el saldo limite de la lista
    saldo = saldo_limite[0]
    simbolo_moneda = simbolo_peso
    # return{'mensaje':f"{long} ---"}
    return render_template('workspace.html', usuarios=usuarios,longitud_usuarios=long, cuantos_usuarios_registrados=long, simbolo_moneda=simbolo_moneda,saldo=saldo)





# @app.route('/')
# def __():
#     return


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# INTERFACES DE ERRORES

@app.route('/error_login')
def interfaz_login_incorrecto():
    return render_template('login-incorrecto.html')

@app.route('/ya_exite')
def interfaz_ya_existe():
    return render_template('ya-existe-admin.html')

@app.route('/EROOR-404')
def interfaz_no_encontrado():
    return render_template('no-encontrado.html')

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


# #################################
# INTERFACES CORRECTAS

@app.route('/logueado')
def interfaz_login_correcto():
    return render_template('logueado.html')

@app.route('/registro-exitoso')
def interfaz_registro_exitoso():
    return render_template('registro-exitoso.html')

# # #######################################

# Interfaces para los usuarios
@app.route('/usuario-registrado')
def interfaz_usuario_ya_registrado():
    return render_template('ya_registrado_usuario.html')

@app.route('/usuarios_encontrados')
def interfaz_usu_encontrados():
    # CANTIDAD DE USUARIOS ENCONTRADOS
    cantidad_user_found = len(usuarios_encontrados) 
    return render_template('usuarios-encontrados.html', usuarios_encontrados=usuarios_encontrados, cantidad_usuarios=cantidad_user_found)

# ##########################################


@app.route('/buscar_usuario', methods=['POST'])
def get_usuario_buscado():

    # Obtengo el dato que me entrega el FrontEnd
    documento_usuario = request.form.get("buscar")
    # buscar por cada usuario

    #  Se pasa por cada dato de la lista
    for usuario in usuarios:
        # Se valida si esta el usuario a buscar
        if usuario.documento == documento_usuario:
            mensaje = f"USUARIO ENCONTRADO! DOCUMENTO:{usuario.documento} - NOMBRES:{usuario.nombres} - MOVIL:{usuario.movil} - SALDO:{usuario.saldo}"
            return {'message':mensaje}
            

        else:
            print("hola desde else:")
            return redirect(url_for('interfaz_usu_encontrados'))
    # return {'NN':'usuario no encontrado'}


@app.route('/login', methods=['POST'])
def get_login():
    
    #  Se verifica el ingreso del usuario : tendero : ADMIN

    # Los datos eentran por formulario HTML
    email = request.form.get("email")
    password = request.form.get("password")

    # los datos entran por JSON
    # email = request.json['email']
    # password = request.json['password']


    for admin in admins:
        # print("for")
        if email == admin.correo and password == admin.password:

            '''TODO PENDIENTE LAS COOKIES'''
            
            # Si el usuario y contraseña coinciden con los de la BD
            # Se verifica la cookie
            # Se crea una sesion y se envia una cookie al navegador

            # session['usuario'] = email
            # session[] = 

            return redirect(url_for('interfaz_login_correcto'))
            # return {'mensaje':'inicio de sesion exitoso',
            #         'status':200}
        return redirect(url_for('interfaz_login_incorrecto'))
    return redirect(url_for('interfaz_no_encontrado'))
    # return {'mensaje':'usuario incorrecto',
    #         'statusCode':404}
    


@app.route('/signUp', methods=['POST'])
def get_signUp():

    def obtener_usuario(request):

        #  Se intancia la clase, para crear un Admin nuevo
        admin = Admin()

        # #  Se crea los atributos del Admin
        # Los datos eentran por formulario HTML
        admin.nombres = request.form.get('nombres')
        admin.documento = request.form.get('documento')
        admin.correo = request.form.get('correo')
        admin.password = request.form.get('password')

        # los datos entran por JSON
        # admin.nombres = request.json['nombres']
        # admin.documento = request.json['documento']
        # admin.correo = request.json['correo']
        # admin.password = request.json['password']
    
        return admin

    # Se llama la funcion
    admin_registrado = obtener_usuario(request)

    # Se verifica si el admin esta registrado previamente
    for admin in admins:
        # se compara cada admin registrado con el admin ingresado
        if  admin_registrado.correo == admin.correo:
            return redirect(url_for('interfaz_ya_existe'))
            # return jsonify({'message':'Ya hay un usuario registrado con este ',
            #                 'statuscode':404})

        return redirect(url_for('interfaz_registro_exitoso'))
        # Se guarda el admin creado a la DB
    admins.append(admin_registrado)
    print(admin_registrado.correo,"-",admin_registrado.documento)

    # Registro exiroso
    return redirect(url_for('interfaz_registro_exitoso'))


    # return jsonify({'statusCode':200,
    #                 'mensaje':'Registro exitoso'})


@app.route('/crear_usuario', methods=['POST'])
def post_crear_usuario():
    print(request.form.get("movil"))

    # definimos funcion para crear USUARIO
    def get_usuario(request):

        # creamos un nuevo objeto usuario
        usuario = Usuario()

        # Los datos eentran por formulario HTML
        usuario.documento = request.form.get('documento')
        usuario.nombres = request.form.get('nombres').lower()
        usuario.movil = request.form.get('movil')
        usuario.saldo =request.form.get('saldo')


        # los datos entran por JSON
        # usuario.documento = request.json['documento']
        # usuario.nombres = request.json['nombres']
        # usuario.movil = request.json['movil']
        # usuario.saldo =request.json['saldo']

        return usuario

    # Se llama la funcion y se guarda en una variable 
    usuario_registrado = get_usuario(request)

    # Se verifica que el usuario no este registrado previamente
    for usuario in usuarios:
        if usuario.documento == usuario_registrado.documento:

            '''JSON'''
            # Si el usuario esta registrado se retornara lo siguiente
            usuario = usuario.documento
            return render_template('aviso-usuario-registrado.html',usuario=usuario)

            # return redirect(url_for('interfaz_usuario_ya_registrato'))

    # Si el usuario NO esta registrado se retornara lo siguiente:
    usuarios.append(usuario_registrado)
    usuario = usuario_registrado.documento
    nombre = usuario_registrado.nombres
    return render_template('usuario-registrado.html', usuario=usuario, nombres=nombre)




# #########################
#  REUTAS - PUT
# ########################
@app.route('/edit_usuario', methods=['POST'])
def post_edit_usuario():
    # Busco el usuario registrado en la base de datos con el id
    documento = request.form.get('documento')

    print(request.form)

    if documento:
        print("Documento")
        # Verifico el documento con el usuario
        resultados = tuple(usuario for usuario in usuarios if usuario.documento == documento)

        if len(resultados)>0:
            usuario = resultados[0]
            print('Usuario encontrado')
            usuario.nombres = request.form.get('nombres')
            usuario.movil = request.form.get('movil')
            usuario.saldo = float(request.form.get('saldo'))

            saldo_antiguo = usuario.saldo

            # Saldo obtenido desde el 'FORM' 
            editar_saldo = float(request.form.get('editarSaldo')) 

            operacion = saldo_antiguo + editar_saldo 
            usuario.saldo = operacion
            
            print(vars(usuario))

    return redirect(url_for('interfaz_workspace'))

@app.route('/edit_limite_creditos', methods=['POST'])
def limite_saldo():
    print(saldo_limite)

    saldo_nuevo = 0
    saldo_antiguo = 0

    saldo_nuevo = int(request.form.get('saldo'))
    # El elemnto que estaba en la lista
    saldo_antiguo = saldo_limite[0]
    saldo_limite[0] = saldo_nuevo
    
    print(saldo_limite)
        # Se define el mensaje a mostrar
    mensaje =f"El saldo se edito correctamente SALDO ANTIGUO {simbolo_peso}{saldo_antiguo} SALDO NUEVO {simbolo_peso}{saldo_nuevo}"
    # return redirect(url_for('interfaz_navegacion'))
    # return {'menssage':mensaje}
    return render_template('saldo_editado_correctamente.html', saldo_antiguo=saldo_antiguo, saldo_nuevo=saldo_nuevo)

# ########################################
# RUTAS DELETE
# ########################################

@app.route('/eliminar_usuario/<id>')
def interfaz_eliminar_usuario(id):

    usuario_encontrado = tuple(usuario for usuario in usuarios if usuario.documento == id)

    if (len(usuario_encontrado) > 0):
        # Obtenemos el dato encontrado en el generador (tuple)
        usuario = usuario_encontrado[0]
        return render_template('eliminar-usuario.html', usuario=usuario)
    else:
        return {'mensaje': f'No se ha encontrado el usuario con el id {id}'}

@app.route('/eliminar_usuario0', methods=['POST'])
def eliminar_usuario():

    documento = request.form.get('documento')

    for usuario in usuarios:
        if (usuario.documento == documento):
            usuarios.pop(usuario.documento)
            # usuarios.pop(usuario.nombres)
            # usuarios.pop(usuario.movil)
            # usuarios.pop(usuario.saldo)

            return {'mensaje':'Usuario eliminado'}
        else:
            return{'mensaje':'usuario no found'}
'''
'''

# //////////////////////////////////////
# CERAR SESION
@app.route('/sesion_cerrada')
def sesion_cerrada():
    return render_template('sesion_cerrada_exitosamente.html')



if __name__ == "__main__":
    app.run(debug=True, port=5000)


