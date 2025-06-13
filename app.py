from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
import io
from werkzeug.security import generate_password_hash
from flask_mysqldb import MySQL
from xhtml2pdf import pisa
from MySQLdb.cursors import DictCursor


app = Flask(__name__)
app.secret_key = 'clave_secreta'  

# Configuración de conexión a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotel_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('login.html')
#----------------------login-------------------------------------------

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s AND password = %s", (usuario, password))
    user = cur.fetchone()
    cur.close()

    if user:
        session['usuario'] = user[1]
        session['rol'] = user[3]
        return redirect(url_for('dashboard'))
    else:
        flash('Credenciales incorrectas', 'error')
        return redirect(url_for('home'))


#----------------------dashboard--------------------------------------------

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect('/')

    if session['rol'] == 'usuario':
        return render_template('dashboard_usuario.html') 
    elif session['rol'] == 'admin':

        cur = mysql.connection.cursor()



    cur.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cur.fetchone()[0]


    cur.execute("SELECT COUNT(*) FROM habitaciones WHERE estado = 'Disponible'")
    habitaciones_disponibles = cur.fetchone()[0]


    cur.execute("SELECT COUNT(*) FROM reservas WHERE estado = 'Activa'")
    reservas_activas = cur.fetchone()[0]


    cur.execute("""
        SELECT IFNULL(SUM(monto), 0) FROM pagos
        WHERE MONTH(fecha_pago) = MONTH(CURDATE()) AND YEAR(fecha_pago) = YEAR(CURDATE())
    """)
    ingresos_mes = cur.fetchone()[0]

    cur.close()

    return render_template(
        'dashboard.html',
        total_clientes=total_clientes,
        habitaciones_disponibles=habitaciones_disponibles,
        reservas_activas=reservas_activas,
        ingresos_mes=ingresos_mes
    )
#-----------------------------------------------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


#----------------clientes-----------------------------------

@app.route('/clientes')
def clientes():
    if 'usuario' in session and session.get('rol') == 'admin':

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM clientes")
        clientes = cur.fetchall()
        cur.close()
        return render_template('clientes.html', clientes=clientes)
    else:
        return redirect(url_for('home'))

@app.route('/clientes/nuevo')
def nuevo_cliente():
    if 'usuario' in session:
        return render_template('nuevo_cliente.html')
    else:
        return redirect(url_for('home'))

@app.route('/clientes/guardar', methods=['POST'])
def guardar_cliente():
    if 'usuario' in session:
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        dni = request.form['dni']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO clientes (nombre, email, telefono, dni) VALUES (%s, %s, %s, %s)",
                    (nombre, email, telefono, dni))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('clientes'))
    else:
        return redirect(url_for('home'))

#-------------------editar y eliminar---------------------------------------

@app.route('/clientes/editar/<int:id>')
def editar_cliente(id):
    if 'usuario' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id,))
        cliente = cur.fetchone()
        cur.close()
        return render_template('editar_cliente.html', cliente=cliente)
    else:
        return redirect(url_for('home'))

