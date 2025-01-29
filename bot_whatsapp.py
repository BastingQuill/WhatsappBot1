# -*- coding: utf-8 -*-
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Diccionario para almacenar los puntos de cada usuario
puntos = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    # Recibir el mensaje y los detalles del remitente
    msg = request.form.get("Body").strip()
    sender = request.form.get("WaId")  # Número de quien envió el mensaje
    nombre = request.form.get("ProfileName")  # Nombre del usuario en WhatsApp

    # Inicializar la respuesta
    resp = MessagingResponse()
    respuesta = ""

    # Comando para agregar puntos
    if msg.startswith("+1"):
        partes = msg.split()
        if len(partes) == 2 and partes[1].startswith("@"):
            usuario = partes[1].replace("@", "").strip()
            puntos[usuario] = puntos.get(usuario, 0) + 1
            respuesta = f"✅ ¡Punto para @{usuario}! 🎯\n\n🏆 *Marcador actual:*\n"
            for user, score in puntos.items():
                respuesta += f"• {user}: {score} pts\n"
        else:
            respuesta = "❌ *Formato incorrecto.* Usa: `+1 @nombre` para agregar un punto."

    # Comando para mostrar el marcador
    elif msg == "!puntos":
        if puntos:
            respuesta = "📊 *Marcador actual:*\n"
            for user, score in puntos.items():
                respuesta += f"• {user}: {score} pts\n"
        else:
            respuesta = "📊 *Aún no hay puntos registrados.*"

    # Respuesta por defecto con los comandos disponibles
    else:
        respuesta = "🤖 *Comandos disponibles:*\n"
        respuesta += "• `+1 @nombre` → *Agregar un punto* a un usuario\n"
        respuesta += "• `!puntos` → *Ver el marcador actual* de puntos.\n\n"
        respuesta += "*Ejemplo de uso:*\n"
        respuesta += "`+1 @Carlos` → Sumar un punto a Carlos."

    # Enviar la respuesta de vuelta
    resp.message(respuesta)
    return str(resp)

if __name__ == "__main__":
    # Ejecutar el servidor Flask
    app.run(debug=True)

