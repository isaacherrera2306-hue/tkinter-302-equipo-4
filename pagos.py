import mysql.connector
import tkinter as tk
from tkinter import messagebox

def conectar():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="taller"
    )

def guardar():
    con = conectar(); cur = con.cursor()
    cur.execute("INSERT INTO PAGOS VALUES (%s, %s, %s, %s)", (id_pago.get(), id_orden.get(), monto.get(), forma.get()))
    con.commit(); cur.close(); con.close()
    messagebox.showinfo("PAGOS", "Guardado exitoso")
    consultar()

def consultar():
    con = conectar(); cur = con.cursor()
    cur.execute("SELECT * FROM PAGOS")
    filas = cur.fetchall()
    cur.close(); con.close()
    lista.delete(0, tk.END)
    for f in filas:
        lista.insert(tk.END, f"Pago:{f[0]} | Orden:{f[1]} | {f[2]} | {f[3]}")

def actualizar():
    con = conectar(); cur = con.cursor()
    cur.execute("UPDATE PAGOS SET ID_orden=%s, Monto=%s, Forma=%s WHERE ID_pago=%s", (id_orden.get(), monto.get(), forma.get(), id_pago.get()))
    con.commit(); cur.close(); con.close()
    messagebox.showinfo("PAGOS", "Actualizado exitosamente")
    consultar()

def eliminar():
    con = conectar(); cur = con.cursor()
    cur.execute("DELETE FROM PAGOS WHERE ID_pago=%s", (id_pago.get(),))
    con.commit(); cur.close(); con.close()
    messagebox.showinfo("PAGOS", "Eliminado exitosamente")
    consultar()

ventana = tk.Tk()
ventana.title("Tabla PAGOS")
ventana.config(bg="#1b2631")

tk.Label(ventana, text="ID Pago", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6, pady=4)
id_pago = tk.Entry(ventana, bg="#ebedef"); id_pago.grid(row=0, column=1, padx=6, pady=4)

tk.Label(ventana, text="ID Orden", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=6, pady=4)
id_orden = tk.Entry(ventana, bg="#ebedef"); id_orden.grid(row=1, column=1, padx=6, pady=4)

tk.Label(ventana, text="Monto", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=6, pady=4)
monto = tk.Entry(ventana, bg="#ebedef"); monto.grid(row=2, column=1, padx=6, pady=4)

tk.Label(ventana, text="Forma", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=6, pady=4)
forma = tk.Entry(ventana, bg="#ebedef"); forma.grid(row=3, column=1, padx=6, pady=4)

lista = tk.Listbox(ventana, width=45, bg="#ebedef"); lista.grid(row=4, column=0, columnspan=2, padx=6, pady=6)

tk.Button(ventana, text="Guardar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=guardar).grid(row=5, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Consultar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=consultar).grid(row=5, column=1, pady=4, sticky="we")
tk.Button(ventana, text="Actualizar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=actualizar).grid(row=6, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Eliminar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=eliminar).grid(row=6, column=1, pady=4, sticky="we")

consultar()
ventana.mainloop()