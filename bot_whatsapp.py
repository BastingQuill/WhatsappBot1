from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Diccionario para almacenar los puntos de cada usuario
puntos = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    msg = request.form.get("Body").strip()
    sender = request.form.get("WaId")  # Número de quien envió el mensaje
    nombre = request.form.get("ProfileName")  # Nombre del usuario en WhatsApp

    resp = MessagingResponse()
    respuesta = ""

    if msg.startswith("+1"):
        partes = msg.split()
        if len(partes) == 2:
            usuario = partes[1].replace("@", "").strip()
            puntos[usuario] = puntos.get(usuario, 0) + 1
            respuesta = f"✅ ¡Punto para {usuario}! 🎯\n\n🏆 Marcador actual:\n"
            respuesta += "\n".join([f"• {user}: {score} pts" for user, score in puntos.items()])
        else:
            respuesta = "❌ Formato incorrecto. Usa: +1 @nombre"
    
    elif msg == "!puntos":
        if puntos:
            respuesta = "📊 *Marcador actual:*\n"
            respuesta += "\n".join([f"• {user}: {score} pts" for user, score in puntos.items()])
        else:
            respuesta = "📊 Aún no hay puntos registrados."
    
    else:
        respuesta = "🤖 Comandos disponibles:\n• `+1 @nombre` → Agregar punto\n• `!puntos` → Ver marcador"
    
    resp.message(respuesta)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
