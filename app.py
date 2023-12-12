from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Archivos de datos
initial_todos_file = "initial_todos.json"
todos_file = "todos.json"

# Cargar datos iniciales desde el archivo JSON
def cargar_todos():
    if os.path.exists(initial_todos_file):
        with open(initial_todos_file, "r") as json_file:
            return json.load(json_file)
    elif os.path.exists(todos_file):
        with open(todos_file, "r") as json_file:
            return json.load(json_file)
    else:
        return []

todos = cargar_todos()

def guardar_a_json():
    with open(todos_file, "w") as json_file:
        json.dump(todos, json_file)

@app.route("/todos", methods=["GET"])
def obtener_todos():
    try:
        # Guarda en el archivo JSON antes de enviar los datos
        guardar_a_json()
        return jsonify(todos)
    except Exception as e:
        return jsonify({"error": "No fue posible obtener las tareas"}), 500

@app.route("/todos", methods=["POST"])
def agregar_todo():
    try:
        nuevo_todo = request.get_json()
        todos.append(nuevo_todo)
        guardar_a_json()  # Guarda en el archivo JSON
        return jsonify(todos)
    except Exception as e:
        return jsonify({"error": "No fue posible agregar la tarea"}), 400

@app.route("/todos/<int:posicion>", methods=["DELETE"])
def eliminar_todo(posicion):
    try:
        if 0 <= posicion < len(todos):
            del todos[posicion]
            guardar_a_json()  # Guarda en el archivo JSON
            return jsonify(todos)
        else:
            return jsonify({"error": "Posición no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)






