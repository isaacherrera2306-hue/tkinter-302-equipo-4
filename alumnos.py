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
        "INSERT INTO alumnos (id_alumno, nombre, apellido, id_grupo) VALUES (%s, %s, %s, %s)",
        (id_alumno.get(), nombre.get(), apellido.get(), id_grupo.get()),
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("ALUMNOS", "Guardado")
    consultar()

def consultar():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id_alumno, nombre, apellido, id_grupo FROM alumnos")
    filas = cur.fetchall()
    cur.close()
    con.close()
    lista.delete(0, tk.END)
    for fila in filas:
        lista.insert(tk.END, f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]}")

def actualizar():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE alumnos SET nombre=%s, apellido=%s, id_grupo=%s WHERE id_alumno=%s",
        (nombre.get(), apellido.get(), id_grupo.get(), id_alumno.get()),
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("ALUMNOS", "Actualizado")
    consultar()

def eliminar():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM alumnos WHERE id_alumno=%s", (id_alumno.get(),))
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("ALUMNOS", "Eliminado")
    consultar()

ventana = tk.Tk()
ventana.title("ALUMNOS")
ventana.config(bg="#145a32")

tk.Label(ventana, text="Id Alumno", bg="#145a32", fg="#a9dfbf", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6, pady=4)
id_alumno = tk.Entry(ventana, bg="#eafaf1", fg="#145a32")
id_alumno.grid(row=0, column=1, padx=6, pady=4)

tk.Label(ventana, text="Nombre", bg="#145a32", fg="#a9dfbf", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=6, pady=4)
nombre = tk.Entry(ventana, bg="#eafaf1", fg="#145a32")
nombre.grid(row=1, column=1, padx=6, pady=4)

tk.Label(ventana, text="Apellido", bg="#145a32", fg="#a9dfbf", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=6, pady=4)
apellido = tk.Entry(ventana, bg="#eafaf1", fg="#145a32")
apellido.grid(row=2, column=1, padx=6, pady=4)

tk.Label(ventana, text="Id Grupo", bg="#145a32", fg="#a9dfbf", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=6, pady=4)
id_grupo = tk.Entry(ventana, bg="#eafaf1", fg="#145a32")
id_grupo.grid(row=3, column=1, padx=6, pady=4)

lista = tk.Listbox(ventana, width=42, bg="#eafaf1", fg="#145a32")
lista.grid(row=4, column=0, columnspan=2, padx=6, pady=6)

tk.Button(ventana, text="Guardar", bg="#117a65", fg="white", font=("Arial", 9, "bold"), command=guardar).grid(row=5, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Consultar", bg="#117a65", fg="white", font=("Arial", 9, "bold"), command=consultar).grid(row=5, column=1, pady=4, sticky="we")
tk.Button(ventana, text="Actualizar", bg="#117a65", fg="white", font=("Arial", 9, "bold"), command=actualizar).grid(row=6, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Eliminar", bg="#117a65", fg="white", font=("Arial", 9, "bold"), command=eliminar).grid(row=6, column=1, pady=4, sticky="we")

ventana.mainloop()