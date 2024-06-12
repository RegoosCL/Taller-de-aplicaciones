from flask import Flask, render_template, redirect, request, session, url_for, jsonify, make_response
from flask_mysqldb import MySQL
from fpdf import FPDF

app = Flask(__name__, template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bikeregodb'
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
        cur.execute('SELECT * FROM admin WHERE correo = %s AND password = %s', (_correo, _password))
        admin_account = cur.fetchone()

        if admin_account:
            session['logueado'] = True
            session['id'] = admin_account['id']
            return redirect(url_for('administrador'))
        
        cur.execute('SELECT * FROM usuario WHERE correo = %s AND password = %s', (_correo, _password))
        user_account = cur.fetchone()

        if user_account:
            session['logueado'] = True
            session['id'] = user_account['id']
            return redirect(url_for('admin'))
        else:
            return render_template('formulario.html', mensaje="Usuario o contraseña incorrectos")

    return render_template('formulario.html')

@app.route('/crear-registro', methods=["GET", "POST"])
def crear_registro():
    nombre = request.form['txtNombre']
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']
    rut = request.form['txtRut']
    telefono = request.form['txtTelefono']
    postal = request.form['txtPostal']
    nacimiento = request.form['txtNacimiento']
    region = request.form['txtRegion']
    comuna = request.form['txtComuna']
    calle = request.form['txtCalle']
    numero = request.form['txtNumero']
    piso = request.form['txtPiso']
    referencia = request.form['txtReferencia']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuario (nombre, correo, password, rut, telefono, postal, nacimiento, region, comuna, calle, numero, piso, referencia) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                (nombre, correo, password, rut, telefono, postal, nacimiento, region, comuna, calle, numero, piso, referencia))
    mysql.connection.commit()

    return render_template('formulario.html', mensaje2="Registro exitoso")

@app.route('/guardar_arriendo', methods=["POST"])
def guardar_arriendo():
    data = request.get_json()
    modelo = data['modelo']
    precio_base = data['precio_base']
    dias = data['dias']
    precio_final = float(data['precio_final'].replace('CLP ', ''))
    nombre = data['nombre']
    correo = data['correo']
    direccion = data['direccion']
    telefono = data['telefono']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO arriendo (modelo, precio_base, dias, precio_final, nombre, correo, region, telefono) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (modelo, precio_base, dias, precio_final, nombre, correo, direccion, telefono))
    mysql.connection.commit()
    cur.close()

    return jsonify(success=True)

@app.route('/listar', methods=["GET", "POST"])
def listar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuario")
    usuario = cur.fetchall()
    cur.close()

    return render_template("listar_user.html", usuario=usuario)

@app.route('/listar_arri', methods=["GET", "POST"])
def listar_arri():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM arriendo")
    usuario = cur.fetchall()
    cur.close()

    return render_template("listar_arriendo.html", usuario=usuario)

@app.route('/generar_pdf', methods=["GET"])
def generar_pdf():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM arriendo")
    arriendos = cur.fetchall()
    cur.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Lista de Arriendos", ln=True, align='C')

    for arriendo in arriendos:
        pdf.cell(200, 10, txt=f"*ID: {arriendo['id']} - Modelo: {arriendo['modelo']} - Precio Base: {arriendo['precio_base']} - Dias: {arriendo['dias']} - Precio Final: {arriendo['precio_final']} ", ln=True)
        pdf.cell(200, 10, txt=f"Nombre: {arriendo['nombre']} - Correo: {arriendo['correo']} - Dirección: {arriendo['region']} - Teléfono: {arriendo['telefono']}", ln=True)
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=arriendos.pdf'
    return response

if __name__ == '__main__':
    app.secret_key = "javier_hds"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
