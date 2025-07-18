from flask import Flask, render_template, request
import psycopg2
from urllib.parse import urlparse
import os
from datetime import date

app = Flask(__name__)

# URL de Render - reemplaza esta por tu propia URL
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://botica_bd_user:pJ0E96luKaBjJ2QjhWU2MGCeYN8Cmzyh@dpg-d1ssm16r433s73emt7og-a.oregon-postgres.render.com/botica_bd')

# Conexión a la base de datos
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        comprador = request.form['comprador']
        producto = request.form['producto']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha = request.form['fecha']

        cursor.execute("""
            INSERT INTO ventas (comprador, producto, cantidad, precio, fecha)
            VALUES (%s, %s, %s, %s, %s)
        """, (comprador, producto, cantidad, precio, fecha))
        conn.commit()

    cursor.execute("SELECT * FROM ventas")
    ventas = cursor.fetchall()

    return render_template('index.html', ventas=ventas, fecha_maxima=str(date.today()))

if __name__ == '__main__':
    app.run(debug=True)