@app.route('/clientes/actualizar/<int:id>', methods=['POST'])
def actualizar_cliente(id):
    if 'usuario' in session:
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        dni = request.form['dni']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE clientes SET nombre=%s, email=%s, telefono=%s, dni=%s
            WHERE id_cliente=%s
        """, (nombre, email, telefono, dni, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('clientes'))
    else:
        return redirect(url_for('home'))

@app.route('/clientes/eliminar/<int:id>')
def eliminar_cliente(id):
    if 'usuario' in session and session.get('rol') == 'admin':

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM clientes WHERE id_cliente = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('clientes'))
    else:
        return redirect(url_for('home'))

#---------------habitaciones--------------------------------------------
@app.route('/habitaciones')
def habitaciones():
    if 'usuario' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM habitaciones")
        habitaciones = cur.fetchall()
        cur.close()
        return render_template('habitaciones.html', habitaciones=habitaciones)
    else:
        return redirect(url_for('home'))

@app.route('/habitaciones/nueva')
def nueva_habitacion():
    if 'usuario' in session:
        return render_template('nueva_habitacion.html')
    else:
        return redirect(url_for('home'))

@app.route('/habitaciones/guardar', methods=['POST'])
def guardar_habitacion():
    if 'usuario' in session:
        numero = request.form['numero']
        tipo = request.form['tipo']
        precio = request.form['precio']
        estado = request.form['estado']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO habitaciones (numero, tipo, precio, estado) VALUES (%s, %s, %s, %s)",
                    (numero, tipo, precio, estado))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('habitaciones'))
    else:
        return redirect(url_for('home'))
    
#---------------ediccion y eliminacion-----------------------------------
@app.route('/habitaciones/editar/<int:id>')
def editar_habitacion(id):
    if 'usuario' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM habitaciones WHERE id_habitacion = %s", (id,))
        habitacion = cur.fetchone()
        cur.close()
        return render_template('editar_habitacion.html', habitacion=habitacion)
    else:
        return redirect(url_for('home'))

@app.route('/habitaciones/actualizar/<int:id>', methods=['POST'])
def actualizar_habitacion(id):
    if 'usuario' in session:
        numero = request.form['numero']
        tipo = request.form['tipo']
        precio = request.form['precio']
        estado = request.form['estado']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE habitaciones SET numero=%s, tipo=%s, precio=%s, estado=%s
            WHERE id_habitacion=%s
        """, (numero, tipo, precio, estado, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('habitaciones'))
    else:
        return redirect(url_for('home'))

@app.route('/habitaciones/eliminar/<int:id>')
def eliminar_habitacion(id):
    if 'usuario' in session and session.get('rol') == 'admin':

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM habitaciones WHERE id_habitacion = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('habitaciones'))
    else:
        return redirect(url_for('home'))

#-----------------------reserva----------------------------------------
@app.route('/reservas')
def reservas():
    if 'usuario' in session:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT r.id_reserva, c.nombre, h.numero, r.fecha_inicio, r.fecha_fin, r.estado
            FROM reservas r
            JOIN clientes c ON r.cliente_id = c.id_cliente
            JOIN habitaciones h ON r.habitacion_id = h.id_habitacion
        """)
        reservas = cur.fetchall()
        cur.close()
        return render_template('reservas.html', reservas=reservas)
    else:
        return redirect(url_for('home'))

@app.route('/reservas/nueva')
def nueva_reserva():
    if 'usuario' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_cliente, nombre FROM clientes")
        clientes = cur.fetchall()
        cur.execute("SELECT id_habitacion, numero FROM habitaciones WHERE estado = 'Disponible'")
        habitaciones = cur.fetchall()
        cur.close()
        return render_template('nueva_reserva.html', clientes=clientes, habitaciones=habitaciones)
    else:
        return redirect(url_for('home'))

@app.route('/reservas/guardar', methods=['POST'])
def guardar_reserva():
    if 'usuario' in session:
        cliente_id = request.form['cliente_id']
        habitacion_id = request.form['habitacion_id']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reservas (cliente_id, habitacion_id, fecha_inicio, fecha_fin) VALUES (%s, %s, %s, %s)",
                    (cliente_id, habitacion_id, fecha_inicio, fecha_fin))
        cur.execute("UPDATE habitaciones SET estado = 'Ocupada' WHERE id_habitacion = %s", (habitacion_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('reservas'))
    else:
        return redirect(url_for('home'))

#--------------------------cancelar y editar--------------------------------------

@app.route('/reservas/editar/<int:id>')
def editar_reserva(id):
    if 'usuario' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id,))
        reserva = cur.fetchone()
        cur.execute("SELECT id_cliente, nombre FROM clientes")
        clientes = cur.fetchall()
        cur.execute("SELECT id_habitacion, numero FROM habitaciones")
        habitaciones = cur.fetchall()
        cur.close()
        return render_template('editar_reserva.html', reserva=reserva, clientes=clientes, habitaciones=habitaciones)
    else:
        return redirect(url_for('home'))

@app.route('/reservas/actualizar/<int:id>', methods=['POST'])
def actualizar_reserva(id):
    if 'usuario' in session:
        cliente_id = request.form['cliente_id']
        habitacion_id = request.form['habitacion_id']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        estado = request.form['estado']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE reservas SET cliente_id=%s, habitacion_id=%s, fecha_inicio=%s, fecha_fin=%s, estado=%s
            WHERE id_reserva=%s
        """, (cliente_id, habitacion_id, fecha_inicio, fecha_fin, estado, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('reservas'))
    else:
        return redirect(url_for('home'))

