from flask import Flask, render_template, redirect, request, session, url_for
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('formulario.html')

@app.route('/index')
def admin():
    return render_template('index.html')

@app.route('/arriendos')
def arriendos():
    return render_template('arriendos.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/garantiaycambio')
def garantiaycambio():
    return render_template('garantiaycambio.html')

@app.route('/politicaprivacidad')
def politicaprivacidad():
    return render_template('politicaprivacidad.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/repuestos')
def repuestos():
    return render_template('repuestos.html')

@app.route('/terminoycondiciones')
def terminoycondiciones():
    return render_template('terminoycondiciones.html')

@app.route('/administrador')
def administrador():
    return render_template('administrador.html')

@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuario WHERE correo = %s AND password = %s', (_correo, _password))
        cur.execute('SELECT * FROM admin WHERE correo = %s AND password = %s', (_correo, _password))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['id'] = account['id']
            return redirect(url_for('admin'))
        if account:
            session['logueado'] = True
            session['id'] = account['id']
            return redirect(url_for('administrador'))        
        else:
            return render_template('formulario.html', mensaje="usuario incorrecto")


        

@app.route('/crear-registro', methods=["GET", "POST"])
def crear_registro():

    nombre=request.form['txtNombre']
    correo=request.form['txtCorreo']
    password=request.form['txtPassword']
    rut=request.form['txtRut']
    telefono=request.form['txtTelefono']
    postal=request.form['txtPostal']
    nacimiento=request.form['txtNacimiento']
    region=request.form['txtRegion']
    comuna=request.form['txtComuna']
    calle=request.form['txtCalle']
    numero=request.form['txtNumero']
    piso=request.form['txtPiso']
    referencia=request.form['txtReferencia']


    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuario (nombre, correo, password, rut, telefono, postal, nacimiento, region, comuna, calle, numero, piso, referencia) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(nombre,correo,password,rut,telefono,postal,nacimiento,region,comuna,calle,numero,piso,referencia))
    account = cur.fetchone()
    mysql.connection.commit()

    if account:
        session['logueado'] = True
        session['id'] = account['id']
        return redirect(url_for('admin'))
    else:
        return render_template('formulario.html', mensaje2="Registro exitoso")

if __name__ == '__main__':
    app.secret_key = "javier_hds"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
