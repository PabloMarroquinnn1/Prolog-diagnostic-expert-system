# Doctor Byte - Manual de Usuario
## Inteligencia Artificial 1 - USAC 2026

**Estudiante:** Pablo Alejandro Marroquin Cutz  
**Carnet:** 202200214  
**Fecha:** Junio 2026  

---

## 1. Requisitos previos

- Python 3.11+
- SWI-Prolog 10+
- Docker (opcional)
- Navegador web moderno (Chrome, Edge o Firefox)

---

## 2. Instalación y ejecución local

### Paso 1 — Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd FASE1
```

### Paso 2 — Instalar dependencias
```bash
pip install -r backend/requirements.txt
```

### Paso 3 — Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```
TELEGRAM_TOKEN=tu_token_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui
SWI_HOME_DIR=C:\Program Files\swipl
```

### Paso 4 — Levantar el backend
```bash
# Windows
$env:SWI_HOME_DIR = "C:\Program Files\swipl"
python -m backend.app
```

### Paso 5 — Abrir el frontend
```bash
# Windows
start frontend\templates\index.html
```

### Paso 6 — Levantar el bot de Telegram (opcional)
```bash
python telegram_bot\bot.py
```

---

## 3. Ejecución con Docker

```bash
docker compose up --build
```

---

## 4. Uso del sistema

### 4.1 Realizar un diagnóstico desde el frontend

1. Abrir `frontend/templates/index.html` en el navegador
2. Seleccionar los síntomas que presenta el equipo haciendo clic en los chips
3. Presionar el botón **Diagnosticar**
4. Ver los resultados con porcentaje de coincidencia, barra de progreso y recomendaciones
5. El diagnóstico se guarda en el historial y se envía automáticamente al bot de Telegram


### 4.2 Ver historial de diagnósticos

1. Después de un diagnóstico presionar **Ver historial**
2. Se muestran dos gráficas:
   - **Dona**: fallas más frecuentes detectadas
   - **Barras**: cantidad de diagnósticos por fecha
3. Se listan todos los diagnósticos con fecha, falla principal y síntomas

### 4.3 Limpiar selección

- Presionar **Limpiar** para deseleccionar todos los síntomas

### 4.4 Nuevo diagnóstico

- Desde la pantalla de resultados presionar **Nuevo diagnóstico**

---

## 5. Bot de Telegram

### 5.1 Configuración inicial

1. Buscar el bot en Telegram por su username
2. Presionar **START** o enviar `/start`
3. El bot responderá con el menú de comandos

### 5.2 Comandos disponibles

| Comando | Descripción |
|---|---|
| /start | Iniciar el bot y ver comandos |
| /diagnosticar | Iniciar diagnóstico interactivo |
| /sintomas | Ver lista de síntomas disponibles con sus IDs |
| /historial | Ver los últimos 5 diagnósticos realizados |
| /listo | Finalizar selección de síntomas y obtener diagnóstico |
| /cancelar | Cancelar operación actual |

### 5.3 Realizar un diagnóstico por Telegram

1. Enviar `/diagnosticar`
2. El bot muestra la lista de síntomas disponibles con sus IDs
3. Escribir el ID de cada síntoma uno por uno (ejemplo: `pantalla_azul`)
4. El bot confirma cada síntoma agregado
5. Cuando termines enviar `/listo`
6. El bot responde con los 3 principales diagnósticos

### 5.4 Notificaciones automáticas

Cada vez que se realiza un diagnóstico desde el frontend, el bot envía automáticamente una notificación con:
- Número de diagnóstico y fecha
- Síntomas reportados
- Diagnóstico principal con porcentaje
- Recomendación

---

## 6. CRUD de síntomas y fallas

### 6.1 Crear un síntoma nuevo

```bash
POST http://127.0.0.1:5000/api/crud/sintomas
Content-Type: application/json

{"id": "nuevo_sintoma", "nombre": "Nombre del síntoma"}
```

### 6.2 Eliminar un síntoma

```bash
DELETE http://127.0.0.1:5000/api/crud/sintomas/nuevo_sintoma
```

### 6.3 Crear una falla nueva

```bash
POST http://127.0.0.1:5000/api/crud/fallas
Content-Type: application/json

{
  "id": "nueva_falla",
  "nombre": "Nombre de la falla",
  "sintomas": ["sintoma1", "sintoma2"],
  "recomendacion": "Pasos para resolver la falla"
}
```

### 6.4 Actualizar una falla

```bash
PUT http://127.0.0.1:5000/api/crud/fallas/nueva_falla
Content-Type: application/json

{
  "nombre": "Nombre actualizado",
  "sintomas": ["sintoma1", "sintoma3"],
  "recomendacion": "Recomendación actualizada"
}
```

### 6.5 Eliminar una falla

```bash
DELETE http://127.0.0.1:5000/api/crud/fallas/nueva_falla
```

---

## 7. Solución de problemas

| Problema | Causa | Solución |
|---|---|---|
| Error `SWI_HOME_DIR` | Variable de entorno no configurada | Ejecutar `$env:SWI_HOME_DIR = "C:\Program Files\swipl"` |
| Frontend no carga síntomas | Backend no está corriendo | Verificar que el backend esté en el puerto 5000 |
| Bot no responde | Token incorrecto o no configurado | Verificar el `.env` con el token de BotFather |
| Error de CORS | Flask-CORS no instalado | Ejecutar `pip install flask-cors` |
| Access violation en pyswip | DLL de Prolog no encontrada | Configurar `SWI_HOME_DIR` correctamente |
| Síntomas no se unifican | Archivos Prolog desincronizados | El backend regenera el unificador automáticamente al usar el CRUD |
