import mysql.connector
import tkinter as tk
from tkinter import messagebox

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="uniforme1",
    )

def guardar():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO pedidos (id_pedido, id_prenda, cantidad, monto, alumno) VALUES (%s, %s, %s, %s, %s)",
        (id_pedido.get(), id_prenda.get(), cantidad.get(), monto.get(), alumno.get()),
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("pedidos", "Guardado")
    consultar()

def consultar():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id_pedido, id_prenda, cantidad, monto, alumno FROM pedidos")
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
        "UPDATE pedidos SET id_prenda=%s, cantidad=%s, monto=%s, alumno=%s WHERE id_pedido=%s",
        ( id_prenda.get(), cantidad.get(), monto.get(), alumno.get(), id_pedido.get()),
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("PEDIDOS", "Actualizado")
    consultar()

def eliminar():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM pedidos WHERE id_pedido=%s", (id_pedido.get(),))
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("PEDIDO", "Eliminado")
    consultar()

ventana = tk.Tk()
ventana.title("PEDIDOS")
ventana.config(bg="#212f3d")

tk.Label(ventana, text="Id pedido", bg="#212f3d", fg="#85929e", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6, pady=4)
id_pedido = tk.Entry(ventana, bg="#eaeded", fg="#212f3d")
id_pedido.grid(row=0, column=1, padx=6, pady=4)

tk.Label(ventana, text="Id prenda", bg="#212f3d", fg="#85929e", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=6, pady=4)
id_prenda = tk.Entry(ventana, bg="#eaeded", fg="#212f3d")
id_prenda.grid(row=1, column=1, padx=6, pady=4)

tk.Label(ventana, text="Cantidad", bg="#212f3d", fg="#85929e", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=6, pady=4)
cantidad = tk.Entry(ventana, bg="#eaeded", fg="#212f3d")
cantidad.grid(row=2, column=1, padx=6, pady=4)

tk.Label(ventana, text="Monto", bg="#212f3d", fg="#85929e", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=6, pady=4)
monto = tk.Entry(ventana, bg="#eaeded", fg="#212f3d")
monto.grid(row=3, column=1, padx=6, pady=4)

tk.Label(ventana, text="Alumno", bg="#212f3d", fg="#85929e", font=("Arial", 10, "bold")).grid(row=4, column=0, padx=6, pady=4)
alumno = tk.Entry(ventana, bg="#eaeded", fg="#212f3d")
alumno.grid(row=4, column=1, padx=6, pady=4)

lista = tk.Listbox(ventana, width=50, bg="#eaeded", fg="#212f3d")
lista.grid(row=5, column=0, columnspan=2, padx=6, pady=6)

tk.Button(ventana, text="Guardar", bg="#212f3d", fg="white", font=("Arial", 9, "bold"), command=guardar).grid(row=6, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Consultar", bg="#212f3d", fg="white", font=("Arial", 9, "bold"), command=consultar).grid(row=6, column=1, pady=4, sticky="we")
tk.Button(ventana, text="Actualizar", bg="#212f3d", fg="white", font=("Arial", 9, "bold"), command=actualizar).grid(row=7, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Eliminar", bg="#212f3d", fg="white", font=("Arial", 9, "bold"), command=eliminar).grid(row=7, column=1, pady=4, sticky="we")

ventana.mainloop()