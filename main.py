from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field # <<< AÑADE 'Field' AQUÍ
from typing import List, Tuple, Literal, Optional, Dict, Any
from database import create_user, get_all_users, get_user_by_id

app = FastAPI(title="CRUD Básico")

# Configuración CORS
origins = ["http://localhost:5173", "http://127.0.0.1:5173"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------
# MODELOS PYDANTIC
# ----------------------------------------------------------------------

# Modelo de datos que el frontend ENVÍA (sólo nombre y correo)
class UserIn(BaseModel):
    nombre: str = Field(..., description="Nombre del usuario.")
    correo: EmailStr = Field(..., description="Correo del usuario.") # EmailStr valida el formato

# Modelo de datos que el frontend RECIBE (con ID)
class UserOut(BaseModel):
    id: int = Field(..., description="ID asignado por la BD.")
    nombre: str
    correo: EmailStr

# ----------------------------------------------------------------------
# ENDPOINTS
# ----------------------------------------------------------------------

# 1. Endpoint POST (CREATE)
@app.post("/api/users", response_model=UserOut)
async def create_new_user(user_data: UserIn):
    """Crea un nuevo usuario."""
    new_user_data = user_data.model_dump(by_alias=True)
    new_user = create_user(new_user_data)
    return UserOut(**new_user)

# 2. Endpoint GET ALL (READ ALL)
@app.get("/api/users", response_model=List[UserOut])
async def list_users():
    """Lista todos los usuarios."""
    db_data = get_all_users()
    return [UserOut(**u) for u in db_data]

# 3. Endpoint GET ONE (READ ONE)
@app.get("/api/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    """Obtiene un usuario por ID."""
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserOut(**user)