# Gestor de Alumnos con Tkinter

Aplicación de escritorio desarrollada con **Tkinter** y **SQLite** para gestionar un listado de alumnos. La interfaz replica el estilo de las capturas provistas originalmente: un `Treeview` con los registros, botones que cambian de estado según el flujo de trabajo y un formulario para editar los campos principales.

## Requisitos

- Python 3.11 o superior (se recomienda la misma versión utilizada en el desarrollo)
- Dependencias estándar de la biblioteca (`tkinter`, `sqlite3`, `pathlib`), disponibles por defecto en Python.

## Estructura del proyecto

```
.
├── alumnos_app.py   # Aplicación principal con la interfaz y el CRUD completo
├── crearBase.py     # Script auxiliar para inicializar la base de datos SQLite
└── README.md        # Este archivo
```

## Puesta en marcha

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/<usuario>/tkinter_CDEIA.git
   cd tkinter_CDEIA
   ```

2. **(Opcional) Crear un entorno virtual**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. **Inicializar la base de datos**
   Ejecuta el script que crea la tabla `alumnos` si aún no existe:
   ```bash
   python crearBase.py
   ```

4. **Iniciar la aplicación**
   ```bash
   python alumnos_app.py
   ```

La base de datos se guarda en el archivo `alumnos.db` en la raíz del proyecto. Si deseas restablecerla, elimina ese archivo y vuelve a ejecutar `crearBase.py`.

## Características principales

- `Treeview` con columnas para nombre, domicilio, DNI y edad.
- Botones con estados dinámicos (habilitado/deshabilitado) según la acción disponible.
- Operaciones CRUD completas: crear, listar, actualizar y eliminar alumnos.
- Validaciones básicas para campos numéricos y entradas vacías.
- Confirmaciones antes de eliminar registros.

## Desarrollo y pruebas

Para comprobar que los archivos se compilan correctamente puedes ejecutar:

```bash
python -m compileall alumnos_app.py crearBase.py
```

## Contribuciones

Se aceptan mejoras mediante *pull requests*. Antes de enviar cambios, procura mantener el estilo de codificación y agregar las pruebas necesarias.

## Licencia

Este proyecto se distribuye sin una licencia explícita. Si planeas reutilizarlo, contacta al autor original para acordar los términos.
