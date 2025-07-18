from flask import Flask, render_template, request
import psycopg2
from datetime import date

app = Flask(__name__)

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="Botica",
    user="postgres",
    password="1234567"  # cámbialo por tu contraseña real
)
cursor = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        comprador = request.form['comprador']
        producto = request.form['producto']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha = request.form['fecha']

        # INSERT con columnas explícitas (muy importante)
        cursor.execute("""
            INSERT INTO ventas (comprador, producto, cantidad, precio, fecha)
            VALUES (%s, %s, %s, %s, %s)
        """, (comprador, producto, cantidad, precio, fecha))
        conn.commit()

    # Obtener las ventas para mostrar en la tabla
    cursor.execute("SELECT * FROM ventas")
    ventas = cursor.fetchall()

    # Enviar HTML con datos y la fecha máxima
    return render_template('index.html', ventas=ventas, fecha_maxima=str(date.today()))

if __name__ == '__main__':
    app.run(debug=True)
