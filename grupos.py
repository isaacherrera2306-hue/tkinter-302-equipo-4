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
        "INSERT INTO grupos (id_grupo, nombre, turno) VALUES (%s, %s, %s)",
        (id_grupo.get(), nombre.get(), turno.get()),
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("GRUPOS", "Guardado")
    consultar()

def consultar():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id_grupo, nombre, turno FROM grupos")
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
        "UPDATE grupos SET nombre=%s, turno=%s WHERE id_grupo=%s",
        (nombre.get(), turno.get(), id_grupo.get()),
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("GRUPOS", "Actualizado")
    consultar()

def eliminar():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM grupos WHERE id_grupo=%s", (id_grupo.get(),))
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("GRUPOS", "Eliminado")
    consultar()

ventana = tk.Tk()
ventana.title("GRUPOS")
ventana.config(bg="#1a5276")

tk.Label(ventana, text="Id Grupo", bg="#1a5276", fg="#a9cce3", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6, pady=4)
id_grupo = tk.Entry(ventana, bg="#d4efdf", fg="#1a5276")
id_grupo.grid(row=0, column=1, padx=6, pady=4)

tk.Label(ventana, text="Nombre", bg="#1a5276", fg="#a9cce3", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=6, pady=4)
nombre = tk.Entry(ventana, bg="#d4efdf", fg="#1a5276")
nombre.grid(row=1, column=1, padx=6, pady=4)

tk.Label(ventana, text="Turno", bg="#1a5276", fg="#a9cce3", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=6, pady=4)
turno = tk.Entry(ventana, bg="#d4efdf", fg="#1a5276")
turno.grid(row=2, column=1, padx=6, pady=4)

lista = tk.Listbox(ventana, width=42, bg="#d4efdf", fg="#1a5276")
lista.grid(row=3, column=0, columnspan=2, padx=6, pady=6)

tk.Button(ventana, text="Guardar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=guardar).grid(row=4, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Consultar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=consultar).grid(row=4, column=1, pady=4, sticky="we")
tk.Button(ventana, text="Actualizar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=actualizar).grid(row=5, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Eliminar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=eliminar).grid(row=5, column=1, pady=4, sticky="we")

ventana.mainloop()