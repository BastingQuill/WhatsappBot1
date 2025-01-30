import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Nombre del archivo JSON donde se guardan los datos
JSON_FILE = "puntos.json"

# Cargar datos desde JSON si existe
def cargar_puntos():
    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Guardar datos en JSON
def guardar_puntos():
    with open(JSON_FILE, "w") as file:
        json.dump(puntos, file, indent=4)

# Diccionario de puntos cargado desde JSON
puntos = cargar_puntos()

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    msg = request.form.get("Body").strip()
    sender = request.form.get("WaId")
    nombre = request.form.get("ProfileName")

    resp = MessagingResponse()
    respuesta = ""

    # Agregar punto a un usuario
    if msg.startswith("+1"):
        partes = msg.split()
        if len(partes) == 2:
            usuario = partes[1].replace("@", "").strip()
            puntos[usuario] = puntos.get(usuario, 0) + 1
            guardar_puntos()
            respuesta = f"✅ ¡Se agregó un punto a {usuario}! 🎯\n\n🏆 Marcador actual:\n"
            respuesta += "\n".join([f"• {user}: {score} pts" for user, score in puntos.items()])
        else:
            respuesta = "❌ Error: Usa el formato: +1 @nombre"

    # Mostrar puntajes
    elif msg == "!puntos":
        if puntos:
            respuesta = "📊 *Marcador actual:*\n"
            respuesta += "\n".join([f"• {user}: {score} pts" for user, score in puntos.items()])
        else:
            respuesta = "📊 Aún no hay puntos registrados."

    # Modificar nombre de usuario
    elif msg.startswith("!modificar"):
        partes = msg.split()
        if len(partes) == 3:
            antiguo = partes[1].replace("@", "").strip()
            nuevo = partes[2].replace("@", "").strip()
            if antiguo in puntos:
                puntos[nuevo] = puntos.pop(antiguo)
                guardar_puntos()
                respuesta = f"🔄 ¡El nombre {antiguo} ahora es {nuevo}!"
            else:
                respuesta = f"❌ Error: No se encontró al usuario {antiguo}."
        else:
            respuesta = "❌ Error: Usa el formato: !modificar @antiguo_nombre @nuevo_nombre"

    # Corregir puntaje de un usuario
    elif msg.startswith("!corregir"):
        partes = msg.split()
        if len(partes) == 3:
            usuario = partes[1].replace("@", "").strip()
            try:
                nuevo_puntaje = int(partes[2])
                if usuario in puntos:
                    puntos[usuario] = nuevo_puntaje
                    guardar_puntos()
                    respuesta = f"✅ ¡Puntaje corregido! {usuario} tiene ahora {nuevo_puntaje} puntos."
                else:
                    respuesta = f"❌ Error: No se encontró al usuario {usuario}."
            except ValueError:
                respuesta = "❌ Error: El puntaje debe ser un número. Usa el formato: !corregir @nombre puntaje_nuevo"
        else:
            respuesta = "❌ Error: Usa el formato: !corregir @nombre puntaje_nuevo"

    else:
        respuesta = "🤖 *Comandos disponibles:*\n" \
                    "• `+1 @nombre` → Agregar un punto\n" \
                    "• `!puntos` → Ver el marcador\n" \
                    "• `!modificar @antiguo_nombre @nuevo_nombre` → Cambiar el nombre de un usuario\n" \
                    "• `!corregir @nombre puntaje_nuevo` → Corregir el puntaje de un usuario"

    resp.message(respuesta)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
