# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 13:40:22 2025

@author: abrah
"""

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

    if msg.startswith("+1"):
        partes = msg.split()
        if len(partes) == 2:
            usuario = partes[1].replace("@", "").strip()
            puntos[usuario] = puntos.get(usuario, 0) + 1
            respuesta = f"✅ ¡Punto para {usuario}! 🎯\n\n🏆 Marcador actual:\n"
            for user, score in puntos.items():
                respuesta += f"• {user}: {score} pts\n"
        else:
            respuesta = "❌ Formato incorrecto. Usa: +1 @nombre"

    elif msg == "!puntos":
        respuesta = "📊 *Marcador actual:*\n"
        for user, score in puntos.items():
            respuesta += f"• {user}: {score} pts\n"
        if not puntos:
            respuesta = "📊 Aún no hay puntos registrados."

    else:
        respuesta = "🤖 Comandos disponibles:\n• `+1 @nombre` → Agregar punto\n• `!puntos` → Ver marcador"

    resp.message(respuesta)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
