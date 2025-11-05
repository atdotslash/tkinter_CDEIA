"""Aplicacion Tkinter para la gestion de alumnos con CRUD completo.

El estilo general replica la estructura vista en las capturas de referencia:
- Treeview para listar alumnos
- Botones que se habilitan/deshabilitan segun el contexto
- Entradas asociadas a variables Tkinter para mantener un estado coherente
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from tkinter import END, DISABLED, NORMAL, StringVar, Tk, ttk, messagebox

DB_PATH = Path(__file__).with_name("alumnos.db")


class AlumnosApp:
    """Gestiona la interfaz grafica y las operaciones CRUD."""

    def __init__(self, raiz: Tk) -> None:
        self.raiz = raiz
        self.raiz.title("Gestor de Alumnos")
        self.raiz.resizable(False, False)

        self.conexion = sqlite3.connect(DB_PATH)
        self.conexion.row_factory = sqlite3.Row
        self._crear_tabla_si_no_existe()

        self.var_nombre = StringVar()
        self.var_domicilio = StringVar()
        self.var_dni = StringVar()
        self.var_edad = StringVar()

        self.id_seleccionado: int | None = None

        self._configurar_estilos()
        self._construir_interfaz()
        self._configurar_eventos()

        self._refrescar_treeview()
        self._estado_inicial()

    # ------------------------------------------------------------------
    # Configuracion de la interfaz
    # ------------------------------------------------------------------
    def _configurar_estilos(self) -> None:
        estilo = ttk.Style(self.raiz)
        estilo.theme_use("clam")
        estilo.configure("Treeview", font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        estilo.map("BotonAccion.TButton", foreground=[("disabled", "#777")])

    def _construir_interfaz(self) -> None:
        marco_formulario = ttk.LabelFrame(self.raiz, text="Datos del alumno", padding=10)
        marco_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(marco_formulario, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.entry_nombre = ttk.Entry(marco_formulario, textvariable=self.var_nombre, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=3)

        ttk.Label(marco_formulario, text="Domicilio:").grid(row=1, column=0, sticky="w")
        self.entry_domicilio = ttk.Entry(marco_formulario, textvariable=self.var_domicilio, width=30)
        self.entry_domicilio.grid(row=1, column=1, padx=5, pady=3)

        ttk.Label(marco_formulario, text="DNI:").grid(row=2, column=0, sticky="w")
        self.entry_dni = ttk.Entry(marco_formulario, textvariable=self.var_dni, width=30)
        self.entry_dni.grid(row=2, column=1, padx=5, pady=3)

        ttk.Label(marco_formulario, text="Edad:").grid(row=3, column=0, sticky="w")
        self.entry_edad = ttk.Entry(marco_formulario, textvariable=self.var_edad, width=30)
        self.entry_edad.grid(row=3, column=1, padx=5, pady=3)

        marco_botones = ttk.Frame(marco_formulario)
        marco_botones.grid(row=4, column=0, columnspan=2, pady=(10, 0))

        self.boton_nuevo = ttk.Button(
            marco_botones,
            text="Nuevo",
            style="BotonAccion.TButton",
            command=self._accion_nuevo,
        )
        self.boton_nuevo.grid(row=0, column=0, padx=4)

        self.boton_guardar = ttk.Button(
            marco_botones,
            text="Guardar",
            style="BotonAccion.TButton",
            command=self._accion_guardar,
        )
        self.boton_guardar.grid(row=0, column=1, padx=4)

        self.boton_editar = ttk.Button(
            marco_botones,
            text="Editar",
            style="BotonAccion.TButton",
            command=self._accion_editar,
        )
        self.boton_editar.grid(row=0, column=2, padx=4)

        self.boton_actualizar = ttk.Button(
            marco_botones,
            text="Actualizar",
            style="BotonAccion.TButton",
            command=self._accion_actualizar,
        )
        self.boton_actualizar.grid(row=0, column=3, padx=4)

        self.boton_eliminar = ttk.Button(
            marco_botones,
            text="Eliminar",
            style="BotonAccion.TButton",
            command=self._accion_eliminar,
        )
        self.boton_eliminar.grid(row=0, column=4, padx=4)

        self.boton_cancelar = ttk.Button(
            marco_botones,
            text="Cancelar",
            style="BotonAccion.TButton",
            command=self._accion_cancelar,
        )
        self.boton_cancelar.grid(row=0, column=5, padx=4)

        self.boton_salir = ttk.Button(
            marco_botones,
            text="Salir",
            style="BotonAccion.TButton",
            command=self._accion_salir,
        )
        self.boton_salir.grid(row=0, column=6, padx=4)

        marco_tree = ttk.LabelFrame(self.raiz, text="Listado de alumnos", padding=10)
        marco_tree.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        columnas = ("nombre", "domicilio", "dni", "edad")
        self.tree = ttk.Treeview(marco_tree, columns=columnas, show="headings", height=8)
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("domicilio", text="Domicilio")
        self.tree.heading("dni", text="DNI")
        self.tree.heading("edad", text="Edad")

        self.tree.column("nombre", width=160)
        self.tree.column("domicilio", width=160)
        self.tree.column("dni", width=100, anchor="center")
        self.tree.column("edad", width=60, anchor="center")

        scrollbar = ttk.Scrollbar(marco_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        marco_tree.rowconfigure(0, weight=1)
        marco_tree.columnconfigure(0, weight=1)

    def _configurar_eventos(self) -> None:
        self.tree.bind("<<TreeviewSelect>>", lambda _: self._on_seleccion())
        self.raiz.protocol("WM_DELETE_WINDOW", self._accion_salir)

    # ------------------------------------------------------------------
    # Estados y validaciones
    # ------------------------------------------------------------------
    def _estado_inicial(self) -> None:
        self._deshabilitar_campos()
        self._limpiar_campos()
        self.tree.selection_remove(self.tree.selection())
        self._configurar_botones(
            nuevo=NORMAL,
            guardar=DISABLED,
            editar=DISABLED,
            actualizar=DISABLED,
            eliminar=DISABLED,
            cancelar=DISABLED,
        )

    def _estado_edicion(self, *, modo_guardar: bool) -> None:
        self._habilitar_campos()
        self._configurar_botones(
            nuevo=DISABLED,
            guardar=NORMAL if modo_guardar else DISABLED,
            editar=DISABLED,
            actualizar=NORMAL if not modo_guardar else DISABLED,
            eliminar=DISABLED,
            cancelar=NORMAL,
        )

    def _estado_seleccion(self) -> None:
        self._deshabilitar_campos()
        self._configurar_botones(
            nuevo=NORMAL,
            guardar=DISABLED,
            editar=NORMAL,
            actualizar=DISABLED,
            eliminar=NORMAL,
            cancelar=NORMAL,
        )

    def _configurar_botones(
        self,
        *,
        nuevo: str,
        guardar: str,
        editar: str,
        actualizar: str,
        eliminar: str,
        cancelar: str,
    ) -> None:
        self.boton_nuevo.state(["!disabled"] if nuevo == NORMAL else ["disabled"])
        self.boton_guardar.state(["!disabled"] if guardar == NORMAL else ["disabled"])
        self.boton_editar.state(["!disabled"] if editar == NORMAL else ["disabled"])
        self.boton_actualizar.state(["!disabled"] if actualizar == NORMAL else ["disabled"])
        self.boton_eliminar.state(["!disabled"] if eliminar == NORMAL else ["disabled"])
        self.boton_cancelar.state(["!disabled"] if cancelar == NORMAL else ["disabled"])

    def _habilitar_campos(self) -> None:
        for entry in (self.entry_nombre, self.entry_domicilio, self.entry_dni, self.entry_edad):
            entry.state(["!disabled"])

    def _deshabilitar_campos(self) -> None:
        for entry in (self.entry_nombre, self.entry_domicilio, self.entry_dni, self.entry_edad):
            entry.state(["disabled"])

    def _limpiar_campos(self) -> None:
        self.var_nombre.set("")
        self.var_domicilio.set("")
        self.var_dni.set("")
        self.var_edad.set("")
        self.id_seleccionado = None

    def _validar_campos(self) -> bool:
        nombre = self.var_nombre.get().strip()
        domicilio = self.var_domicilio.get().strip()
        dni = self.var_dni.get().strip()
        edad = self.var_edad.get().strip()

        if not (nombre and domicilio and dni and edad):
            messagebox.showwarning("Validacion", "Complete todos los campos.")
            return False

        if not dni.isdigit():
            messagebox.showwarning("Validacion", "El DNI debe contener solo numeros.")
            return False

        if not edad.isdigit() or int(edad) <= 0:
            messagebox.showwarning("Validacion", "La edad debe ser un numero positivo.")
            return False

        return True

    # ------------------------------------------------------------------
    # Eventos de interfaz
    # ------------------------------------------------------------------
    def _on_seleccion(self) -> None:
        seleccion = self.tree.selection()
        if not seleccion:
            return
        item_id = seleccion[0]
        valores = self.tree.item(item_id, "values")
        if not valores:
            return

        self.var_nombre.set(valores[0])
        self.var_domicilio.set(valores[1])
        self.var_dni.set(valores[2])
        self.var_edad.set(valores[3])
        self.id_seleccionado = int(item_id)
        self._estado_seleccion()

    def _accion_nuevo(self) -> None:
        self.id_seleccionado = None
        self._limpiar_campos()
        self._estado_edicion(modo_guardar=True)
        self.entry_nombre.focus_set()

    def _accion_guardar(self) -> None:
        if not self._validar_campos():
            return

        try:
            with self.conexion:
                self.conexion.execute(
                    "INSERT INTO alumnos (nombre, domicilio, dni, edad) VALUES (?, ?, ?, ?)",
                    (
                        self.var_nombre.get().strip(),
                        self.var_domicilio.get().strip(),
                        self.var_dni.get().strip(),
                        int(self.var_edad.get().strip()),
                    ),
                )
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El DNI ingresado ya existe en la base de datos.")
            return

        self._refrescar_treeview()
        self._estado_inicial()

    def _accion_editar(self) -> None:
        if self.id_seleccionado is None:
            messagebox.showinfo("Editar", "Seleccione un alumno para modificar.")
            return

        self._estado_edicion(modo_guardar=False)
        self.entry_nombre.focus_set()

    def _accion_actualizar(self) -> None:
        if self.id_seleccionado is None:
            messagebox.showinfo("Actualizar", "Seleccione un alumno para editar.")
            return

        if not self._validar_campos():
            return

        try:
            with self.conexion:
                self.conexion.execute(
                    """
                    UPDATE alumnos
                    SET nombre = ?, domicilio = ?, dni = ?, edad = ?
                    WHERE id = ?
                    """,
                    (
                        self.var_nombre.get().strip(),
                        self.var_domicilio.get().strip(),
                        self.var_dni.get().strip(),
                        int(self.var_edad.get().strip()),
                        self.id_seleccionado,
                    ),
                )
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "No se pudo actualizar el registro. DNI duplicado.")
            return

        self._refrescar_treeview()
        self._estado_inicial()

    def _accion_eliminar(self) -> None:
        if self.id_seleccionado is None:
            messagebox.showinfo("Eliminar", "Seleccione un alumno antes de eliminar.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminacion",
            "¿Desea eliminar al alumno seleccionado?",
        )
        if not confirmar:
            return

        with self.conexion:
            self.conexion.execute("DELETE FROM alumnos WHERE id = ?", (self.id_seleccionado,))

        self._refrescar_treeview()
        self._estado_inicial()

    def _accion_cancelar(self) -> None:
        self._estado_inicial()

    def _accion_salir(self) -> None:
        self.conexion.close()
        self.raiz.destroy()

    # ------------------------------------------------------------------
    # Persistencia
    # ------------------------------------------------------------------
    def _crear_tabla_si_no_existe(self) -> None:
        with self.conexion:
            self.conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS alumnos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    domicilio TEXT NOT NULL,
                    dni TEXT NOT NULL UNIQUE,
                    edad INTEGER NOT NULL
                )
                """
            )

    def _refrescar_treeview(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conexion.execute(
            "SELECT id, nombre, domicilio, dni, edad FROM alumnos ORDER BY nombre"
        )
        for fila in cursor:
            self.tree.insert(
                "",
                END,
                iid=str(fila[0]),
                values=(fila[1], fila[2], fila[3], fila[4]),
            )


def main() -> None:
    raiz = Tk()
    app = AlumnosApp(raiz)
    raiz.mainloop()
    # Cerrar conexion de forma explicita si la ventana se cerro externamente.
    app.conexion.close()


if __name__ == "__main__":
    main()
