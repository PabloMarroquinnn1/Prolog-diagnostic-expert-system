# Doctor Byte — Prolog Diagnostic Expert System

Sistema experto para diagnóstico de fallas en computadoras. El usuario selecciona síntomas y el motor de inferencia en SWI-Prolog determina el diagnóstico con recomendaciones de solución.

Incluye interfaz web, panel de administración para gestionar la base de conocimiento (CRUD), historial de diagnósticos y notificaciones automáticas vía Telegram.

![Arquitectura](images/arquitectura.drawio.png)

## Tecnologías

| Componente | Tecnología |
|---|---|
| Motor de inferencia | SWI-Prolog |
| Backend / API | Python + Flask |
| Frontend | HTML, CSS, JavaScript |
| Bot | Telegram (python-requests) |
| Contenedores | Docker + docker-compose |

## Arquitectura

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │     │  Telegram    │     │    Admin      │
│  index.html  │     │    Bot       │     │  admin.html   │
└──────┬───────┘     └──────┬───────┘     └──────┬────────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │ HTTP
                   ┌────────▼────────┐
                   │   Flask API     │
                   │   (backend)     │
                   │                 │
                   │  routes/        │
                   │  services/      │
                   └────────┬────────┘
                            │ subprocess
                   ┌────────▼────────┐
                   │   SWI-Prolog    │
                   │                 │
                   │  doctor_byte.pl │
                   │  (base + CRUD)  │
                   └─────────────────┘
```

## Características

- **Diagnóstico inteligente:** Selección de síntomas → motor Prolog infiere el problema y sugiere soluciones
- **CRUD de conocimiento:** Agregar, editar y eliminar síntomas, diagnósticos y reglas desde el panel admin
- **Base de conocimiento dual:** Reglas base (read-only) + reglas dinámicas (gestionadas vía CRUD)
- **Historial:** Registro JSON de todos los diagnósticos realizados
- **Telegram Bot:** Notificaciones automáticas de cada diagnóstico al chat configurado
- **Dockerizado:** Levanta todo el sistema con un solo comando

## Instalación

### Requisitos

- Docker Desktop 4.x

### Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con tu token de Telegram y chat ID.

### Levantar el sistema

```bash
docker compose up -d
```

La interfaz web estará disponible en `http://localhost:5000`.

## Uso

1. Abrir `http://localhost:5000` en el navegador
2. Seleccionar los síntomas que presenta el equipo
3. Hacer clic en "Diagnosticar"
4. El sistema muestra el diagnóstico y las recomendaciones
5. El resultado se guarda en el historial y se notifica por Telegram

### Panel de administración

Acceder a `http://localhost:5000/admin` para:
- Ver y gestionar síntomas
- Ver y gestionar diagnósticos
- Crear nuevas reglas de diagnóstico
- Consultar el historial de diagnósticos

## Estructura del proyecto

```
├── docker-compose.yml        # Orquestación de servicios
├── Dockerfile.backend        # Imagen del backend Flask
├── Dockerfile.bot            # Imagen del bot de Telegram
├── .env.example              # Template de variables de entorno
├── backend/
│   ├── app.py                # Aplicación Flask principal
│   ├── routes/
│   │   ├── diagnose.py       # Endpoints de diagnóstico
│   │   ├── crud_routes.py    # Endpoints CRUD de conocimiento
│   │   └── history_routes.py # Endpoints de historial
│   ├── services/
│   │   ├── prolog_service.py      # Comunicación con SWI-Prolog
│   │   ├── prolog_crud_service.py # Gestión de archivos .pl
│   │   └── telegram_service.py    # Notificaciones Telegram
│   └── models/
│       └── history.py        # Gestión del historial JSON
├── frontend/
│   ├── templates/            # HTML (index + admin)
│   └── static/               # CSS + JS
├── prolog/
│   ├── doctor_byte_base.pl   # Base de conocimiento original
│   ├── doctor_byte_dynamic.pl # Reglas agregadas vía CRUD
│   └── doctor_byte.pl        # Unificador (base + dinámico)
├── telegram_bot/
│   └── bot.py                # Bot de Telegram
└── docs/
    ├── documento_tecnico.md  # Documentación técnica
    └── manual_usuario.md     # Guía de uso
```

## Documentación

- [Documento Técnico](docs/documento_tecnico.md) — Arquitectura, motor de inferencia, endpoints
- [Manual de Usuario](docs/manual_usuario.md) — Instalación y guía paso a paso

## Autor

**Pablo Alejandro Marroquin Cutz**
