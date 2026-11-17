import mysql.connector
import tkinter as tk
from tkinter import messagebox

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="A302",
    )

def guardar():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO incidencias (id_incidencia, id_alumno, id_docente, fecha, descripcion) VALUES (%s, %s, %s, %s, %s)",
        (id_incidencia.get(), id_alumno.get(), id_docente.get(), fecha.get(), descripcion.get()),
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("INCIDENCIAS", "Guardado")
    consultar()

def consultar():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id_incidencia, id_alumno, id_docente, fecha, descripcion FROM incidencias")
    filas = cur.fetchall()
    cur.close()
    con.close()
    lista.delete(0, tk.END)
    for fila in filas:
        lista.insert(tk.END, f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]} | {fila[4]}")

def actualizar():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE incidencias SET id_alumno=%s, id_docente=%s, fecha=%s, descripcion=%s WHERE id_incidencia=%s",
        (id_alumno.get(), id_docente.get(), fecha.get(), descripcion.get(), id_incidencia.get()),
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("INCIDENCIAS", "Actualizado")
    consultar()

def eliminar():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM incidencias WHERE id_incidencia=%s", (id_incidencia.get(),))
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("INCIDENCIAS", "Eliminado")
    consultar()

ventana = tk.Tk()
ventana.title("INCIDENCIAS")
ventana.config(bg="#212f3d")

tk.Label(ventana, text="Id Incidencia", bg="#212f3d", fg="#85929e", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6, pady=4)
id_incidencia = tk.Entry(ventana, bg="#eaeded", fg="#212f3d")
id_incidencia.grid(row=0, column=1, padx=6, pady=4)

tk.Label(ventana, text="Id Alumno", bg="#212f3d", fg="#85929e", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=6, pady=4)
id_alumno = tk.Entry(ventana, bg="#eaeded", fg="#212f3d")
id_alumno.grid(row=1, column=1, padx=6, pady=4)

tk.Label(ventana, text="Id Docente", bg="#212f3d", fg="#85929e", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=6, pady=4)
id_docente = tk.Entry(ventana, bg="#eaeded", fg="#212f3d")
id_docente.grid(row=2, column=1, padx=6, pady=4)

tk.Label(ventana, text="Fecha", bg="#212f3d", fg="#85929e", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=6, pady=4)
fecha = tk.Entry(ventana, bg="#eaeded", fg="#212f3d")
fecha.grid(row=3, column=1, padx=6, pady=4)

tk.Label(ventana, text="Descripción", bg="#212f3d", fg="#85929e", font=("Arial", 10, "bold")).grid(row=4, column=0, padx=6, pady=4)
descripcion = tk.Entry(ventana, bg="#eaeded", fg="#212f3d")
descripcion.grid(row=4, column=1, padx=6, pady=4)

lista = tk.Listbox(ventana, width=50, bg="#eaeded", fg="#212f3d")
lista.grid(row=5, column=0, columnspan=2, padx=6, pady=6)

tk.Button(ventana, text="Guardar", bg="#212f3d", fg="white", font=("Arial", 9, "bold"), command=guardar).grid(row=6, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Consultar", bg="#212f3d", fg="white", font=("Arial", 9, "bold"), command=consultar).grid(row=6, column=1, pady=4, sticky="we")
tk.Button(ventana, text="Actualizar", bg="#212f3d", fg="white", font=("Arial", 9, "bold"), command=actualizar).grid(row=7, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Eliminar", bg="#212f3d", fg="white", font=("Arial", 9, "bold"), command=eliminar).grid(row=7, column=1, pady=4, sticky="we")

ventana.mainloop()