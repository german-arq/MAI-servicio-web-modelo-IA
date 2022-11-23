from flask import Flask, render_template, request, redirect, url_for
import json

import joblib

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    #return "Hello World"
    if request.method == 'POST':
        area = request.form['area']
        perimetro = request.form['perimetro']
        cantidad_vertices = request.form['cantidad_vertices']
        nivel = request.form['nivel']
        rmc_largo = request.form['rmc_largo']
        rmc_alto = request.form['rmc_alto']
        rmc_ratio = request.form['rmc_ratio']

        data = {'Area': area, 'Perimetro': perimetro, 'Cantidad de vertices': cantidad_vertices, 'Nivel': nivel, 'RMC Largo': rmc_largo, 'RMC Alto': rmc_alto, 'RMC Ratio': rmc_ratio}
        #data = [float(area), float(perimetro), float(cantidad_vertices), float(nivel), float(rmc_largo), float(rmc_alto), float(rmc_ratio)]

        return redirect(url_for('prediccion', data=json.dumps(data)))

    return render_template('input_form.html')

@app.route('/prediccion<data>')
def prediccion(data):
    # Ruta modelo para la prediccion en Local
    model = joblib.load('final_model.joblib')

    formated_data = json.loads(data)

    bien_data = [float(formated_data.get('Area')), float(formated_data.get('Perimetro')), int(formated_data.get('Cantidad de vertices')), float(formated_data.get('Nivel')), float(formated_data.get('RMC Largo')), float(formated_data.get('RMC Alto')), float(formated_data.get('RMC Ratio'))]

    prediccion = model.predict([bien_data])
    complemento = f"El Bien con características: {bien_data} es"
    respuesta = f"{complemento} PRIVADO" if prediccion[0] == 0 else f"{complemento} COMÚN"

    return respuesta


if __name__ == "__main__":
    app.run(debug=True)