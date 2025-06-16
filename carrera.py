#Materia: Sistemas Distribuidos
#Autor: Diego Valdes Castillo
#Fecha de  creacion: 01/04/2025
#Version: 1.0
#Practica 6 - Servicios Web
#Codigo de la carrera en pyhton - flask

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Estado de la carrera
race_status = {
    "cars": {},  # Se inicializa vacio para registrar autos dinamicamente
    "max_distance": 100,
    "podium": []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_car():
    """Registra un nuevo auto en la carrera."""
    car_id = request.json.get('car_id')
    if not car_id:
        return jsonify({"error": "Debes proporcionar un ID de auto"}), 400
    if car_id in race_status["cars"]:
        return jsonify({"error": "El auto ya esta registrado"}), 400
    
    race_status["cars"][car_id] = {"position": 0}
    return jsonify({"message": f"Auto {car_id} registrado exitosamente"})

@app.route('/move', methods=['POST'])
def move_car():
    """Mueve un auto basado en una solicitud POST."""
    if len(race_status["cars"]) < 4:
        return jsonify({"error": "La carrera iniciara cuando haya 4 autos registrados"}), 400
    
    car_id = request.json.get('car_id')
    distance = request.json.get('distance', 5)
    
    if car_id not in race_status["cars"]:
        return jsonify({"error": "Carro no registrado"}), 400
    
    if car_id in race_status["podium"]:
        return jsonify({"error": "Este auto ya termino la carrera"}), 400
    
    race_status["cars"][car_id]["position"] += distance
    if race_status["cars"][car_id]["position"] >= race_status["max_distance"]:
        race_status["cars"][car_id]["position"] = race_status["max_distance"]
        race_status["podium"].append(car_id)
    
    return jsonify({"message": f"{car_id} avanzo {distance} metros", "position": race_status["cars"][car_id]["position"]})

@app.route('/race_status', methods=['GET'])
def get_race_status():
    """Devuelve el estado actual de la carrera."""
    return jsonify(race_status)

@app.route('/podium', methods=['GET'])
def get_podium():
    """Devuelve el podio final."""
    if len(race_status["podium"]) == 4:
        return jsonify({"podium": race_status["podium"]})
    return jsonify({"message": "La carrera aun no ha terminado"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
