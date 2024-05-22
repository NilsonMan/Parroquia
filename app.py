from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Datos de usuario (en un caso real, esto se almacenaría en una base de datos)
usuarios = {
    "usuario1": "contraseña1",
    "usuario2": "contraseña2"
}

# Funciones de base de datos
def conectar_db():
    return sqlite3.connect('tu_basede_datos.db')

def buscar_bd(query):
    conn = conectar_db()
    cursor = conn.cursor()
    query = f"%{query}%"
    
    # Buscar en tabla Difuntos
    cursor.execute('''
        SELECT 'Difunto' AS tipo, nombre_completo, apellido_paterno, apellido_materno, fecha_defuncion, fecha, familia_id 
        FROM Difuntos 
        WHERE nombre_completo LIKE ? OR apellido_paterno LIKE ? OR apellido_materno LIKE ?
    ''', (query, query, query))
    difuntos = cursor.fetchall()
    
    # Buscar en tabla Clientes
    cursor.execute('''
        SELECT 'Cliente' AS tipo, Num_nuevo, Nombre_titular, Apellido_paterno, Apellido_materno, Familia_id, Cripta 
        FROM Clientes 
        WHERE Nombre_titular LIKE ? OR Apellido_paterno LIKE ? OR Apellido_materno LIKE ?
    ''', (query, query, query))
    clientes = cursor.fetchall()
    
    conn.close()
    return difuntos + clientes

@app.route("/buscar")
def buscar():
    query = request.args.get('query')
    resultados = buscar_bd(query)
    return render_template("resultados_busqueda.html", query=query, resultados=resultados)

@app.route("/agregar_difunto", methods=["POST"])
def agregar_difunto():
    nombre_completo = request.form["nombre_completo"]
    apellido_paterno = request.form["apellido_paterno"]
    apellido_materno = request.form["apellido_materno"]
    fecha_defuncion = request.form["fecha_defuncion"]
    fecha = request.form["fecha"]
    familia_id = request.form["familia_id"]

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Difuntos (nombre_completo, apellido_paterno, apellido_materno, fecha_defuncion, fecha, familia_id)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (nombre_completo, apellido_paterno, apellido_materno, fecha_defuncion, fecha, familia_id))
    conn.commit()
    conn.close()
    
    return redirect(url_for("difuntos"))

def agregar_cliente(num_nuevo, titular, apellido_paterno, apellido_materno, familia_id, cripta):
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO Clientes (Num_nuevo, Nombre_titular, Apellido_paterno, Apellido_materno, Familia_id, Cripta)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (num_nuevo, titular, apellido_paterno, apellido_materno, familia_id, cripta))
        conn.commit()
    except sqlite3.IntegrityError:
        # Manejar la excepción de violación de la restricción UNIQUE
        return "El número nuevo ya está en uso. Por favor, elija otro número."
    finally:
        conn.close()

def obtener_familias():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Familia_id FROM Clientes")
    familias = cursor.fetchall()
    conn.close()
    return familias

def obtener_difuntos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Difuntos")
    difuntos = cursor.fetchall()
    conn.close()
    return difuntos

def obtener_clientes(letra=None):
    conn = conectar_db()
    cursor = conn.cursor()
    if letra is not None:
        cursor.execute("SELECT * FROM Clientes WHERE Cripta LIKE ?", ('%' + letra + '%',))
    else:
        cursor.execute("SELECT * FROM Clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

# Rutas existentes
@app.route("/")
def inicio():
    return render_template("inicio_sesion.html")

@app.route("/difuntos")
def difuntos():
    familias = obtener_clientes()
    difuntos = obtener_difuntos()
    return render_template("difuntos.html", familias=familias, difuntos=difuntos)

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    contraseña = request.form["contraseña"]
    if usuario in usuarios and usuarios[usuario] == contraseña:
        return redirect(url_for("menu_principal"))
    else:
        return "Usuario o contraseña incorrectos"

@app.route("/menu_principal")
def menu_principal():
    return render_template("menu_principal.html")

@app.route("/agregar")
def agregar():
    clientes = obtener_clientes()   
    return render_template("agregar.html", clientes=clientes)

@app.route("/usuarios_con_a")
def usuarios_con_a():
    clientes = obtener_clientes('a')
    return render_template("usuarios_con_a.html", clientes=clientes)

@app.route("/usuarios_con_b")
def usuarios_con_b():
    clientes = obtener_clientes('b')
    return render_template("usuarios_con_b.html", clientes=clientes)

@app.route("/agregar_cliente", methods=["POST"])
def agregar_cliente_route():
    num_nuevo = request.form["num_nuevo"]
    titular = request.form["titular"]
    apellido_paterno = request.form["apellido_paterno"]
    apellido_materno = request.form["apellido_materno"]
    familia_id = request.form["familia_id"]
    cripta = request.form["cripta"]
    
    print("Datos del nuevo cliente:")
    print("NUM. NUEVO:", num_nuevo)
    print("TITULAR:", titular)
    print("APELLIDO PATERNO:", apellido_paterno)
    print("APELLIDO MATERNO:", apellido_materno)
    print("FAMILIA ID:", familia_id)
    print("CRIPTA:", cripta)
    
    agregar_cliente(num_nuevo, titular, apellido_paterno, apellido_materno, familia_id, cripta)
    
    print("Cliente agregado correctamente a la base de datos.")
    
    clientes = obtener_clientes()  
    return render_template("agregar.html", clientes=clientes)

if __name__ == "__main__":
    app.run(debug=True)
