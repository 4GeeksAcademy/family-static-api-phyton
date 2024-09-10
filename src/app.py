import os # Importe que proporciona funciones para interactuar con el sistema operativo, como acceder a variables de entorno
from flask import Flask, request, jsonify # La clase principal de Flask para crear una aplicación web. Request: Permite acceder a los datos enviados en la solicitud HTTP (por ejemplo, datos enviados por POST). Jsonify: Convierte datos en formato JSON para enviarlos como respuesta HTTP.
from flask_cors import CORS # Importa CORS, que permite que el frontend (como JavaScript) haga peticiones a tu backend sin problemas de seguridad relacionados con el mismo origen (Cross-Origin Resource Sharing).

app = Flask(__name__) # Instancia de la aplicación Flask. __name__ se usa para que Flask conozca el nombre del módulo actual
app.url_map.strict_slashes = False # Permite que la URL funcione igual si termina o no con una barra /
CORS(app) # Habilita CORS para la aplicación, permitiendo que el frontend interactúe con el backend

class FamilyStructure:
    def __init__(self, last_name): # Método inicializador de la clase que se ejecuta cuando se crea una instancia
        self.last_name = last_name
        self._next_id = 1 # Inicializa un contador de ID que comenzará en 1 y se incrementará cada vez que se añada un nuevo miembro a la familia
        self._members = [ 
            {"id": 1, "first_name": "John", "last_name": "Jackson", "age": 33, "lucky_numbers": [7, 13, 22]},
            {"id": 2, "first_name": "Jane", "last_name": "Jackson", "age": 35, "lucky_numbers": [10, 14, 3]},
            {"id": 3, "first_name": "Tommy", "last_name": "Jackson", "age": 23, "lucky_numbers": [1]},
        ]

    def get_all_members(self): # Devuelve la lista completa de miembros de la familia
        return self._members

    def get_member(self, id):
        return next((m for m in self._members if m['id'] == id), None) # Busca en la lista members un miembro que su id coincida y devuelve el primero encontrado, o None si no existe

    def add_member(self, member):
        # Agrega un nuevo miembro, asignando un id si no tiene
        if 'id' not in member:
            member['id'] = self._next_id # Asigna el próximo id disponible al miembro
            self._next_id += 1 # Incrementa el contador de IDs para el siguiente miembro
        member['last_name'] = self.last_name #  Añade el apellido de la familia al miembro
        self._members.append(member) # Añade el miembro a la lista members
 
    def delete_member(self, id): 
        initial_length = len(self._members)  # Calcula la longitud actual de la lista _members y la almacena en initial_length
        self._members = [m for m in self._members if m['id'] != id]  # Crea una nueva lista que excluye el miembro con el id dado
        return len(self._members) < initial_length  # Retorna True si se eliminó un miembro, si no False

# Instancia de la familia Jackson
jackson_family = FamilyStructure("Jackson")

@app.route('/members', methods=['GET']) # Define la ruta /members que responde a las solicitudes GET
def get_all_members():
    return jsonify(jackson_family.get_all_members()), 200 # Devuelve los miembros en formato JSON y un código de estado 200 (OK)


@app.route('/member/<int:member_id>', methods=['GET']) 
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"message": "Member not found"}), 404 # Verifica si el miembro existe y devuelve el miembro o un error 404
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def add_member():
    member_data = request.get_json()
    if not member_data or 'first_name' not in member_data or 'age' not in member_data or 'lucky_numbers' not in member_data: # Verifica si los datos enviados son válidos y, si lo son, agrega al miembro
        return jsonify({"message": "Invalid input: missing required fields"}), 400
    
    jackson_family.add_member(member_data)
    return jsonify(member_data), 200 # Cambia a 200 si los requisitos así lo indican

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return jsonify({"done": True}), 200
    return jsonify({"message": "Member not found"}), 404

if __name__ == '__main__': # Ejecuta la aplicación solo si el archivo se ejecuta directamente.
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000)) #  Inicia la aplicación Flask en el puerto especificado (por defecto, 5000)
