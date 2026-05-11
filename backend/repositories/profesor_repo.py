# Repositorio para profesores
# Maneja las operaciones de base de datos relacionadas con profesores

class ProfesorRepository:
    def __init__(self, connection):
        self.connection = connection
    
    def obtener_todos(self):
        """Obtiene todos los profesores"""
        pass
    
    def obtener_por_id(self, profesor_id):
        """Obtiene un profesor por su ID"""
        pass
    
    def crear(self, profesor):
        """Crea un nuevo profesor"""
        pass
    
    def actualizar(self, profesor_id, datos):
        """Actualiza los datos de un profesor"""
        pass
    
    def eliminar(self, profesor_id):
        """Elimina un profesor"""
        pass
