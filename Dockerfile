# 1. Usar una imagen oficial de Python como base
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar los archivos de requerimientos e instalarlos
# (En nuestro caso simple, instalamos directamente)
RUN pip install fastapi "uvicorn[standard]"

# 4. Copiar el código de la aplicación al contenedor
COPY ./main.py /app/

# 5. Exponer el puerto en el que correrá la aplicación
EXPOSE 8000

# 6. El comando para iniciar la aplicación cuando el contenedor arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]