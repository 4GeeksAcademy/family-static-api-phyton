from random import randint # Importa la función randint del módulo random. Esta función se utiliza para generar un número entero aleatorio dentro de un rango especificado. Aunque en el código presentado no se utiliza randint, generalmente se usaría para tareas como generar IDs aleatorios o números de la suerte.

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []

    def get_all_members(self):
        return self._members # Devuelve la lista completa de miembros de la familia

    def get_member(self, id):
        return next((m for m in self._members if m['id'] == id), None) # Busca un miembro por su id

    def add_member(self, member): # Agrega un nuevo miembro, asignando un id si no tiene
        if 'id' not in member:
            member['id'] = self._next_id
            self._next_id += 1
        member['last_name'] = self.last_name
        self._members.append(member)

    def delete_member(self, id): # Elimina un miembro por su id
        initial_length = len(self._members)
        self._members = [m for m in self._members if m['id'] != id]
        return len(self._members) < initial_length