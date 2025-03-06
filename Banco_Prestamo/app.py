from flask import Flask, render_template, request

app = Flask(__name__)

clientes = []

# Función para la evaluación de clientes no "primera vez"
def evaluar_cliente_no_primera_vez(cliente):
    bajo_riesgo = 0
    moderado_riesgo = 0
    alto_riesgo = 0

    if cliente["puntuacion_crediticia"] > 750:
        bajo_riesgo += 1
    elif 600 <= cliente["puntuacion_crediticia"] <= 750:
        moderado_riesgo += 1
    else:
        alto_riesgo += 1

    if cliente["ingresos_mensuales"] > 3 * cliente["cuota_prestamo"]:
        bajo_riesgo += 1
    elif 1.5 * cliente["cuota_prestamo"] <= cliente["ingresos_mensuales"] <= 3 * cliente["cuota_prestamo"]:
        moderado_riesgo += 1
    else:
        alto_riesgo += 1

    dti = cliente["deuda_actual"]
    if dti < 30:
        bajo_riesgo += 1
    elif 30 <= dti <= 50:
        moderado_riesgo += 1
    else:
        alto_riesgo += 1

    if cliente["tipo_empleo"] == "fijo_5_anios":
        bajo_riesgo += 1
    elif cliente["tipo_empleo"] == "fijo_menos5_anios":
        moderado_riesgo += 1
    else:
        alto_riesgo += 1

    if cliente["garantias"] == "propiedad":
        bajo_riesgo += 1
    elif cliente["garantias"] == "aval_bajo_valor":
        moderado_riesgo += 1
    else:
        alto_riesgo += 1

    if cliente["historial_prestamos"] == "sin_retrasos":
        bajo_riesgo += 1
    elif cliente["historial_prestamos"] == "retrasos_ocacionales":
        moderado_riesgo += 1
    else:
        alto_riesgo += 1

    if bajo_riesgo >= 5:
        return "Aprobado"
    elif alto_riesgo >= 5:
        return "Rechazado"
    else:
        return "Aprobación Condicional"

# Función para la evaluación de clientes "primera vez"
def evaluar_cliente_primera_vez(cliente):
    bajo_riesgo = 0
    alto_riesgo = 0

    if cliente["ingresos_mensuales"] > 3 * cliente["cuota_prestamo"]:
        bajo_riesgo += 1
    else:
        alto_riesgo += 1

    dti = cliente["deuda_actual"]
    if dti < 30:
        bajo_riesgo += 1
    else:
        alto_riesgo += 1

    if cliente["tipo_empleo"] == "fijo_5_anios":
        bajo_riesgo += 1
    else:
        alto_riesgo += 1

    if cliente["garantias"] == "propiedad":
        bajo_riesgo += 1
    else:
        alto_riesgo += 1

    if bajo_riesgo >= 4:
        return "Aprobado"
    elif alto_riesgo >= 3:
        return "Rechazado"
    else:
        return "Aprobación Condicional"

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nuevo_cliente = {
            "nombre": request.form["nombre"],
            "puntuacion_crediticia": int(request.form["puntuacion_crediticia"]),
            "ingresos_mensuales": int(request.form["ingresos_mensuales"]),
            "cuota_prestamo": int(request.form["cuota_prestamo"]),
            "deuda_actual": int(request.form["deuda_actual"]),
            "tipo_empleo": request.form["tipo_empleo"],
            "garantias": request.form["garantias"],
            "historial_prestamos": request.form["historial_prestamos"],
            "primera_vez": request.form["primera_vez"] == "True"
        }

        # Evaluar según si es primera vez o no
        if nuevo_cliente["primera_vez"]:
            nuevo_cliente["clasificacion"] = evaluar_cliente_primera_vez(nuevo_cliente)
        else:
            nuevo_cliente["clasificacion"] = evaluar_cliente_no_primera_vez(nuevo_cliente)

        clientes.append(nuevo_cliente)

    return render_template('index.html', resultados=clientes)

if __name__ == '__main__':
    app.run(debug=True)
