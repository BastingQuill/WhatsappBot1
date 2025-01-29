import os
import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Ruta del archivo JSON para almacenar los puntos
os.makedirs("data", exist_ok=True)
PUNTOS_FILE = "data/puntos.json"

# Cargar puntos desde el archivo si existe
def cargar_puntos():
    if os.path.exists(PUNTOS_FILE):
        with open(PUNTOS_FILE, "r") as f:
            return json.load(f)
    return {}

# Guardar puntos en el archivo
def guardar_puntos():
    with open(PUNTOS_FILE, "w") as f:
        json.dump(puntos, f, indent=4)

puntos = cargar_puntos()

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    msg = request.form.get("Body").strip()
    sender = request.form.get("WaId")
    nombre = request.form.get("ProfileName")

    resp = MessagingResponse()
    respuesta = ""

    if msg.startswith("+1"):
        partes = msg.split()
        if len(partes) == 2:
            usuario = partes[1].replace("@", "").strip()
            puntos[usuario] = puntos.get(usuario, 0) + 1
            guardar_puntos()
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
    
    elif msg.startswith("!modificar"):  # Modificar nombre
        partes = msg.split()
        if len(partes) == 3:
            antiguo, nuevo = partes[1], partes[2]
            if antiguo in puntos:
                puntos[nuevo] = puntos.pop(antiguo)
                guardar_puntos()
                respuesta = f"🔄 {antiguo} ahora es {nuevo}."
            else:
                respuesta = "❌ Nombre no encontrado."
        else:
            respuesta = "❌ Formato incorrecto. Usa: !modificar antiguo nuevo"
    
    elif msg.startswith("!corregir"):  # Corregir puntaje
        partes = msg.split()
        if len(partes) == 3:
            usuario = partes[1]
            try:
                nuevo_puntaje = int(partes[2])
                if usuario in puntos:
                    puntos[usuario] = nuevo_puntaje
                    guardar_puntos()
                    respuesta = f"✅ Puntaje corregido para {usuario}: {nuevo_puntaje} pts."
                else:
                    respuesta = "❌ Usuario no encontrado."
            except ValueError:
                respuesta = "❌ Formato incorrecto. Usa: !corregir @nombre puntaje"
        else:
            respuesta = "❌ Formato incorrecto. Usa: !corregir @nombre puntaje"
    
    else:
        respuesta = ("🤖 Comandos disponibles:\n"
                     "• `+1 @nombre` → Agregar punto\n"
                     "• `!puntos` → Ver marcador\n"
                     "• `!modificar antiguo nuevo` → Cambiar nombre\n"
                     "• `!corregir @nombre puntaje` → Corregir puntaje")
    
    resp.message(respuesta)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
