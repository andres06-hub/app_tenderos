# Se importa flask
from logging import debug
from flask import Flask, request, render_template, session, redirect, url_for

# se importa la libreria bcrypt para la encriptacion 
import bcrypt 

#  Se importa los objetos
from data import Usuario
from data import Admin

app = Flask('tenderos')


# ###########################################
# RUTAS SOLAMENTE PARA MOSTRAR EN PANTALLA --> GET
# ###########################################

@app.route('/login')
def interfaz_login():
    return render_template('login.html')

@app.route('/signUp')
def interfaz_signUp():
    return render_template('signUp.html')

@app.route('')



if __name__ in '__main__':
        app.run(debug=True, port=5000)