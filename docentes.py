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
        "INSERT INTO docentes (id_docente, nombre, id_grupo) VALUES (%s, %s, %s)",
        (id_docente.get(), nombre.get(), id_grupo.get()),
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("DOCENTES", "Guardado")
    consultar()

def consultar():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id_docente, nombre, id_grupo FROM docentes")
    filas = cur.fetchall()
    cur.close()
    con.close()
    lista.delete(0, tk.END)
    for fila in filas:
        lista.insert(tk.END, f"{fila[0]} | {fila[1]} | {fila[2]}")

def actualizar():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE docentes SET nombre=%s, id_grupo=%s WHERE id_docente=%s",
        (nombre.get(), id_grupo.get(), id_docente.get()),
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("DOCENTES", "Actualizado")
    consultar()

def eliminar():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM docentes WHERE id_docente=%s", (id_docente.get(),))
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("DOCENTES", "Eliminado")
    consultar()

ventana = tk.Tk()
ventana.title("DOCENTES")
ventana.config(bg="#4a235a")

tk.Label(ventana, text="Id Docente", bg="#4a235a", fg="#d7bde2", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6, pady=4)
id_docente = tk.Entry(ventana, bg="#f5eef8", fg="#4a235a")
id_docente.grid(row=0, column=1, padx=6, pady=4)

tk.Label(ventana, text="Nombre", bg="#4a235a", fg="#d7bde2", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=6, pady=4)
nombre = tk.Entry(ventana, bg="#f5eef8", fg="#4a235a")
nombre.grid(row=1, column=1, padx=6, pady=4)

tk.Label(ventana, text="Id Grupo", bg="#4a235a", fg="#d7bde2", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=6, pady=4)
id_grupo = tk.Entry(ventana, bg="#f5eef8", fg="#4a235a")
id_grupo.grid(row=2, column=1, padx=6, pady=4)

lista = tk.Listbox(ventana, width=42, bg="#f5eef8", fg="#4a235a")
lista.grid(row=3, column=0, columnspan=2, padx=6, pady=6)

tk.Button(ventana, text="Guardar", bg="#8e44ad", fg="white", font=("Arial", 9, "bold"), command=guardar).grid(row=4, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Consultar", bg="#8e44ad", fg="white", font=("Arial", 9, "bold"), command=consultar).grid(row=4, column=1, pady=4, sticky="we")
tk.Button(ventana, text="Actualizar", bg="#8e44ad", fg="white", font=("Arial", 9, "bold"), command=actualizar).grid(row=5, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Eliminar", bg="#8e44ad", fg="white", font=("Arial", 9, "bold"), command=eliminar).grid(row=5, column=1, pady=4, sticky="we")

ventana.mainloop()