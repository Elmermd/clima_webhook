from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
API_KEY = '3d7e46d81d2a88ca2a59495a060ee8d9'

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    print("Petición recibida desde Dialogflow:")
    print(req)

    parameters = req.get('sessionInfo', {}).get('parameters', {})
    ciudad = parameters.get('ciudad', '')
    fecha = parameters.get('fecha', '')

    if not ciudad:
        texto = "No entendí en qué ciudad deseas saber el clima."
    elif "mañana" in fecha.lower():
        texto = f"Por ahora solo puedo darte el clima actual en {ciudad}, no el de mañana."
    else:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es'
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            desc = data['weather'][0]['description']
            temp = data['main']['temp']
            texto = f"Hoy en {ciudad} está {desc} con {temp:.1f}°C."
        else:
            texto = f"No pude obtener el clima para {ciudad}. ¿Podrías revisar el nombre?"

    return jsonify({
        "fulfillment_response": {
            "messages": [{"text": {"text": [texto]}}]
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
