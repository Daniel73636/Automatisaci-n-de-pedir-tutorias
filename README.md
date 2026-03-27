# 🤖 Automatización de Pedido de Tutorías - UPB

Este proyecto es un bot de automatización desarrollado en **Python** utilizando **Selenium WebDriver**. Su objetivo es agilizar el proceso de inscripción en el formulario de tutorías de la Universidad Pontificia Bolivariana (UPB), permitiendo programar múltiples sesiones de forma masiva y precisa.

## 🚀 Características

- **Gestión Multi-Tutoría:** Permite agendar una lista completa de tutorías (Lunes a Domingo) en una sola ejecución.
- **Interacción Avanzada:** Simulación de movimientos de mouse (ActionChains) para manejar menús desplegables complejos de Google Forms.
- **Soporte para Materias Externas:** Lógica específica para detectar y llenar el campo "Otro" (ej. Ofimática).
- **Personalización de Observaciones:** Capacidad de enviar mensajes específicos a tutores (ej. solicitudes para Daniel Patiño).
- **Diseño Robusto:** Uso de esperas explícitas y selectores dinámicos para evitar errores de carga de página.

## 🛠️ Requisitos Técnicos

Para ejecutar este bot, necesitas tener instalado:

1. **Python 3.10+**
2. **Google Chrome** (Actualizado)
3. **Librerías de Python:**
   ```bash
   pip install selenium webdriver-manager
````

## 📂 Estructura del Proyecto

  - `main.py`: Código fuente principal con la lógica del bot y el calendario de tutorías.
  - `.gitignore`: Configuración para evitar subir archivos basura (como `.venv` o `__pycache__`).
  - `README.md`: Documentación del proyecto.

## ⚙️ Configuración

Dentro de `main.py`, puedes encontrar dos diccionarios principales:

  - `DATOS_FIJOS`: Contiene tu información personal (Nombre, ID, Correo UPB).
  - `TUTORIAS_PARA_ENVIAR`: Una lista donde puedes agregar o quitar las tutorías de la semana, definiendo día, materia, tema y horario exacto.

## 🛡️ Notas de Seguridad

Este script fue creado con fines académicos para la facultad de **Ingeniería de Sistemas**. Se recomienda no compartir datos sensibles en repositorios públicos.

-----

**Desarrollado por:** [Daniel Montiel](https://www.google.com/search?q=https://github.com/Daniel73636)  
**Institución:** Universidad Pontificia Bolivariana (UPB)  
**Semestre:** 3° - Ingeniería de Sistemas