@app.route('/reservas/cancelar/<int:id>')
def cancelar_reserva(id):
    if 'usuario' in session:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE reservas SET estado = 'Cancelada' WHERE id_reserva = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('reservas'))
    else:
        return redirect(url_for('home'))

#------------------------pago----------------------------------------------------------
@app.route('/pagos')
def pagos():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT pagos.id_pago, pagos.monto, pagos.fecha_pago, pagos.metodo_pago,
               reservas.id_reserva, reservas.fecha_inicio, reservas.fecha_fin,
               clientes.nombre AS cliente_nombre, clientes.dni, clientes.email, clientes.telefono,
               habitaciones.numero AS numero_habitacion, habitaciones.tipo, habitaciones.precio
        FROM pagos
        JOIN reservas ON pagos.reserva_id = reservas.id_reserva
        JOIN clientes ON reservas.cliente_id = clientes.id_cliente
        JOIN habitaciones ON reservas.habitacion_id = habitaciones.id_habitacion
        ORDER BY pagos.id_pago DESC
    """)
    pagos = cur.fetchall()
    cur.close()
    return render_template('pagos.html', pagos=pagos)



@app.route('/pagos/nuevo')
def nuevo_pago():
    if 'usuario' in session:
        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT r.id_reserva, c.nombre, h.numero
            FROM reservas r
            JOIN clientes c ON r.cliente_id = c.id_cliente
            JOIN habitaciones h ON r.habitacion_id = h.id_habitacion
            WHERE r.estado = 'Activa'
        """)
        reservas = cur.fetchall()
        cur.close()
        return render_template('nuevo_pago.html', reservas=reservas)
    else:
        return redirect(url_for('home'))

@app.route('/pagos/guardar', methods=['POST'])
def guardar_pago():
    if 'usuario' in session:
        reserva_id = request.form['reserva_id']
        monto = request.form['monto']
        fecha_pago = request.form['fecha_pago']
        metodo_pago = request.form['metodo_pago']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pagos (reserva_id, monto, fecha_pago, metodo_pago) VALUES (%s, %s, %s, %s)",
                    (reserva_id, monto, fecha_pago, metodo_pago))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('pagos'))
    else:
        return redirect(url_for('home'))

#-------------------reportes------------------------------------
@app.route('/reportes')
def reportes():
    if 'usuario' in session and session.get('rol') == 'admin':
        
        cur = mysql.connection.cursor()

        # Reporte 1: Habitaciones ocupadas actualmente
        cur.execute("""
            SELECT h.numero, h.tipo, r.fecha_inicio, r.fecha_fin, c.nombre
            FROM reservas r
            JOIN habitaciones h ON r.habitacion_id = h.id_habitacion
            JOIN clientes c ON r.cliente_id = c.id_cliente
            WHERE CURDATE() BETWEEN r.fecha_inicio AND r.fecha_fin AND r.estado = 'Activa'
        """)
        habitaciones_ocupadas = cur.fetchall()

        # Reporte 2: Ingresos por mes
        cur.execute("""
            SELECT DATE_FORMAT(fecha_pago, '%Y-%m') as mes, SUM(monto) as total
            FROM pagos
            GROUP BY mes
            ORDER BY mes DESC
        """)
        ingresos_mensuales = cur.fetchall()

        cur.close()
        return render_template('reportes.html', habitaciones=habitaciones_ocupadas, ingresos=ingresos_mensuales)
    else:
        return redirect(url_for('home'))
    
