# 🎬 Sistema de Venta de Boletos de Cine (CLI)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Universidad de El Salvador](https://img.shields.io/badge/Universidad%20de%20El%20Salvador-FMOcc-9D2235)](https://www.facebook.com/FMOccUES/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Proyecto de ciclo para la asignatura **Lógica de Programación Orientada a Objetos**  
**Universidad de El Salvador - Facultad Multidisciplinaria de Occidente**  
**Ingeniería en Desarrollo de Software**  
**Ciclo I - 2026**

---

## 📌 Descripción

Este proyecto consiste en el desarrollo de una aplicación de consola (CLI) utilizando Python, orientada a la gestión de venta de boletos de cine.

El sistema simula el funcionamiento básico de un cine, permitiendo administrar películas, salas, funciones y la compra de boletos, asegurando un control adecuado de los asientos disponibles.

---

## ⚙️ Funcionalidades principales

- Gestión de películas  
- Gestión de salas de cine  
- Creación de funciones (horarios por sala)  
- Compra de boletos  
- Control de asientos disponibles por función  
- Prevención de sobreventa  
- Validación de asientos únicos por cliente  


---

## 👥 Integrantes

- Daniel Enrique Menendez Gomez - MG13020
- Joel Isaias Garcia Torres - GT14001
- Paola Elizabeth Ascencio Barrientos - AA25001


---

## 🛠️ Requisitos

- Python 🐍

---
## 📁 Estructura del proyecto

```
📁 Estructura del proyecto

cine-boletos-cli/
├── docs/                              # Documentación y análisis del proyecto
│   ├── pseudocode/                    # Pseudocódigo de funcionalidades y flujos
│   └── srs/                           # Software Requirements Specification
│
├── src/                               # Código fuente principal
│   └── cine_boletos_cli/
│       ├── application/               # Casos de uso y lógica de aplicación
│       │   ├── dto/                   # Objetos de transferencia de datos
│       │   ├── services/              # Servicios de aplicación
│       │   └── use_cases/             # Casos de uso del sistema
│       │
│       ├── cli/                       # Interfaz de línea de comandos
│       │   ├── command_router.py      # Router principal de comandos
│       │   └── commands/              # Comandos CLI organizados por módulo
│       │
│       ├── domain/                    # Núcleo del dominio y reglas de negocio
│       │   ├── entities/              # Entidades principales del sistema
│       │   ├── exceptions/            # Excepciones oficiales del dominio
│       │   └── value_objects/         # Value Objects del dominio
│       │
│       ├── infrastructure/            # Infraestructura técnica del sistema
│       │   ├── idempotency/           # Manejo de idempotencia
│       │   ├── locking/               # Sistema de bloqueo de asientos
│       │   ├── logging/               # Logging centralizado
│       │   └── persistence/           # Persistencia y repositorios
│       │
│       ├── shared/                    # Componentes compartidos globalmente
│       │   ├── constants.py           # Constantes oficiales del sistema
│       │   └── utils.py               # Utilidades compartidas
│       │
│       ├── workers/                   # Workers y tareas asíncronas
│       │   ├── compensation_worker.py
│       │   ├── lock_expiry_worker.py
│       │   └── notification_worker.py
│       │
│       ├── main.py                    # Punto de entrada principal
│       └── __init__.py
│
├── tests/                             # Suite de pruebas
│   ├── concurrency/                   # Pruebas de concurrencia y locking
│   ├── integration/                   # Pruebas de integración
│   └── unit/                          # Pruebas unitarias
│
├── pyproject.toml                     # Configuración del proyecto y dependencias
├── uv.lock                            # Lockfile de dependencias
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🚧 Estado del proyecto

Este repositorio representa una versión inicial del proyecto.
Se irán agregando mejoras, nuevas funcionalidades, documentación y pruebas unitarias en futuras entregas.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT — ver el archivo LICENSE para más detalles.