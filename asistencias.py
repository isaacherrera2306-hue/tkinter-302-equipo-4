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
        "INSERT INTO asistencias (id_asistencia, id_alumno, fecha, estado) VALUES (%s, %s, %s, %s)",
        (id_asistencia.get(), id_alumno.get(), fecha.get(), estado.get()),
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("ASISTENCIAS", "Guardado")
    consultar()

def consultar():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id_asistencia, id_alumno, fecha, estado FROM asistencias")
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
        "UPDATE asistencias SET id_alumno=%s, fecha=%s, estado=%s WHERE id_asistencia=%s",
        (id_alumno.get(), fecha.get(), estado.get(), id_asistencia.get()),
    )
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("ASISTENCIAS", "Actualizado")
    consultar()

def eliminar():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM asistencias WHERE id_asistencia=%s", (id_asistencia.get(),))
    con.commit()
    cur.close()
    con.close()
    messagebox.showinfo("ASISTENCIAS", "Eliminado")
    consultar()

ventana = tk.Tk()
ventana.title("ASISTENCIAS")
ventana.config(bg="#1b2631")

tk.Label(ventana, text="Id Asistencia", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6, pady=4)
id_asistencia = tk.Entry(ventana, bg="#ebedef", fg="#1b2631")
id_asistencia.grid(row=0, column=1, padx=6, pady=4)

tk.Label(ventana, text="Id Alumno", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=6, pady=4)
id_alumno = tk.Entry(ventana, bg="#ebedef", fg="#1b2631")
id_alumno.grid(row=1, column=1, padx=6, pady=4)

tk.Label(ventana, text="Fecha", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=6, pady=4)
fecha = tk.Entry(ventana, bg="#ebedef", fg="#1b2631")
fecha.grid(row=2, column=1, padx=6, pady=4)

tk.Label(ventana, text="Estado", bg="#1b2631", fg="#85c1e9", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=6, pady=4)
estado = tk.Entry(ventana, bg="#ebedef", fg="#1b2631")
estado.grid(row=3, column=1, padx=6, pady=4)

lista = tk.Listbox(ventana, width=42, bg="#ebedef", fg="#1b2631")
lista.grid(row=4, column=0, columnspan=2, padx=6, pady=6)

tk.Button(ventana, text="Guardar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=guardar).grid(row=5, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Consultar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=consultar).grid(row=5, column=1, pady=4, sticky="we")
tk.Button(ventana, text="Actualizar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=actualizar).grid(row=6, column=0, pady=4, sticky="we")
tk.Button(ventana, text="Eliminar", bg="#2980b9", fg="white", font=("Arial", 9, "bold"), command=eliminar).grid(row=6, column=1, pady=4, sticky="we")

ventana.mainloop()