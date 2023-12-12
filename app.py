from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Archivo de datos principal
todos_file = "todos.json"

# Cargar o inicializar datos desde el archivo JSON principal
def cargar_o_inicializar_todos():
    if os.path.exists(todos_file):
        with open(todos_file, "r") as json_file:
            data = json.load(json_file)
            if not data:
                # Si el archivo existe pero está vacío, inicializa con tareas iniciales
                tareas_iniciales = [
                    {"done": True, "label": "Tarea inicial 1"},
                    {"done": True, "label": "Tarea inicial 2"}
                ]
                return tareas_iniciales
            return data
    else:
        # Si el archivo no existe, crea el archivo con tareas iniciales y devuelve esas tareas
        tareas_iniciales = [
            {"done": True, "label": "Tarea inicial 1"},
            {"done": True, "label": "Tarea inicial 2"}
        ]
        with open(todos_file, "w") as json_file:
            json.dump(tareas_iniciales, json_file)
        return tareas_iniciales

todos = cargar_o_inicializar_todos()

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

        # Validar que el campo 'label' no sea nulo
        if not nuevo_todo.get("label"):
            return jsonify({"error": "El campo 'label' no puede estar vacio"}), 400

        # Establecer automáticamente el estado de 'done' en True
        nuevo_todo["done"] = True

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
            return jsonify({"error": "Posicion no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)









