import mysql.connector
import tkinter as tk
from tkinter import messagebox

def conectar():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="taller"
    )

def guardar():
    con = conectar(); cur = con.cursor()
    cur.execute("INSERT INTO ORDENES VALUES (%s, %s, %s, %s, %s)", (id_orden.get(), id_servicio.get(), cantidad.get(), monto.get(), alumno.get()))
    con.commit(); cur.close(); con.close()
    messagebox.showinfo("ORDENES", "Guardado exitoso")
    consultar()

def consultar():
    con = conectar(); cur = con.cursor()
    cur.execute("SELECT * FROM ORDENES")
    filas = cur.fetchall()
    cur.close(); con.close()
    lista.delete(0, tk.END)
    for f in filas:
        lista.insert(tk.END, f"Ord:{f[0]} | Serv:{f[1]} | Cant:{f[2]} | {f[3]} | {f[4]}")

def actualizar():
    con = conectar(); cur = con.cursor()
    cur.execute("UPDATE ORDENES SET ID_servicio=%s, Cantidad=%s, Monto=%s, Alumno=%s WHERE ID_orden=%s", (id_servicio.get(), cantidad.get(), monto.get(), alumno.get(), id_orden.get()))
    con.commit(); cur.close(); con.close()
    messagebox.showinfo("ORDENES", "Actualizado exitosamente")
    consultar()

def eliminar():
    con = conectar(); cur = con.cursor()
    cur.execute("DELETE FROM ORDENES WHERE ID_orden=%s", (id_orden.get(),))
    con.commit(); cur.close(); con.close()
    messagebox.showinfo("ORDENES", "Eliminado exitosamente")
    consultar()

ventana = tk.Tk()
ventana.title("Tabla ORDENES (Taller)")
ventana.config(bg="#1b2631")

tk.Label(ventana, text="ID Orden", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6, pady=4)
id_orden = tk.Entry(ventana, bg="#ebedef"); id_orden.grid(row=0, column=1, padx=6, pady=4)

tk.Label(ventana, text="ID Servicio", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=6, pady=4)
id_servicio = tk.Entry(ventana, bg="#ebedef"); id_servicio.grid(row=1, column=1, padx=6, pady=4)

tk.Label(ventana, text="Cantidad", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=6, pady=4)
cantidad = tk.Entry(ventana, bg="#ebedef"); cantidad.grid(row=2, column=1, padx=6, pady=4)

tk.Label(ventana, text="Monto", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=6, pady=4)
monto = tk.Entry(ventana, bg="#ebedef"); monto.grid(row=3, column=1, padx=6, pady=4)

tk.Label(ventana, text="Alumno", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=4, column=0, padx=6, pady=4)
alumno = tk.Entry(ventana, bg="#ebedef"); alumno.grid(row=4, column=1, padx=6, pady=4)

lista = tk.Listbox(ventana, width=48, bg="#ebedef"); lista.grid(row=5, column=0, columnspan=2, padx=6, pady=6)

tk.Button(ventana, text="Guardar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=guardar).grid(row=6, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Consultar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=consultar).grid(row=6, column=1, pady=4, sticky="we")
tk.Button(ventana, text="Actualizar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=actualizar).grid(row=7, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Eliminar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=eliminar).grid(row=7, column=1, pady=4, sticky="we")

consultar()
ventana.mainloop()