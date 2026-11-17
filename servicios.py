import mysql.connector
import tkinter as tk
from tkinter import messagebox

def conectar():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="taller"
    )

def guardar():
    con = conectar(); cur = con.cursor()
    cur.execute("INSERT INTO SERVICIOS VALUES (%s, %s, %s)", (id_servicio.get(), nombre.get(), precio.get()))
    con.commit(); cur.close(); con.close()
    messagebox.showinfo("SERVICIOS", "Guardado exitoso")
    consultar()

def consultar():
    con = conectar(); cur = con.cursor()
    cur.execute("SELECT * FROM SERVICIOS")
    filas = cur.fetchall()
    cur.close(); con.close()
    lista.delete(0, tk.END)
    for f in filas:
        lista.insert(tk.END, f"ID:{f[0]} | Nom:{f[1]} | Precio:{f[2]}")

def actualizar():
    con = conectar(); cur = con.cursor()
    cur.execute("UPDATE SERVICIOS SET Nombre=%s, Precio=%s WHERE ID_servicio=%s", (nombre.get(), precio.get(), id_servicio.get()))
    con.commit(); cur.close(); con.close()
    messagebox.showinfo("SERVICIOS", "Actualizado exitosamente")
    consultar()

def eliminar():
    con = conectar(); cur = con.cursor()
    cur.execute("DELETE FROM SERVICIOS WHERE ID_servicio=%s", (id_servicio.get(),))
    con.commit(); cur.close(); con.close()
    messagebox.showinfo("SERVICIOS", "Eliminado exitosamente")
    consultar()

ventana = tk.Tk()
ventana.title("Tabla SERVICIOS")
ventana.config(bg="#1b2631")

tk.Label(ventana, text="ID Servicio", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6, pady=4)
id_servicio = tk.Entry(ventana, bg="#ebedef"); id_servicio.grid(row=0, column=1, padx=6, pady=4)

tk.Label(ventana, text="Nombre", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=6, pady=4)
nombre = tk.Entry(ventana, bg="#ebedef"); nombre.grid(row=1, column=1, padx=6, pady=4)

tk.Label(ventana, text="Precio", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=6, pady=4)
precio = tk.Entry(ventana, bg="#ebedef"); precio.grid(row=2, column=1, padx=6, pady=4)

lista = tk.Listbox(ventana, width=45, bg="#ebedef"); lista.grid(row=3, column=0, columnspan=2, padx=6, pady=6)

tk.Button(ventana, text="Guardar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=guardar).grid(row=4, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Consultar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=consultar).grid(row=4, column=1, pady=4, sticky="we")
tk.Button(ventana, text="Actualizar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=actualizar).grid(row=5, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Eliminar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=eliminar).grid(row=5, column=1, pady=4, sticky="we")

consultar()
ventana.mainloop()