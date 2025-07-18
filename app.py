from flask import Flask, render_template, request
import psycopg2
import os
from datetime import date

app = Flask(__name__)

# URL de conexión de PostgreSQL en Render
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://botica_bd_user:pJ0E96luKaBjJ2QjhWU2MGCeYN8Cmzyh@dpg-d1ssm16r433s73emt7og-a.oregon-postgres.render.com/botica_bd'
)

@app.route('/', methods=['GET', 'POST'])
def registro():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

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

    cursor.close()
    conn.close()

    return render_template('index.html', ventas=ventas, fecha_maxima=str(date.today()))

if __name__ == '__main__':
    app.run(debug=True)
