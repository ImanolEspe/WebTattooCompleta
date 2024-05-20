from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="clientestattoo"
)

# Crear un cursor para ejecutar consultas
cursor = conexion.cursor()

# Ruta para obtener datos de la base de datos
@app.route('/datos')
def obtener_datos():
    # Ejecutar una consulta
    cursor.execute("SELECT * FROM clientes")

    # Obtener los resultados
    resultados = cursor.fetchall()

    # Convertir los resultados a una lista de diccionarios para enviar como JSON
    datos = []
    for fila in resultados:
        datos.append({
            'ID': fila[0],  # Reemplaza 'columna1' con el nombre real de la columna
            'Nombre': fila[1],  # Reemplaza 'columna2' con el nombre real de la columna
            'Apellidos': fila[2],
            'Calle': fila[3],
            'Email': fila[4],
            'NumTelefono': fila[5],
        })

    # Devolver los datos como JSON
    return jsonify(datos)

# Ruta para agregar un nuevo cliente
@app.route('/agregar-cliente', methods=['POST'])
def agregar_cliente():
    # Obtener los datos del nuevo cliente del cuerpo de la solicitud
    datos_cliente = request.json
    nombre = datos_cliente['nombre']
    apellidos = datos_cliente['apellidos']
    calle = datos_cliente['calle']
    email = datos_cliente['email']
    num_telefono = datos_cliente['numTelefono']

    # Insertar el nuevo cliente en la base de datos
    cursor.execute("INSERT INTO clientes (nombre, apellidos, calle, email, numTelefono) VALUES (%s, %s, %s, %s, %s)", (nombre, apellidos, calle, email, num_telefono))
    conexion.commit()

    # Devolver una respuesta al frontend
    return jsonify({'mensaje': 'Cliente agregado correctamente'})

if __name__ == '__main__':
    app.run(debug=True)