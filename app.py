from flask import Flask, render_template, request
import psycopg2
from datetime import date
import urllib.parse as up

app = Flask(__name__)

# 🔗 CONEXIÓN A POSTGRESQL EN RENDER
try:
    conn = psycopg2.connect(
        dbname="botica_bd_bq72",
        user="botica_bd_bq72_user",
        password="WfYYqBZ5Bi8obQpGicatlM8rCadb0UF8",
        host="dpg-d1t5ia3ipnbc7385jjug-a.oregon-postgres.render.com",
        port="5432"
    )
    cursor = conn.cursor()
except Exception as e:
    print("❌ Error de conexión:", e)
    conn = None
    cursor = None

@app.route('/', methods=['GET', 'POST'])
def registro():
    mensaje = None

    try:
        cursor.execute("SELECT id, nombre FROM clientes")
        clientes = cursor.fetchall()

        cursor.execute("SELECT id, nombre FROM productos")
        productos = cursor.fetchall()
    except Exception as e:
        clientes = []
        productos = []
        mensaje = f"❌ Error al cargar datos: {str(e)}"

    if request.method == 'POST':
        try:
            cliente_id = int(request.form['cliente'])
            producto_id = int(request.form['producto'])
            cantidad = int(request.form['cantidad'])
            precio = float(request.form['precio'])
            fecha = request.form['fecha']

            cursor.execute("""
                INSERT INTO ventas (cliente_id, producto_id, cantidad, precio, fecha)
                VALUES (%s, %s, %s, %s, %s)
            """, (cliente_id, producto_id, cantidad, precio, fecha))
            conn.commit()
            mensaje = "✅ Registro exitoso"
        except Exception as e:
            conn.rollback()
            mensaje = f"❌ Error al registrar: {str(e)}"
            print("ERROR:", e)

    try:
        cursor.execute("""
            SELECT v.id, c.nombre AS cliente, p.nombre AS producto, v.cantidad, v.precio, v.fecha
            FROM ventas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN productos p ON v.producto_id = p.id
            ORDER BY v.fecha DESC
        """)
        ventas = cursor.fetchall()
    except Exception as e:
        ventas = []
        mensaje = f"❌ Error al cargar ventas: {str(e)}"

    return render_template('index.html',
                           ventas=ventas,
                           clientes=clientes,
                           productos=productos,
                           mensaje=mensaje,
                           fecha_maxima=str(date.today()))

if __name__ == '__main__':
    app.run(debug=True)
