import sqlite3

# Conectar a la base de datos
conexion = sqlite3.connect('tu_basede_datos.db')
cursor = conexion.cursor()

# Crear tabla Clientes
cursor.execute('''CREATE TABLE IF NOT EXISTS Clientes (
                    Num_nuevo INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nombre_titular TEXT,
                    Apellido_paterno TEXT,
                    Apellido_materno TEXT,
                    Familia_id TEXT,
                    Cripta TEXT,
                    FOREIGN KEY (Familia_id) REFERENCES Familia(Familia_id)
                )''')

#cursor.execute('DROP TABLE IF EXISTS Clientes')
# Crear tabla Difuntos
cursor.execute('''CREATE TABLE IF NOT EXISTS Difuntos (
                    ID_difunto INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nombre_completo TEXT,
                    Apellido_paterno TEXT,
                    Apellido_materno TEXT,
                    Familia_id TEXT,
                    Fecha_defuncion DATE,
                    Fecha DATE,
                    FOREIGN KEY (Familia_id) REFERENCES Familia(Familia_id)
                )''')
#cursor.execute('DROP TABLE IF EXISTS Difuntos')
# Crear tabla Familia
cursor.execute('''CREATE TABLE IF NOT EXISTS Familia (
                    Familia_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nombre_familia TEXT,
                    ID_cliente INTEGER,
                    ID_difunto TEXT,
                    FOREIGN KEY (ID_cliente) REFERENCES Clientes(Num_nuevo),
                    FOREIGN KEY (ID_difunto) REFERENCES Difuntos(ID_difunto)
                )''')

# Crear tabla Pagos
cursor.execute('''CREATE TABLE IF NOT EXISTS Pagos (
                    Folio TEXT PRIMARY KEY,
                    ID_cliente TEXT,
                   eliminiar--- ID_difunto TEXT,
                    Saldo REAL,
                    Abono REAL,
                    Saldo_total REAL,
                    Notas TEXT,
                    FOREIGN KEY (ID_cliente) REFERENCES Clientes(Num_nuevo),
                    FOREIGN KEY (ID_difunto) REFERENCES Difuntos(ID_difunto)
                )''')

# Confirmar cambios y cerrar la conexión
conexion.commit()
conexion.close()