#---------------------reporte en pdf---------------------------------------------------------------
@app.route('/reporte_pdf/<int:pago_id>')
def reporte_pdf(pago_id):
    cur = mysql.connection.cursor(DictCursor)


    query = """
        SELECT 
            pagos.id_pago, pagos.monto, pagos.fecha_pago,
            clientes.nombre AS cliente_nombre,
            habitaciones.numero, habitaciones.tipo, habitaciones.precio,
            reservas.fecha_inicio, reservas.fecha_fin
        FROM pagos
        JOIN reservas ON pagos.reserva_id = reservas.id_reserva
        JOIN clientes ON reservas.cliente_id = clientes.id_cliente
        JOIN habitaciones ON reservas.habitacion_id = habitaciones.id_habitacion
        WHERE pagos.id_pago = %s
    """
    cur.execute(query, (pago_id,))
    data = cur.fetchone()

    if not data:
        return "Pago no encontrado", 404

    rendered = render_template('factura_pdf.html', data=data)

    pdf = io.BytesIO()
    pisa_status = pisa.CreatePDF(rendered, dest=pdf)

    if pisa_status.err:
        return "Error al generar PDF", 500

    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=factura_pago_{pago_id}.pdf'

    return response

#--------------------------filtros------------------------------------------------
@app.route('/reservas/buscar', methods=['GET', 'POST'])
def buscar_reservas():
    if 'usuario' in session:
        resultados = []
        if request.method == 'POST':
            criterio = request.form['criterio']
            valor = request.form['valor']
            cur = mysql.connection.cursor()

            if criterio == 'cliente':
                cur.execute("""
                    SELECT r.id_reserva, c.nombre, h.numero, r.fecha_inicio, r.fecha_fin, r.estado
                    FROM reservas r
                    JOIN clientes c ON r.cliente_id = c.id_cliente
                    JOIN habitaciones h ON r.habitacion_id = h.id_habitacion
                    WHERE c.nombre LIKE %s
                """, ('%' + valor + '%',))
            elif criterio == 'habitacion':
                cur.execute("""
                    SELECT r.id_reserva, c.nombre, h.numero, r.fecha_inicio, r.fecha_fin, r.estado
                    FROM reservas r
                    JOIN clientes c ON r.cliente_id = c.id_cliente
                    JOIN habitaciones h ON r.habitacion_id = h.id_habitacion
                    WHERE h.numero LIKE %s
                """, ('%' + valor + '%',))
            elif criterio == 'fecha':
                cur.execute("""
                    SELECT r.id_reserva, c.nombre, h.numero, r.fecha_inicio, r.fecha_fin, r.estado
                    FROM reservas r
                    JOIN clientes c ON r.cliente_id = c.id_cliente
                    JOIN habitaciones h ON r.habitacion_id = h.id_habitacion
                    WHERE %s BETWEEN r.fecha_inicio AND r.fecha_fin
                """, (valor,))
            resultados = cur.fetchall()
            cur.close()
        return render_template('buscar_reservas.html', resultados=resultados)
    else:
        return redirect(url_for('home'))

#----------------------------------------------------------------------

@app.route('/habitaciones/disponibles')
def ver_habitaciones():
    if 'usuario' in session and session['rol'] == 'usuario':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM habitaciones WHERE estado = 'Disponible'")
        habitaciones = cur.fetchall()
        cur.close()
        return render_template('habitaciones_disponibles.html', habitaciones=habitaciones)
    return redirect(url_for('dashboard'))

#---------------------------registro-----------------------------------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        rol = request.form['rol']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nombre_usuario, password, rol) VALUES (%s, %s, %s)", 
                    (usuario, password, rol))
        mysql.connection.commit()
        cur.close()

        session['usuario'] = usuario
        session['rol'] = 'admin'

        return redirect(url_for('dashboard'))

    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)
