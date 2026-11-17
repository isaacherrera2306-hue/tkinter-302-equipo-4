import mysql.connector
import tkinter as tk
from tkinter import messagebox

def conectar():
    return mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="", 
        database="uniforme1"
    )

def guardar():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO PRENDAS VALUES (%s, %s, %s, %s)", 
        (id_prenda.get(), nombre.get(), talla.get(), precio.get())
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("PRENDAS", "Guardado exitoso")
    consultar()

def consultar():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM PRENDAS")
    filas = cur.fetchall()
    cur.close()
    con.close()
    lista.delete(0, tk.END)
    for f in filas:
        lista.insert(tk.END, f"{f[0]} | {f[1]} | Talla: {f[2]} | {f[3]}")

def actualizar():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE PRENDAS SET Nombre=%s, Talla=%s, Precio=%s WHERE ID_prenda=%s", 
        (nombre.get(), talla.get(), precio.get(), id_prenda.get())
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("PRENDAS", "Actualizado exitosamente")
    consultar()

def eliminar():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM PRENDAS WHERE ID_prenda=%s", (id_prenda.get(),))
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("PRENDAS", "Eliminado exitosamente")
    consultar()

ventana = tk.Tk()
ventana.title("Tabla PRENDAS")
ventana.config(bg="#1b2631")

tk.Label(ventana, text="ID Prenda", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6, pady=4)
id_prenda = tk.Entry(ventana, bg="#ebedef")
id_prenda.grid(row=0, column=1, padx=6, pady=4)

tk.Label(ventana, text="Nombre", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=6, pady=4)
nombre = tk.Entry(ventana, bg="#ebedef")
nombre.grid(row=1, column=1, padx=6, pady=4)

tk.Label(ventana, text="Talla", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=6, pady=4)
talla = tk.Entry(ventana, bg="#ebedef")
talla.grid(row=2, column=1, padx=6, pady=4)

tk.Label(ventana, text="Precio", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=6, pady=4)
precio = tk.Entry(ventana, bg="#ebedef")
precio.grid(row=3, column=1, padx=6, pady=4)

lista = tk.Listbox(ventana, width=45, bg="#ebedef")
lista.grid(row=4, column=0, columnspan=2, padx=6, pady=6)

tk.Button(ventana, text="Guardar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=guardar).grid(row=5, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Consultar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=consultar).grid(row=5, column=1, pady=4, sticky="we")
tk.Button(ventana, text="Actualizar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=actualizar).grid(row=6, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Eliminar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=eliminar).grid(row=6, column=1, pady=4, sticky="we")

consultar()
ventana.mainloop()