# Herrera Luz Oscar Isac: Sube el programa inicial
import tkinter as tk
from tkinter import messagebox, ttk

# -------------------------------------------------------------
# Lopez Nava Cristopher Manuel: Colores y nombre del equipo (Tema Agua)
# -------------------------------------------------------------
root = tk.Tk()
root.title("Descuento")  # Título de ventana requerido[span_2](start_span)[span_2](end_span)
root.geometry("780x680")
root.config(bg="#E8F4F8")  # Fondo principal estilo agua / azul suave

# Título principal
tk.Label(
    root,
    text="Cálculo de Precio con Descuento",
    font=("Arial", 16, "bold"),
    bg="#E8F4F8",
    fg="#01579B",
).pack(pady=12)

# Marco de datos (Entradas)
frame_form = tk.LabelFrame(
    root,
    text=" Datos del Producto ",
    font=("Arial", 10, "bold"),
    bg="#E0F2F1",
    fg="#004D40",
    padx=15,
    pady=15,
)
frame_form.pack(fill="x", padx=20, pady=5)

tk.Label(
    frame_form, text="Precio Original ($):", bg="#E0F2F1", fg="#00695C"
).grid(row=0, column=0, sticky="w", pady=5)
entry_precio = tk.Entry(frame_form, width=32, bg="#FFFFFF")
entry_precio.grid(row=0, column=1, pady=5, padx=5)

tk.Label(
    frame_form, text="Porcentaje de Descuento (%):", bg="#E0F2F1", fg="#00695C"
).grid(row=1, column=0, sticky="w", pady=5)
entry_descuento = tk.Entry(frame_form, width=32, bg="#FFFFFF")
entry_descuento.grid(row=1, column=1, pady=5, padx=5)

# Variable para llevar el control local de los registros en la tabla
contador_id = 1


# -------------------------------------------------------------
# Martinez Caxnajoy Maria Jose: Aviso si faltan datos y validación de descuento
# -------------------------------------------------------------
def calcular_y_guardar():
    global contador_id
    p_str = entry_precio.get().strip()
    d_str = entry_descuento.get().strip()

    # Aviso si faltan datos
    if not p_str or not d_str:
        messagebox.showwarning(
            "Aviso", "Por favor, completa los campos de precio y descuento."
        )
        return

    try:
        precio_val = float(p_str)
        desc_val = float(d_str)

        # Si el descuento es menor que 0 o mayor que 100, se lee un aviso[span_3](start_span)[span_3](end_span)
        if desc_val < 0 or desc_val > 100:
            messagebox.showwarning(
                "Aviso", "El descuento no está entre 0 y 100."
            )  #[span_4](start_span)[span_4](end_span)
            return

        # Muestra cuánto se descuenta y cuánto se paga[span_5](start_span)[span_5](end_span)
        monto_descuento = precio_val * (desc_val / 100)
        total_pagar = precio_val - monto_descuento

        messagebox.showinfo(
            "Resultado del Cálculo",
            f"Monto descontado: ${monto_descuento:.2f}\nTotal a pagar: ${total_pagar:.2f}",
        )  #[span_6](start_span)[span_6](end_span)

        # Agregar el cálculo directamente a la tabla visual local
        tabla.insert(
            "",
            "end",
            values=(
                contador_id,
                f"${precio_val:.2f}",
                f"{desc_val}%",
                f"${monto_descuento:.2f}",
                f"${total_pagar:.2f}",
            ),
        )
        contador_id += 1

        limpiar_campos()

    except ValueError:
        messagebox.showerror(
            "Error", "Por favor, introduce números válidos en los campos."
        )


def eliminar_registro():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning(
            "Advertencia", "Selecciona un registro de la tabla para eliminar."
        )
        return

    if messagebox.askyesno(
        "Confirmar", "¿Estás seguro de eliminar el registro seleccionado?"
    ):
        for item in seleccionado:
            tabla.delete(item)
        messagebox.showinfo("Éxito", "Registro eliminado correctamente.")


# -------------------------------------------------------------
# Ruiz Tellez Victor Uriel: Botón Limpiar
# -------------------------------------------------------------
def limpiar_campos():
    entry_precio.delete(0, tk.END)
    entry_descuento.delete(0, tk.END)


# Panel de Botones (Estilo agua / azul)
frame_botones = tk.Frame(root, bg="#E8F4F8")
frame_botones.pack(pady=10)

btn_calcular = tk.Button(
    frame_botones,
    text="Calcular y Guardar",
    bg="#0288D1",
    fg="white",
    font=("Arial", 9, "bold"),
    width=16,
    command=calcular_y_guardar,
)  # Botón Calcular requerido[span_7](start_span)[span_7](end_span)
btn_calcular.grid(row=0, column=0, padx=5)

btn_eliminar = tk.Button(
    frame_botones,
    text="Eliminar",
    bg="#D35400",
    fg="white",
    font=("Arial", 9, "bold"),
    width=12,
    command=eliminar_registro,
)
btn_eliminar.grid(row=0, column=1, padx=5)

btn_limpiar = tk.Button(
    frame_botones,
    text="Limpiar",
    bg="#607D8B",
    fg="white",
    font=("Arial", 9, "bold"),
    width=12,
    command=limpiar_campos,
)
btn_limpiar.grid(row=0, column=2, padx=5)


# -------------------------------------------------------------
# Tovar Alva Mario Ian: Nombres del equipo y Tabla de visualización
# -------------------------------------------------------------
frame_tabla = tk.LabelFrame(
    root,
    text=" Historial de Cálculos (Memoria Local) ",
    font=("Arial", 10, "bold"),
    bg="#E0F2F1",
    fg="#004D40",
    padx=10,
    pady=10,
)
frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

columnas = (
    "ID",
    "Precio Original",
    "Descuento",
    "Monto Descontado",
    "Total a Pagar",
)
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=6)

anchos = [40, 130, 100, 140, 140]
for col, ancho in zip(columnas, anchos):
    tabla.heading(col, text=col)
    tabla.column(col, anchor="center", width=ancho)

scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scrollbar.set)

tabla.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Pie de página con nombres del equipo
lbl_nombres = tk.Label(
    root,
    text="Equipo: Herrera | Lopez | Martinez | Ruiz | Tovar",
    font=("Arial", 9, "italic"),
    bg="#E8F4F8",
    fg="#0277BD",
)
lbl_nombres.pack(pady=5)

root.mainloop()