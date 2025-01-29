from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    msg = request.form.get("Body").strip()  # Mensaje recibido
    sender = request.form.get("WaId")  # Número del remitente
    nombre = request.form.get("ProfileName")  # Nombre del usuario de WhatsApp

    # Crear respuesta
    resp = MessagingResponse()

    if msg:
        respuesta = f"✅ ¡Mensaje recibido! {msg}\n\n*¡Gracias por probar el bot!* 🎉"
    else:
        respuesta = "❌ *No se recibió mensaje.*"

    # Enviar la respuesta
    resp.message(respuesta)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
