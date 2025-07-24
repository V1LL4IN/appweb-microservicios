import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import uuid # Usaremos uuid para generar IDs únicos

# 1. Creamos la aplicación FastAPI
app = FastAPI(
    title="Microservicio de Canciones",
    description="Un microservicio para realizar operaciones CRUD sobre canciones.",
    version="1.0.0",
)

# 2. Definimos el modelo de datos para una canción usando Pydantic
# Esto asegura que los datos que recibimos tengan el formato correcto.
class Song(BaseModel):
    id: Optional[str] = None # El ID será opcional, lo generaremos en el servidor
    name: str
    path: str
    plays: int

# 3. Creamos nuestra "base de datos" en memoria.
# Es una lista simple que almacenará las canciones como diccionarios.
db: List[Song] = [
    Song(id=str(uuid.uuid4()), name="Bohemian Rhapsody", path="/songs/bohemian.mp3", plays=1000),
    Song(id=str(uuid.uuid4()), name="Hotel California", path="/songs/hotel.mp3", plays=500)
]

# 4. Endpoints de la API

# Endpoint para crear una nueva canción (Create)
@app.post("/songs", response_model=Song, status_code=status.HTTP_201_CREATED, summary="Crear una nueva canción")
def create_song(song: Song):
    """
    Crea una nueva canción y la añade a la base de datos.
    - **name**: Nombre de la canción.
    - **path**: Ruta o URL del archivo de la canción.
    - **plays**: Número de reproducciones inicial.
    """
    song.id = str(uuid.uuid4()) # Generamos un ID único
    db.append(song)
    return song

# Endpoint para obtener todas las canciones (Read)
@app.get("/songs", response_model=List[Song], status_code=status.HTTP_200_OK, summary="Obtener todas las canciones")
def get_songs():
    """
    Retorna una lista de todas las canciones en la base de datos.
    """
    return db

# Endpoint para obtener una canción por su ID (Read)
@app.get("/songs/{song_id}", response_model=Song, status_code=status.HTTP_200_OK, summary="Obtener una canción por ID")
def get_song(song_id: str):
    """
    Busca y retorna una canción específica por su ID.
    Si no la encuentra, retorna un error 404.
    """
    for song in db:
        if song.id == song_id:
            return song
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Canción no encontrada")

# Endpoint para actualizar una canción (Update)
@app.put("/songs/{song_id}", response_model=Song, status_code=status.HTTP_200_OK, summary="Actualizar una canción")
def update_song(song_id: str, updated_song: Song):
    """
    Actualiza los datos de una canción existente.
    Busca la canción por su ID y reemplaza sus datos con los proporcionados.
    """
    for index, song in enumerate(db):
        if song.id == song_id:
            # Mantenemos el ID original y actualizamos el resto de los campos
            updated_song.id = song_id
            db[index] = updated_song
            return updated_song
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Canción no encontrada")

# Endpoint para eliminar una canción (Delete)
@app.delete("/songs/{song_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar una canción")
def delete_song(song_id: str):
    """
    Elimina una canción de la base de datos por su ID.
    """
    for index, song in enumerate(db):
        if song.id == song_id:
            db.pop(index)
            # El código 204 no debe retornar contenido en el body.
            # FastAPI se encarga de esto automáticamente.
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Canción no encontrada")

# Esto es para poder ejecutar el archivo directamente con `python main.py` si quisiéramos
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)