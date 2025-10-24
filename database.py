from typing import List, Dict, Any, Optional

# Simulación de la tabla de usuarios en PostGIS
DB_USERS: List[Dict[str, Any]] = []
next_id = 1

def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simula la inserción de un nuevo usuario, asignándole un ID."""
    global next_id
    
    new_user = {
        "id": next_id,
        "nombre": user_data["nombre"],
        "correo": user_data["correo"]
    }
    
    DB_USERS.append(new_user)
    next_id += 1
    
    return new_user

def get_all_users() -> List[Dict[str, Any]]:
    """Simula SELECT * FROM users;"""
    return DB_USERS

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Simula SELECT * FROM users WHERE id = user_id;"""
    for user in DB_USERS:
        if user["id"] == user_id:
            return user
    return None