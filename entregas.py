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
        "INSERT INTO ENTREGAS VALUES (%s, %s, %s, %s)", 
        (id_entrega.get(), id_pedido.get(), fecha.get(), estado.get())
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("ENTREGAS", "Guardado exitoso")
    consultar()

def consultar():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM ENTREGAS")
    filas = cur.fetchall()
    cur.close()
    con.close()
    lista.delete(0, tk.END)
    for f in filas:
        lista.insert(tk.END, f"Ent:{f[0]} | Ped:{f[1]} | {f[2]} | {f[3]}")

def actualizar():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE ENTREGAS SET ID_pedido=%s, Fecha=%s, Estado=%s WHERE ID_entrega=%s", 
        (id_pedido.get(), fecha.get(), estado.get(), id_entrega.get())
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("ENTREGAS", "Actualizado exitosamente")
    consultar()

def eliminar():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM ENTREGAS WHERE ID_entrega=%s", (id_entrega.get(),))
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("ENTREGAS", "Eliminado exitosamente")
    consultar()

ventana = tk.Tk()
ventana.title("Tabla ENTREGAS")
ventana.config(bg="#1b2631")

tk.Label(ventana, text="ID Entrega", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6, pady=4)
id_entrega = tk.Entry(ventana, bg="#ebedef")
id_entrega.grid(row=0, column=1, padx=6, pady=4)

tk.Label(ventana, text="ID Pedido", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=6, pady=4)
id_pedido = tk.Entry(ventana, bg="#ebedef")
id_pedido.grid(row=1, column=1, padx=6, pady=4)

tk.Label(ventana, text="Fecha", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=6, pady=4)
fecha = tk.Entry(ventana, bg="#ebedef")
fecha.grid(row=2, column=1, padx=6, pady=4)

tk.Label(ventana, text="Estado", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=6, pady=4)
estado = tk.Entry(ventana, bg="#ebedef")
estado.grid(row=3, column=1, padx=6, pady=4)

lista = tk.Listbox(ventana, width=45, bg="#ebedef")
lista.grid(row=4, column=0, columnspan=2, padx=6, pady=6)

tk.Button(ventana, text="Guardar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=guardar).grid(row=5, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Consultar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=consultar).grid(row=5, column=1, pady=4, sticky="we")
tk.Button(ventana, text="Actualizar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=actualizar).grid(row=6, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Eliminar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=eliminar).grid(row=6, column=1, pady=4, sticky="we")

consultar()
ventana.mainloop()