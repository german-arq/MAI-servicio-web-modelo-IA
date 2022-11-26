from flask import Flask, render_template, request, redirect, url_for
import json

import joblib
import boto3

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

    bien_data_for_endpoint = ",".join(str(x) for x in bien_data)
    bien_data_for_endpoint = bien_data_for_endpoint + "\n" + bien_data_for_endpoint

    print(bien_data)
    print(bien_data_for_endpoint)

    # Predicción con Endpoint SageMaker
    endpoint = 'sagemaker-scikit-learn-2022-11-25-23-15-58-775'
    client = boto3.client('sagemaker-runtime', 'us-east-1')

    response = client.invoke_endpoint(EndpointName=endpoint, Body=bien_data_for_endpoint, ContentType='text/csv')

    #print(response)

    # Devuelve un string con el valor de la predicción, entonces extraemos el segundo caracter que contiene el valor de la predicción y lo convertimos a entero
    prediccion = int(response['Body'].read().decode()[1:2])


    print(prediccion)

    # Predicción con modelo local
    #prediccion = model.predict([bien_data])


    complemento = f"El Bien con características: {bien_data} es"
    respuesta = f"{complemento} PRIVADO" if prediccion[0] == 0 else f"{complemento} COMÚN"

    return respuesta


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)