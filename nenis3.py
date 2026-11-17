from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import sqlite3
import os
import sys
import csv
from datetime import date, datetime
import calendar

# ==========================================================
# PRIMARIA NEZAHUALCÓYOTL | PANEL DE DIRECCIÓN Y DOCENTE
# Versión optimizada con rutas seguras para compilación
# ==========================================================

TEMAS = {
    "claro": {
        "BG": "#EBF2F0",           
        "WHITE": "#FFFFFF",
        "NAVY": "#0A2540",         
        "DARK": "#112D32",         
        "PURPLE": "#2563EB",       
        "GOLD": "#059669",         
        "GOLD_LIGHT": "#D1FAE5",   
        "GOLD_DARK": "#047857",    
        "LAVENDER": "#E0F2FE",     
        "MUTED": "#475569",        
        "BORDER": "#CBD5E1",
        "BLUE_SOFT": "#DBEAFE",
        "GREEN_SOFT": "#DCFCE7",
        "YELLOW_SOFT": "#E0F2FE",  
        "RED_SOFT": "#FEE2E2",
        "RED": "#DC2626",
        "RED_DARK": "#991B1B",
        "TEAL": "#0284C7",         
        "TEXT_NAV": "#FFFFFF",     
        "TEXT_MAIN": "#0A2540",
    },
    "oscuro": {
        "BG": "#06121E",           
        "WHITE": "#0D1B2A",        
        "NAVY": "#1B263B",
        "DARK": "#415A77",
        "PURPLE": "#38BDF8",       
        "GOLD": "#10B981",         
        "GOLD_LIGHT": "#1E293B",
        "GOLD_DARK": "#059669",
        "LAVENDER": "#0F172A",
        "MUTED": "#94A3B8",        
        "BORDER": "#1E293B",
        "BLUE_SOFT": "#1E3A8A",
        "GREEN_SOFT": "#064E3B",
        "YELLOW_SOFT": "#1E293B",  
        "RED_SOFT": "#7F1D1D",
        "RED": "#F87171",
        "RED_DARK": "#EF4444",
        "TEAL": "#38BDF8",         
        "TEXT_NAV": "#F8FAFC",     
        "TEXT_MAIN": "#F8FAFC",
    }
}

UMBRAL_FALTAS = 3

# --- RUTA SEGURA PARA COMPILACIÓN (PyInstaller / Pydroid) ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        BASE_DIR = os.getcwd()

DB_PATH = os.path.join(BASE_DIR, "direccion_nezahualcoyotl.db")


class PanelDireccion:
    def __init__(self, root, modo_oscuro=False):
        self.root = root
        self.modo_oscuro = modo_oscuro
        self.actualizar_colores()
        
        self.root.title("Primaria Nezahualcóyotl | Dirección y Docentes")
        self.root.geometry("1280x820")
        self.root.minsize(320, 480)
        self.root.configure(bg=self.BG)
        self.pagina = "Inicio"
        self.compacto = False
        self._resize_job = None
        self.iniciar_db()
        self.configurar_estilos()
        self.root.bind("<Configure>", self.detectar_tamano)
        self.pantalla_login()

    def actualizar_colores(self):
        t = TEMAS["oscuro"] if self.modo_oscuro else TEMAS["claro"]
        self.BG = t["BG"]
        self.WHITE = t["WHITE"]
        self.NAVY = t["NAVY"]
        self.DARK = t["DARK"]
        self.PURPLE = t["PURPLE"]
        self.GOLD = t["GOLD"]
        self.GOLD_LIGHT = t["GOLD_LIGHT"]
        self.GOLD_DARK = t["GOLD_DARK"]
        self.LAVENDER = t["LAVENDER"]
        self.MUTED = t["MUTED"]
        self.BORDER = t["BORDER"]
        self.BLUE_SOFT = t["BLUE_SOFT"]
        self.GREEN_SOFT = t["GREEN_SOFT"]
        self.YELLOW_SOFT = t["YELLOW_SOFT"]
        self.RED_SOFT = t["RED_SOFT"]
        self.RED = t["RED"]
        self.RED_DARK = t["RED_DARK"]
        self.TEAL = t["TEAL"]
        self.TEXT_NAV = t["TEXT_NAV"]
        self.TEXT_MAIN = t["TEXT_MAIN"]

    def cambiar_tema(self):
        self.modo_oscuro = not self.modo_oscuro
        self.actualizar_colores()
        self.configurar_estilos()
        self.crear_panel(self.pagina)

    def conectar(self):
        db = sqlite3.connect(DB_PATH)
        db.execute("PRAGMA foreign_keys = ON")
        return db

    def iniciar_db(self):
        with self.conectar() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS metricas(
                    nombre TEXT PRIMARY KEY, valor INTEGER NOT NULL);
                CREATE TABLE IF NOT EXISTS grupos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    grupo TEXT NOT NULL UNIQUE, docente TEXT NOT NULL,
                    alumnos INTEGER NOT NULL DEFAULT 0);
                CREATE TABLE IF NOT EXISTS alumnos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL, grupo TEXT NOT NULL,
                    retardos INTEGER NOT NULL DEFAULT 0,
                    faltas INTEGER NOT NULL DEFAULT 0,
                    UNIQUE(nombre, grupo));
                CREATE TABLE IF NOT EXISTS asistencias(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alumno_id INTEGER NOT NULL, fecha TEXT NOT NULL,
                    estado TEXT NOT NULL, UNIQUE(alumno_id, fecha),
                    FOREIGN KEY(alumno_id) REFERENCES alumnos(id));
                CREATE TABLE IF NOT EXISTS justificantes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alumno TEXT NOT NULL, grupo TEXT NOT NULL,
                    fecha TEXT NOT NULL, motivo TEXT NOT NULL,
                    estado TEXT NOT NULL DEFAULT 'Pendiente');
                CREATE TABLE IF NOT EXISTS seguimientos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alumno_id INTEGER NOT NULL, fecha TEXT NOT NULL,
                    nota TEXT NOT NULL,
                    FOREIGN KEY(alumno_id) REFERENCES alumnos(id));
                CREATE TABLE IF NOT EXISTS incidencias(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alumno_id INTEGER NOT NULL, fecha TEXT NOT NULL,
                    tipo TEXT NOT NULL, descripcion TEXT NOT NULL,
                    estado TEXT NOT NULL DEFAULT 'Pendiente',
                    FOREIGN KEY(alumno_id) REFERENCES alumnos(id));
                CREATE TABLE IF NOT EXISTS eventos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL, titulo TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS comunicados(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL, titulo TEXT NOT NULL, mensaje TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS bitacora(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL, entrada TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS mensajes_docente(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    docente TEXT NOT NULL, fecha TEXT NOT NULL,
                    asunto TEXT NOT NULL, mensaje TEXT NOT NULL);
            """)
            db.executemany(
                "INSERT OR IGNORE INTO metricas(nombre,valor) VALUES (?,?)",
                [("Alumnos", 420), ("Presentes", 0), ("Retardos", 0),
                 ("Faltas", 0), ("Incidencias", 0)])
            grupos = [
                ("1° A", "Sofía Hernández Vega", 31),
                ("2° A", "María López Gómez", 35),
                ("2° B", "Luis Ramírez Díaz", 33),
                ("3° B", "Juan Pérez Cruz", 34),
                ("4° A", "Ana Martínez Solís", 32)]
            for fila in grupos:
                db.execute("INSERT OR IGNORE INTO grupos(grupo,docente,alumnos) VALUES (?,?,?)", fila)
            if db.execute("SELECT COUNT(*) FROM alumnos").fetchone()[0] == 0:
                db.executemany(
                    "INSERT INTO alumnos(nombre,grupo,retardos,faltas) VALUES (?,?,?,?)",
                    [
                        ("Santiago Pérez Gómez", "2° A", 0, 0),
                        ("Valentina Cruz Ruiz", "2° A", 1, 0),
                        ("Mateo Morales López", "2° A", 2, 0),
                        ("Sofía Castillo Vega", "2° A", 3, 1),
                        ("Alejandro Torres Silva", "2° A", 0, 3),
                        ("Camila Ortiz Mendoza", "2° A", 1, 0),
                        ("Diego Ramos Castro", "2° A", 0, 0),
                        ("Regina Flores Jiménez", "2° B", 0, 0),
                        ("Daniel Vargas Soto", "2° B", 2, 1),
                        ("Lucía Mendoza Ríos", "3° B", 1, 3),
                        ("Emiliano Herrera Luna", "4° A", 0, 0),
                        ("Ximena Rivas Domínguez", "4° A", 0, 0)
                    ])

    def configurar_estilos(self):
        s = ttk.Style()
        try: s.theme_use("clam")
        except tk.TclError: pass
        
        fg_tabla = "#F8FAFC" if self.modo_oscuro else "#0A2540"
        bg_tabla = "#0D1B2A" if self.modo_oscuro else "#FFFFFF"
        header_bg = "#1B263B" if self.modo_oscuro else "#0A2540"
        header_fg = "#38BDF8" if self.modo_oscuro else "#FFFFFF"

        s.configure("Treeview", background=bg_tabla, foreground=fg_tabla,
                    fieldbackground=bg_tabla, rowheight=32, borderwidth=0, font=("Arial", 9))
        s.configure("Treeview.Heading", background=header_bg, foreground=header_fg,
                    font=("Arial", 9, "bold"), padding=(6, 8), relief="flat")
        s.map("Treeview", background=[("selected", self.GOLD)],
              foreground=[("selected", "#FFFFFF" if self.modo_oscuro else "#0A2540")])
        s.configure("TCombobox", padding=5, font=("Arial", 9),
                    fieldbackground=bg_tabla, background=bg_tabla, foreground=fg_tabla)
        s.map("TCombobox", fieldbackground=[("readonly", bg_tabla)],
              foreground=[("readonly", fg_tabla)])
        s.configure("Vertical.TScrollbar", background=self.GOLD, troughcolor=self.BG)
        self.root.option_add("*Entry.background", bg_tabla)
        self.root.option_add("*Entry.foreground", fg_tabla)
        self.root.option_add("*Entry.insertBackground", fg_tabla)
        self.root.option_add("*Entry.highlightBackground", self.BORDER)
        self.root.option_add("*Entry.highlightColor", self.GOLD)

    def boton(self, parent, texto, comando, color=None, fg=None, compacto=True):
        col = color if color else self.PURPLE
        texto_col = fg if fg else self.WHITE
        b = tk.Button(parent, text=texto, command=comando, bg=col, fg=texto_col,
                      activebackground=self.GOLD_DARK, activeforeground=self.WHITE,
                      font=("Arial", 8 if compacto else 9, "bold"),
                      bd=0, padx=8, pady=5 if compacto else 7,
                      cursor="hand2", wraplength=200, relief="flat",
                      highlightthickness=0)
        b.bind("<Enter>", lambda e: b.configure(highlightthickness=1, highlightbackground=self.TEAL))
        b.bind("<Leave>", lambda e: b.configure(highlightthickness=0))
        return b

    def formulario_modal(self, titulo, campos):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.configure(bg=self.BG)
        ventana.transient(self.root)
        ventana.grab_set()
        ventana.resizable(True, False)
        ventana.geometry("420x{}".format(min(580, 200 + len(campos) * 70)))

        franja = tk.Frame(ventana, bg=self.NAVY, padx=16, pady=12)
        franja.pack(fill="x")
        tk.Frame(franja, bg=self.GOLD, height=3).pack(fill="x", pady=(0, 6))
        tk.Label(franja, text=titulo, bg=self.NAVY, fg=self.TEXT_NAV,
                 font=("Arial", 13, "bold"), wraplength=360,
                 justify="left").pack(anchor="w")

        cuerpo = tk.Frame(ventana, bg=self.BG, padx=18, pady=14)
        cuerpo.pack(fill="both", expand=True)
        controles = {}
        for indice, campo in enumerate(campos):
            etiqueta, valor, opciones = campo
            fg_label = self.TEXT_MAIN
            tk.Label(cuerpo, text=etiqueta, bg=self.BG, fg=fg_label,
                     font=("Arial", 9, "bold")).pack(anchor="w", pady=(4 if indice else 0, 2))
            if opciones:
                control = ttk.Combobox(cuerpo, values=opciones, state="readonly", font=("Arial", 9))
                if valor is not None:
                    control.set(str(valor))
            else:
                control = tk.Entry(cuerpo, font=("Arial", 10), bg=self.WHITE,
                                   fg=fg_label, insertbackground=fg_label,
                                   relief="flat", highlightthickness=1,
                                   highlightbackground=self.BORDER, highlightcolor=self.GOLD, bd=0)
                if valor is not None:
                    control.insert(0, str(valor))
            control.pack(fill="x", ipady=5, pady=(0, 4))
            controles[etiqueta] = control

        pie = tk.Frame(ventana, bg=self.WHITE, padx=16, pady=10,
                       highlightbackground=self.BORDER, highlightthickness=1)
        pie.pack(fill="x", side="bottom")
        resultado = {"valores": None}

        def guardar(event=None):
            valores = {nombre: control.get().strip() for nombre, control in controles.items()}
            if any(not valor for valor in valores.values()):
                messagebox.showwarning("Incompletos", "Completa todos los campos.", parent=ventana)
                return
            resultado["valores"] = valores
            ventana.destroy()

        def cancelar():
            ventana.destroy()

        self.boton(pie, "Cancelar", cancelar, self.WHITE, self.NAVY, True).pack(side="right", padx=(6, 0))
        self.boton(pie, "Guardar", guardar, self.GOLD, self.WHITE, True).pack(side="right")
        ventana.bind("<Return>", guardar)
        ventana.bind("<Escape>", lambda e: cancelar())
        ventana.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - ventana.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - ventana.winfo_height()) // 2
        ventana.geometry(f"+{max(0, x)}+{max(0, y)}")
        ventana.wait_window()
        return resultado["valores"]

    def limpiar_raiz(self):
        for w in self.root.winfo_children():
            w.destroy()

    def detectar_tamano(self, event):
        if event.widget is not self.root:
            return
        compacto = event.width < 930
        if compacto != self.compacto:
            self.compacto = compacto
            if self._resize_job:
                self.root.after_cancel(self._resize_job)
            self._resize_job = self.root.after(100, self.reconstruir_panel)

    def reconstruir_panel(self):
        if not hasattr(self, "contenido") or not self.contenido.winfo_exists():
            return
        pagina = self.pagina
        self.crear_panel(pagina)

    def pantalla_login(self):
        self.limpiar_raiz()
        outer = tk.Frame(self.root, bg=self.NAVY)
        outer.pack(fill="both", expand=True)
        
        caja = tk.Frame(outer, bg=self.WHITE, padx=32, pady=28,
                        highlightbackground=self.GOLD, highlightthickness=2)
        caja.place(relx=.5, rely=.5, anchor="center", width=420)
        
        fg_caja = self.TEXT_MAIN
        
        tk.Label(caja, text="PN", bg=self.NAVY, fg=self.GOLD,
                 font=("Arial", 18, "bold"), width=3, pady=6,
                 highlightbackground=self.GOLD, highlightthickness=2).pack(pady=(0, 12))
        tk.Label(caja, text="PRIMARIA NEZAHUALCÓYOTL", bg=self.WHITE, fg=fg_caja,
                 font=("Arial", 14, "bold"), justify="center").pack(pady=2)
        tk.Label(caja, text="SISTEMA ESCOLAR INTEGRAL", bg=self.WHITE, fg=self.TEAL,
                 font=("Arial", 8, "bold")).pack(pady=(2, 8))
        tk.Frame(caja, bg=self.GOLD, height=2).pack(fill="x", pady=(2, 14))
        
        btn_tema_txt = "🌙 Modo Oscuro" if not self.modo_oscuro else "☀️ Modo Claro"
        self.boton(caja, btn_tema_txt, self.cambiar_tema_login, self.DARK, self.WHITE, True).pack(fill="x", pady=(0, 14))

        tk.Label(caja, text="Usuario", bg=self.WHITE, fg=fg_caja, font=("Arial", 9, "bold")).pack(anchor="w", pady=(0, 2))
        usuario = tk.Entry(caja, font=("Arial", 11), relief="solid", bd=1)
        usuario.pack(fill="x", ipady=6, pady=(0, 10))
        usuario.insert(0, "Director")
        
        tk.Label(caja, text="Contraseña", bg=self.WHITE, fg=fg_caja, font=("Arial", 9, "bold")).pack(anchor="w", pady=(0, 2))
        clave = tk.Entry(caja, show="•", font=("Arial", 11), relief="solid", bd=1)
        clave.pack(fill="x", ipady=6, pady=(0, 6))
        
        tk.Label(caja, text="Credenciales de acceso:\nDirector / 1234  |  Docente / 1234",
                 bg=self.WHITE, fg=self.MUTED, font=("Arial", 8), justify="left").pack(anchor="w", pady=(2, 14))

        def entrar(event=None):
            user = usuario.get().strip()
            passw = clave.get()
            if user.lower() == "director" and passw == "1234":
                self.crear_panel()
            else:
                with self.conectar() as db:
                    docente_db = db.execute("SELECT docente FROM grupos WHERE docente LIKE ? COLLATE NOCASE", (f"%{user}%",)).fetchone()
                if passw == "1234" and (user.lower() == "docente" or docente_db):
                    nombre_docente = docente_db[0] if docente_db else user
                    self.limpiar_raiz()
                    PanelDocente(self.root, nombre_docente, self.modo_oscuro)
                else:
                    messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")
                    
        self.boton(caja, "ENTRAR AL SISTEMA  ›", entrar, self.GOLD, self.WHITE, False).pack(fill="x", ipady=2)
        clave.bind("<Return>", entrar)
        usuario.focus_set()

    def cambiar_tema_login(self):
        self.modo_oscuro = not self.modo_oscuro
        self.actualizar_colores()
        self.configurar_estilos()
        self.pantalla_login()

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar sesión", "¿Deseas salir al inicio de sesión?"):
            self.pantalla_login()

    def crear_panel(self, pagina="Inicio"):
        self.pagina = pagina
        self.limpiar_raiz()
        
        top = tk.Frame(self.root, bg=self.WHITE, padx=14, pady=8,
                       highlightbackground=self.BORDER, highlightthickness=1)
        top.pack(fill="x")
        tk.Frame(top, bg=self.GOLD, height=3).pack(fill="x", pady=(0, 4))
        
        btn_tema_txt = "🌙 Oscuro" if not self.modo_oscuro else "☀️ Claro"
        self.boton(top, btn_tema_txt, self.cambiar_tema, self.DARK, self.WHITE, True).pack(side="right", padx=(6, 0))

        fg_top = self.TEXT_MAIN
        tk.Label(top, text="PRIMARIA NEZAHUALCÓYOTL", bg=self.WHITE, fg=self.TEAL,
                 font=("Arial", 8, "bold")).pack(anchor="w")
        tk.Label(top, text="Panel de Dirección", bg=self.WHITE, fg=fg_top,
                 font=("Arial", 14, "bold")).pack(anchor="w", pady=(1, 0))
        tk.Label(top, text=f"{date.today().strftime('%d/%m/%Y')}",
                 bg=self.WHITE, fg=self.MUTED, font=("Arial", 8)).place(relx=0.85, rely=.5, anchor="e")

        body = tk.Frame(self.root, bg=self.BG)
        body.pack(fill="both", expand=True)
        
        menu_width = 60 if self.compacto else 210
        self.menu = tk.Frame(body, bg=self.NAVY, width=menu_width)
        self.menu.pack(side="left", fill="y")
        self.menu.pack_propagate(False)

        if self.compacto:
            tk.Label(self.menu, text="PN", bg=self.GOLD, fg=self.WHITE,
                     font=("Arial", 11, "bold"), pady=8).pack(fill="x", padx=4, pady=6)
        else:
            tk.Label(self.menu, text="MENÚ DE CONTROL", bg=self.NAVY, fg=self.TEAL,
                     font=("Arial", 9, "bold"), anchor="w").pack(fill="x", padx=12, pady=(10, 4))

        nav = [
            ("⌂", "Inicio", "GENERAL"),
            ("▦", "Grupos y Docentes", "ACADÉMICO"),
            ("✉", "Comunicados Oficiales", "COMUNICACIÓN"),
            ("📖", "Bitácora Directiva", ""),
            ("▦", "Calendario Oficial", "ORGANIZACIÓN"),
            ("!", "Conducta / Incidencias", "SEGUIMIENTO"),
            ("◇", "Cartas Compromiso", ""),
            ("⚑", "Módulo de Alertas", ""),
            ("▥", "Reportes Periódicos", "INFORMES"),
            ("⚙", "Configuración", "SISTEMA")]
        
        for icon, label, category in nav:
            if category and not self.compacto:
                tk.Label(self.menu, text=category, bg=self.NAVY, fg=self.GOLD,
                         font=("Arial", 7, "bold"), anchor="w").pack(fill="x", padx=12, pady=(5, 1))
            text = icon if self.compacto else f"{icon}  {label}"
            
            if self.pagina == label:
                color_btn = self.GOLD
                fg_btn = "#FFFFFF"
            else:
                color_btn = self.NAVY
                fg_btn = self.TEXT_NAV

            self.boton(self.menu, text, lambda p=label: self.mostrar(p),
                       color_btn, fg_btn, True).pack(fill="x", padx=4, pady=1)
            
        tk.Frame(self.menu, bg=self.NAVY).pack(fill="both", expand=True)
        self.boton(self.menu, "⇦" if self.compacto else "Cerrar sesión",
                   self.cerrar_sesion, self.DARK, self.WHITE, True).pack(fill="x", padx=4, pady=6)

        area = tk.Frame(body, bg=self.BG)
        area.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(area, bg=self.BG, highlightthickness=0)
        scroll = ttk.Scrollbar(area, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.contenido = tk.Frame(self.canvas, bg=self.BG)
        self.window_id = self.canvas.create_window((0, 0), window=self.contenido, anchor="nw")
        self.contenido.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window_id, width=e.width))
        self.mostrar(pagina)

    def titulo(self, texto, subtitulo="Resumen general de la actividad escolar"):
        fg_t = self.TEXT_MAIN
        head = tk.Frame(self.contenido, bg=self.BG)
        head.pack(fill="x", padx=14, pady=(12, 6))
        tk.Label(head, text=texto, bg=self.BG, fg=fg_t, font=("Arial", 16, "bold")).pack(anchor="w")
        tk.Frame(head, bg=self.GOLD, height=2, width=50).pack(anchor="w", pady=(4, 3))
        tk.Label(head, text=subtitulo, bg=self.BG, fg=self.MUTED, font=("Arial", 8)).pack(anchor="w")

    def seccion(self, parent, texto):
        fg_sec = self.TEXT_MAIN
        return tk.LabelFrame(parent, text=f"  {texto}  ", bg=self.WHITE, fg=fg_sec,
                             font=("Arial", 9, "bold"), padx=10, pady=10,
                             bd=1, relief="solid", highlightthickness=0, labelanchor="nw")

    def tarjeta(self, parent, nombre, valor, detalle, color):
        card = tk.Frame(parent, bg=self.WHITE, padx=12, pady=10,
                        highlightbackground=self.BORDER, highlightthickness=1)
        tk.Frame(card, bg=self.GOLD, height=2).pack(fill="x", pady=(0, 4))
        tk.Frame(card, bg=color, height=3).pack(fill="x", pady=(0, 6))
        
        fg_card = self.TEXT_MAIN
        tk.Label(card, text=nombre.upper(), bg=self.WHITE, fg=self.MUTED,
                 font=("Arial", 7, "bold"), wraplength=140, justify="left").pack(anchor="w")
        tk.Label(card, text=str(valor), bg=self.WHITE, fg=fg_card,
                 font=("Arial", 18, "bold")).pack(anchor="w", pady=2)
        tk.Label(card, text=detalle, bg=self.WHITE, fg=self.MUTED,
                 font=("Arial", 7), wraplength=150, justify="left").pack(anchor="w")
        return card

    def mostrar(self, pagina):
        self.pagina = pagina
        for w in self.contenido.winfo_children():
            w.destroy()
        self.canvas.yview_moveto(0)
        subtitulos = {
            "Inicio": "Resumen general de la actividad escolar",
            "Grupos y Docentes": "Organización académica y personal docente",
            "Comunicados Oficiales": "Envío y visualización de avisos a la comunidad",
            "Bitácora Directiva": "Registro diario de incidencias y acuerdos institucionales",
            "Calendario Oficial": "Organización de fechas y eventos escolares",
            "Conducta / Incidencias": "Registro confidencial y seguimiento de casos",
            "Cartas Compromiso": "Seguimiento de alumnos con acuerdos de mejora",
            "Módulo de Alertas": "Casos que requieren revisión de dirección",
            "Reportes Periódicos": "Consulta y exportación de información",
            "Configuración": "Parámetros y estado del sistema"}
        self.titulo(pagina, subtitulos.get(pagina, "Gestión escolar"))
        rutas = {
            "Inicio": self.pagina_inicio,
            "Grupos y Docentes": self.pagina_grupos,
            "Comunicados Oficiales": self.pagina_comunicados,
            "Bitácora Directiva": self.pagina_bitacora,
            "Calendario Oficial": self.pagina_calendario,
            "Conducta / Incidencias": lambda: self.pagina_alertas("Conducta / Incidencias"),
            "Cartas Compromiso": lambda: self.pagina_alertas("Cartas Compromiso"),
            "Módulo de Alertas": lambda: self.pagina_alertas("Módulo de Alertas"),
            "Reportes Periódicos": self.pagina_reportes,
            "Configuración": self.pagina_configuracion}
        rutas.get(pagina, self.pagina_inicio)()

    def obtener_metricas(self):
        with self.conectar() as db:
            data = dict(db.execute("SELECT nombre,valor FROM metricas").fetchall())
            total = db.execute("SELECT COUNT(*) FROM alumnos").fetchone()[0]
            if total:
                data["Alumnos"] = total
            return data

    def obtener_alumnos(self):
        with self.conectar() as db:
            return db.execute("SELECT id,nombre,grupo,retardos,faltas FROM alumnos ORDER BY grupo,nombre").fetchall()

    def obtener_grupos(self):
        with self.conectar() as db:
            return db.execute("SELECT id,grupo,docente,alumnos FROM grupos ORDER BY grupo").fetchall()

    def contar_justificantes(self):
        with self.conectar() as db:
            return db.execute("SELECT COUNT(*) FROM justificantes WHERE estado='Pendiente'").fetchone()[0]

    def contar_incidencias(self):
        with self.conectar() as db:
            return db.execute("SELECT COUNT(*) FROM incidencias WHERE estado='Pendiente'").fetchone()[0]

    def pagina_inicio(self):
        m = self.obtener_metricas()
        total = m.get("Alumnos", 0)
        presentes = m.get("Presentes", 0)
        retardos = m.get("Retardos", 0)
        faltas = m.get("Faltas", 0)
        pendientes = self.contar_justificantes()
        incidencias = self.contar_incidencias()
        
        banner = tk.Frame(self.contenido, bg=self.NAVY, padx=14, pady=10,
                          highlightbackground=self.GOLD, highlightthickness=1)
        banner.pack(fill="x", padx=14, pady=(0, 8))
        banner_left = tk.Frame(banner, bg=self.NAVY)
        banner_left.pack(side="left", fill="x", expand=True)
        tk.Label(banner_left, text="CENTRO DE CONTROL ESCOLAR", bg=self.NAVY,
                 fg=self.TEAL, font=("Arial", 8, "bold")).pack(anchor="w")
        tk.Label(banner_left, text="Monitoreo en tiempo real de asistencia, avisos y disciplina.",
                 bg=self.NAVY, fg=self.TEXT_NAV, font=("Arial", 10, "bold"),
                 wraplength=460, justify="left").pack(anchor="w", pady=(2, 0))

        wrap = tk.Frame(self.contenido, bg=self.BG)
        wrap.pack(fill="x", padx=10)
        values = [
            ("Alumnos", total, "Expedientes registrados", self.PURPLE),
            ("Presentes", presentes, f"{presentes / total * 100:.1f}% asistencia" if total else "Sin registros", self.TEAL),
            ("Retardos", retardos, "Registrados hoy", self.TEAL),
            ("Faltas", faltas, "Registradas hoy", self.RED),
            ("Incidencias", incidencias, "Casos pendientes", self.RED_DARK),
            ("Justificantes", pendientes, "Por validar", self.TEAL)]
        for i, val in enumerate(values):
            card = self.tarjeta(wrap, *val)
            card.grid(row=i // 3, column=i % 3, sticky="nsew", padx=3, pady=3)
            wrap.grid_columnconfigure(i % 3, weight=1, uniform="cards")

        bottom = tk.Frame(self.contenido, bg=self.BG)
        bottom.pack(fill="both", expand=True, padx=14, pady=6)
        left = tk.Frame(bottom, bg=self.BG)
        right = tk.Frame(bottom, bg=self.BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        right.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        bottom.grid_columnconfigure(0, weight=3)
        bottom.grid_columnconfigure(1, weight=2)
        
        summary = self.seccion(left, "Gráfico y Estado de Asistencia (Hoy)")
        summary.pack(fill="x", pady=(0, 6))
        
        fg_lbl = self.TEXT_MAIN
        
        grafico_frame = tk.Frame(summary, bg=self.WHITE, padx=4, pady=4)
        grafico_frame.pack(fill="x", pady=(0, 8))
        tk.Label(grafico_frame, text="📊 Gráfica de Barras - Rendimiento Diario", bg=self.WHITE, fg=self.TEAL, font=("Arial", 8, "bold")).pack(anchor="w", pady=(0, 4))

        max_val = max(total, 1)
        for label, number, color in [
            ("Presentes", presentes, self.TEAL),
            ("Retardos", retardos, self.TEAL),
            ("Faltas", faltas, self.RED)]:
            line = tk.Frame(summary, bg=self.WHITE)
            line.pack(fill="x", pady=2)
            tk.Label(line, text=label, bg=self.WHITE, fg=fg_lbl, font=("Arial", 8), width=10, anchor="w").pack(side="left")
            tk.Label(line, text=str(number), bg=self.WHITE, fg=color, font=("Arial", 9, "bold"), width=4).pack(side="left")
            
            barbg = tk.Frame(summary, bg=self.BORDER, height=12)
            barbg.pack(fill="x", pady=(0, 3))
            bar = tk.Frame(barbg, bg=color, height=12)
            bar.place(relx=0, rely=0, relheight=1, relwidth=min(number / max_val, 1))
            
        quick = self.seccion(left, "Accesos rápidos")
        quick.pack(fill="x")
        for label, dest in [("Enviar comunicado", "Comunicados Oficiales"),
                            ("Bitácora directiva", "Bitácora Directiva"),
                            ("Generar reporte", "Reportes Periódicos")]:
            self.boton(quick, label, lambda p=dest: self.mostrar(p),
                       self.BLUE_SOFT, fg_lbl, True).pack(fill="x", pady=1)
            
        alert = self.seccion(right, "Atención directiva")
        alert.pack(fill="both", expand=True, pady=(0, 6))
        self.resumen_alertas(alert, limite=3)
        
        rule = self.seccion(right, "Criterio institucional")
        rule.pack(fill="x")
        tk.Label(rule, text="3 retardos equivalen a 1 falta adicional automática.",
                 bg=self.GREEN_SOFT, fg="#0A2540", font=("Arial", 8, "bold"),
                 wraplength=260, justify="left", padx=6, pady=6).pack(fill="x")

    def crear_tabla(self, parent, columnas, filas, anchos=None, height=7):
        frame = tk.Frame(parent, bg=self.WHITE)
        frame.pack(fill="both", expand=True)
        tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=height)
        vs = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
        hs = ttk.Scrollbar(frame, orient="horizontal", command=tabla.xview)
        tabla.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)
        vs.pack(side="right", fill="y")
        hs.pack(side="bottom", fill="x")
        tabla.pack(side="left", fill="both", expand=True)
        for col in columnas:
            tabla.heading(col, text=col)
            ancho = (anchos or {}).get(col, 100)
            tabla.column(col, width=ancho, minwidth=40, anchor="w" if col in ("Alumno", "Docente", "Motivo", "Descripción", "Nota", "Título", "Mensaje", "Entrada", "Asunto") else "center", stretch=True)
        for fila in filas:
            tabla.insert("", "end", values=fila)
        return tabla

    def pagina_grupos(self):
        box = self.seccion(self.contenido, "Grupos y docentes")
        box.pack(fill="both", padx=14, pady=4)
        actions = tk.Frame(box, bg=self.WHITE)
        actions.pack(fill="x", pady=(0, 6))
        self.boton(actions, "＋ Agregar grupo", self.agregar_grupo, self.GOLD, self.WHITE).pack(side="left", padx=(0, 4))
        self.boton(actions, "Editar grupo", self.editar_grupo, self.DARK, self.WHITE).pack(side="left", padx=2)
        self.boton(actions, "Actualizar", lambda: self.mostrar("Grupos y Docentes"), self.BLUE_SOFT, self.NAVY).pack(side="left", padx=2)
        
        with self.conectar() as db:
            filas = db.execute("""
                SELECT g.grupo,g.docente,g.alumnos,
                COALESCE(SUM(a.retardos),0), COALESCE(SUM(a.faltas),0),
                COALESCE(SUM(CASE WHEN a.faltas>=? THEN 1 ELSE 0 END),0)
                FROM grupos g LEFT JOIN alumnos a ON a.grupo=g.grupo
                GROUP BY g.id ORDER BY 6 DESC,5 DESC
            """, (UMBRAL_FALTAS,)).fetchall()
        self.tabla_grupos_actual = self.crear_tabla(box, ("Grupo", "Docente", "Alumnos", "Retardos", "Faltas", "Alertas"),
                                                    filas, {"Grupo": 70, "Docente": 160}, 5)

    def agregar_grupo(self):
        datos = self.formulario_modal("Agregar grupo", [
            ("Nombre del grupo", "", None),
            ("Nombre del docente", "", None)
        ])
        if not datos: return
        try:
            with self.conectar() as db:
                db.execute("INSERT INTO grupos(grupo,docente,alumnos) VALUES (?,?,0)",
                           (datos["Nombre del grupo"], datos["Nombre del docente"]))
            self.mostrar("Grupos y Docentes")
        except sqlite3.IntegrityError:
            messagebox.showwarning("Grupo existente", "Ese grupo ya está registrado.")

    def editar_grupo(self):
        tabla = getattr(self, "tabla_grupos_actual", None)
        if not tabla or not tabla.selection():
            messagebox.showwarning("Selecciona", "Selecciona un grupo de la tabla.")
            return
        fila = tabla.item(tabla.selection()[0], "values")
        grupo_original = fila[0]
        datos = self.formulario_modal("Editar grupo", [
            ("Nombre del grupo", fila[0], None),
            ("Nombre del docente", fila[1], None)
        ])
        if not datos: return
        try:
            with self.conectar() as db:
                db.execute("UPDATE grupos SET grupo=?, docente=? WHERE grupo=?",
                           (datos["Nombre del grupo"], datos["Nombre del docente"], grupo_original))
                if datos["Nombre del grupo"] != grupo_original:
                    db.execute("UPDATE alumnos SET grupo=? WHERE grupo=?",
                               (datos["Nombre del grupo"], grupo_original))
            self.mostrar("Grupos y Docentes")
        except sqlite3.IntegrityError:
            messagebox.showwarning("Nombre duplicado", "Ya existe un grupo con ese nombre.")

    def alumno_seleccionado(self, tabla=None):
        tabla = tabla or getattr(self, "tabla_alumnos", None)
        if tabla and tabla.selection():
            return tabla.item(tabla.selection()[0], "values")
        return None

    def registrar_seguimiento(self, alumno_id, nombre):
        datos = self.formulario_modal("Registrar seguimiento", [(f"Nota para {nombre}", "", None)])
        if not datos: return
        nota = datos[f"Nota para {nombre}"]
        with self.conectar() as db:
            db.execute("INSERT INTO seguimientos(alumno_id,fecha,nota) VALUES (?,?,?)", (alumno_id, date.today().isoformat(), nota))
        messagebox.showinfo("Guardado", "La nota se registró correctamente.")
        self.mostrar(self.pagina)

    def pagina_comunicados(self):
        box = self.seccion(self.contenido, "Módulo de Comunicados y Avisos Oficiales")
        box.pack(fill="x", padx=14, pady=4)
        self.boton(box, "＋ Redactar Comunicado", self.agregar_comunicado, self.GOLD, self.WHITE).pack(fill="x")

        listing = self.seccion(self.contenido, "Historial de Comunicados Emitidos")
        listing.pack(fill="both", padx=14, pady=6)
        with self.conectar() as db:
            rows = db.execute("SELECT id, fecha, titulo, mensaje FROM comunicados ORDER BY id DESC").fetchall()
        self.crear_tabla(listing, ("ID", "Fecha", "Título", "Mensaje"), rows, {"Título": 160, "Mensaje": 240}, 6)

    def agregar_comunicado(self):
        datos = self.formulario_modal("Nuevo Comunicado", [
            ("Título del aviso", "", None),
            ("Mensaje detallado", "", None)
        ])
        if not datos: return
        with self.conectar() as db:
            db.execute("INSERT INTO comunicados(fecha, titulo, mensaje) VALUES (?,?,?)",
                       (date.today().isoformat(), datos["Título del aviso"], datos["Mensaje detallado"]))
        messagebox.showinfo("Enviado", "El comunicado se ha registrado.")
        self.mostrar("Comunicados Oficiales")

    def pagina_bitacora(self):
        box = self.seccion(self.contenido, "Bitácora Directiva")
        box.pack(fill="x", padx=14, pady=4)
        
        def agregar_entrada():
            datos = self.formulario_modal("Nueva Nota de Bitácora", [("Descripción del evento", "", None)])
            if not datos: return
            with self.conectar() as db:
                db.execute("INSERT INTO bitacora(fecha, entrada) VALUES (?, ?)", (date.today().isoformat(), datos["Descripción del evento"]))
            messagebox.showinfo("Guardado", "Entrada agregada.")
            self.mostrar("Bitácora Directiva")

        self.boton(box, "＋ Nueva entrada en bitácora", agregar_entrada, self.GOLD, self.WHITE).pack(fill="x")

        listing = self.seccion(self.contenido, "Registro Histórico de Bitácora")
        listing.pack(fill="both", padx=14, pady=6)
        with self.conectar() as db:
            rows = db.execute("SELECT id, fecha, entrada FROM bitacora ORDER BY id DESC").fetchall()
        self.crear_tabla(listing, ("ID", "Fecha", "Entrada"), rows, {"Entrada": 280}, 6)

    def resumen_alertas(self, parent, limite=None):
        with self.conectar() as db:
            alumnos = db.execute("SELECT COUNT(*) FROM alumnos WHERE faltas>=? OR retardos>=?", (UMBRAL_FALTAS, UMBRAL_FALTAS)).fetchone()[0]
            just = db.execute("SELECT COUNT(*) FROM justificantes WHERE estado='Pendiente'").fetchone()[0]
            inc = db.execute("SELECT COUNT(*) FROM incidencias WHERE estado='Pendiente'").fetchone()[0]
        items = []
        if alumnos: items.append((f"{alumnos} alumnos con alertas", "Revisar faltas o retardos.", self.RED_SOFT, "Módulo de Alertas"))
        if just: items.append((f"{just} justificantes pendientes", "Validar documentos.", self.LAVENDER, "Módulo de Alertas"))
        if inc: items.append((f"{inc} incidencias sin atender", "Seguimiento de casos.", self.BLUE_SOFT, "Conducta / Incidencias"))
        if not items: items.append(("Sin alertas pendientes", "Todo en orden.", self.GREEN_SOFT, "Módulo de Alertas"))
        
        fg_alt = "#000000"
        for title, detail, color, dest in (items[:limite] if limite else items):
            f = tk.Frame(parent, bg=color, padx=6, pady=6)
            f.pack(fill="x", pady=2)
            tk.Label(f, text=title, bg=color, fg=fg_alt, font=("Arial", 8, "bold"), wraplength=260, justify="left").pack(anchor="w")
            tk.Label(f, text=detail, bg=color, fg=fg_alt, font=("Arial", 7, "bold"), wraplength=260, justify="left").pack(anchor="w", pady=(1, 3))
            self.boton(f, "Abrir", lambda p=dest: self.mostrar(p), self.NAVY, self.WHITE, True).pack(anchor="e")

    def pagina_alertas(self, pagina):
        summary = self.seccion(self.contenido, "Resumen de alertas")
        summary.pack(fill="x", padx=14, pady=4)
        self.resumen_alertas(summary)
        box = self.seccion(self.contenido, "Alumnos que requieren seguimiento")
        box.pack(fill="both", padx=14, pady=6)
        with self.conectar() as db:
            rows = db.execute("SELECT id,nombre,grupo,retardos,faltas FROM alumnos WHERE faltas>=? OR retardos>=? ORDER BY faltas DESC,retardos DESC",
                              (UMBRAL_FALTAS, UMBRAL_FALTAS)).fetchall()
        filas = [(i,n,g,r,f, "Faltas" if f >= UMBRAL_FALTAS else "Retardos") for i,n,g,r,f in rows]
        table = self.crear_tabla(box, ("ID","Alumno","Grupo","Retardos","Faltas","Motivo"), filas, {"Alumno":150,"Motivo":110}, 5)
        table.tag_configure("falta", background=self.RED_SOFT)
        table.tag_configure("retardo", background=self.YELLOW_SOFT)
        for item in table.get_children():
            v = table.item(item, "values")
            table.item(item, tags=("falta" if int(v[4]) >= UMBRAL_FALTAS else "retardo",))
        actions = tk.Frame(box, bg=self.WHITE)
        actions.pack(fill="x", pady=4)
        def selected():
            a = self.alumno_seleccionado(table)
            if not a: messagebox.showwarning("Selecciona", "Selecciona un registro.")
            return a
        self.boton(actions, "Seguimiento", lambda: self._seguimiento_tabla(selected()), self.DARK, self.WHITE).pack(side="left", padx=(0, 4))
        self.boton(actions, "Incidencia", lambda: self._incidencia_tabla(selected()), self.GOLD, self.WHITE).pack(side="left")
        incbox = self.seccion(self.contenido, "Historial de incidencias")
        incbox.pack(fill="both", padx=14, pady=4)
        with self.conectar() as db:
            incs = db.execute("""SELECT i.id,i.fecha,a.nombre,i.tipo,i.descripcion,i.estado
                                  FROM incidencias i JOIN alumnos a ON a.id=i.alumno_id ORDER BY i.id DESC""").fetchall()
        itable = self.crear_tabla(incbox, ("ID","Fecha","Alumno","Tipo","Descripción","Estado"), incs, {"Alumno":120,"Tipo":100,"Descripción":160}, 4)
        def cerrar():
            if not itable.selection():
                messagebox.showwarning("Selecciona", "Selecciona un registro.")
                return
            ident = itable.item(itable.selection()[0], "values")[0]
            with self.conectar() as db:
                db.execute("UPDATE incidencias SET estado='Atendida' WHERE id=?", (ident,))
            self.mostrar(pagina)
        self.boton(incbox, "Marcar atendida", cerrar, self.GREEN_SOFT, self.NAVY).pack(anchor="w", pady=(4, 0))

    def _seguimiento_tabla(self, alumno):
        if alumno: self.registrar_seguimiento(int(alumno[0]), alumno[1])

    def _incidencia_tabla(self, alumno):
        if not alumno: return
        datos = self.formulario_modal("Registrar incidencia", [("Tipo", "", None), ("Descripción", "", None)])
        if not datos: return
        with self.conectar() as db:
            db.execute("INSERT INTO incidencias(alumno_id,fecha,tipo,descripcion) VALUES (?,?,?,?)",
                       (int(alumno[0]), date.today().isoformat(), datos["Tipo"], datos["Descripción"]))
        messagebox.showinfo("Registrado", "Incidencia guardada.")
        self.mostrar(self.pagina)

    def pagina_calendario(self):
        box = self.seccion(self.contenido, "📅 Calendario Escolar Interactivo")
        box.pack(fill="x", padx=14, pady=4)
        
        cal_frame = tk.Frame(box, bg=self.WHITE, padx=10, pady=10)
        cal_frame.pack(fill="x", pady=5)
        
        hoy = datetime.now()
        cal_texto = calendar.month(hoy.year, hoy.month)
        tk.Label(cal_frame, text=f"Calendario del Mes: {hoy.strftime('%B %Y')}", bg=self.WHITE, fg=self.TEAL, font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 4))
        
        lbl_cal = tk.Label(cal_frame, text=cal_texto, bg=self.WHITE, fg=self.TEXT_MAIN, font=("Courier", 10), justify="left")
        lbl_cal.pack(anchor="w")

        self.boton(box, "＋ Agregar evento al calendario", self.agregar_evento, self.GOLD, self.WHITE).pack(fill="x", pady=(8, 0))

        listing = self.seccion(self.contenido, "Eventos Registrados")
        listing.pack(fill="both", padx=14, pady=6)
        with self.conectar() as db:
            rows = db.execute("SELECT id,fecha,titulo FROM eventos ORDER BY fecha").fetchall()
        table = self.crear_tabla(listing, ("ID", "Fecha", "Evento"), rows, {"Evento": 200}, 5)
        actions = tk.Frame(listing, bg=self.WHITE)
        actions.pack(fill="x", pady=(6, 0))
        self.boton(actions, "Editar", lambda: self.editar_evento(table), self.DARK, self.WHITE).pack(side="left", padx=(0, 4))
        self.boton(actions, "Eliminar", lambda: self.eliminar_evento(table), self.RED, self.WHITE).pack(side="left")

    def agregar_evento(self):
        datos = self.formulario_modal("Agregar evento", [("Fecha (AAAA-MM-DD)", date.today().isoformat(), None), ("Nombre del evento", "", None)])
        if not datos: return
        try: datetime.strptime(datos["Fecha (AAAA-MM-DD)"], "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Formato", "Usa el formato AAAA-MM-DD.")
            return
        with self.conectar() as db:
            db.execute("INSERT INTO eventos(fecha,titulo) VALUES (?,?)", (datos["Fecha (AAAA-MM-DD)"], datos["Nombre del evento"]))
        self.mostrar("Calendario Oficial")

    def editar_evento(self, table):
        if not table.selection():
            messagebox.showwarning("Selecciona", "Selecciona un evento.")
            return
        fila = table.item(table.selection()[0], "values")
        datos = self.formulario_modal("Editar evento", [("Fecha (AAAA-MM-DD)", fila[1], None), ("Nombre del evento", fila[2], None)])
        if not datos: return
        try: datetime.strptime(datos["Fecha (AAAA-MM-DD)"], "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Formato", "Usa el formato AAAA-MM-DD.")
            return
        with self.conectar() as db:
            db.execute("UPDATE eventos SET fecha=?, titulo=? WHERE id=?", (datos["Fecha (AAAA-MM-DD)"], datos["Nombre del evento"], fila[0]))
        self.mostrar("Calendario Oficial")

    def eliminar_evento(self, table):
        if not table.selection():
            messagebox.showwarning("Selecciona", "Selecciona un evento.")
            return
        ident = table.item(table.selection()[0], "values")[0]
        if messagebox.askyesno("Eliminar", "¿Deseas eliminar el evento?"):
            with self.conectar() as db:
                db.execute("DELETE FROM eventos WHERE id=?", (ident,))
            self.mostrar("Calendario Oficial")

    def pagina_reportes(self):
        box = self.seccion(self.contenido, "Reportes y exportación")
        box.pack(fill="x", padx=14, pady=4)
        m = self.obtener_metricas()
        fg_m = self.TEXT_MAIN
        for name in ("Alumnos", "Presentes", "Retardos", "Faltas"):
            row = tk.Frame(box, bg=self.WHITE)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=name, bg=self.WHITE, fg=fg_m, font=("Arial", 8)).pack(side="left")
            tk.Label(row, text=str(m.get(name, 0)), bg=self.WHITE, fg=self.TEAL, font=("Arial", 9, "bold")).pack(side="right")
        self.boton(box, "Exportar historial (CSV)", self.exportar_csv, self.GOLD, self.WHITE).pack(fill="x", pady=(6, 0))
        self.boton(box, "Exportar alumnos (CSV)", self.exportar_alumnos, self.BLUE_SOFT, fg_m).pack(fill="x", pady=(4, 0))

    def exportar_csv(self):
        try:
            ruta = os.path.join(BASE_DIR, "reporte_asistencia.csv")
            with self.conectar() as db:
                rows = db.execute("""SELECT a.fecha,al.id,al.nombre,al.grupo,a.estado
                                     FROM asistencias a JOIN alumnos al ON al.id=a.alumno_id
                                     ORDER BY a.fecha DESC""").fetchall()
            with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["Fecha", "ID alumno", "Nombre", "Grupo", "Estado"])
                writer.writerows(rows)
            messagebox.showinfo("Exportado", f"Guardado en:\n{ruta}")
        except OSError as e: messagebox.showerror("Error", str(e))

    def exportar_alumnos(self):
        try:
            ruta = os.path.join(BASE_DIR, "lista_alumnos.csv")
            with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Nombre", "Grupo", "Retardos", "Faltas"])
                writer.writerows(self.obtener_alumnos())
            messagebox.showinfo("Exportado", f"Guardado en:\n{ruta}")
        except OSError as e: messagebox.showerror("Error", str(e))

    def pagina_configuracion(self):
        box = self.seccion(self.contenido, "Preferencias y reglas del sistema")
        box.pack(fill="x", padx=14, pady=4)
        fg_c = self.TEXT_MAIN
        tk.Label(box, text="Regla de asistencia", bg=self.WHITE, fg=fg_c, font=("Arial", 8, "bold")).pack(anchor="w")
        tk.Label(box, text="3 retardos equivalen a 1 falta. Alertas automáticas al llegar a 3 faltas.",
                 bg=self.BLUE_SOFT, fg=fg_c, padx=8, pady=8, justify="left", wraplength=280).pack(fill="x", pady=(3, 8))
        tk.Label(box, text="Base de datos local", bg=self.WHITE, fg=fg_c, font=("Arial", 8, "bold")).pack(anchor="w")
        tk.Label(box, text=DB_PATH, bg=self.WHITE, fg=self.MUTED, wraplength=280, justify="left").pack(anchor="w", pady=(2, 8))
        self.boton(box, "Volver al inicio", lambda: self.mostrar("Inicio"), self.GOLD, self.WHITE).pack(fill="x", pady=(8, 0))


class PanelDocente:
    def __init__(self, root, docente_nombre, modo_oscuro=False):
        self.root = root
        self.docente_nombre = docente_nombre
        self.modo_oscuro = modo_oscuro
        self.actualizar_colores()
        
        self.root.title(f"Primaria Nezahualcóyotl | Panel Docente - {docente_nombre}")
        self.root.geometry("1280x820")
        self.root.minsize(320, 480)
        self.root.configure(bg=self.BG)
        self.pagina = "Mis Alumnos"
        self.compacto = False
        self._resize_job = None
        self.obtener_grupos_docente()
        self.configurar_estilos()
        self.root.bind("<Configure>", self.detectar_tamano)
        self.crear_panel(self.pagina)

    def actualizar_colores(self):
        t = TEMAS["oscuro"] if self.modo_oscuro else TEMAS["claro"]
        self.BG = t["BG"]
        self.WHITE = t["WHITE"]
        self.NAVY = t["NAVY"]
        self.DARK = t["DARK"]
        self.PURPLE = t["PURPLE"]
        self.GOLD = t["GOLD"]
        self.GOLD_LIGHT = t["GOLD_LIGHT"]
        self.GOLD_DARK = t["GOLD_DARK"]
        self.LAVENDER = t["LAVENDER"]
        self.MUTED = t["MUTED"]
        self.BORDER = t["BORDER"]
        self.BLUE_SOFT = t["BLUE_SOFT"]
        self.GREEN_SOFT = t["GREEN_SOFT"]
        self.YELLOW_SOFT = t["YELLOW_SOFT"]
        self.RED_SOFT = t["RED_SOFT"]
        self.RED = t["RED"]
        self.RED_DARK = t["RED_DARK"]
        self.TEAL = t["TEAL"]
        self.TEXT_NAV = t["TEXT_NAV"]
        self.TEXT_MAIN = t["TEXT_MAIN"]

    def cambiar_tema(self):
        self.modo_oscuro = not self.modo_oscuro
        self.actualizar_colores()
        self.configurar_estilos()
        self.crear_panel(self.pagina)

    def conectar(self):
        db = sqlite3.connect(DB_PATH)
        db.execute("PRAGMA foreign_keys = ON")
        return db

    def obtener_grupos_docente(self):
        with self.conectar() as db:
            if self.docente_nombre.lower() in ("docente", "todos"):
                self.grupos = [row[0] for row in db.execute("SELECT grupo FROM grupos").fetchall()]
            else:
                self.grupos = [row[0] for row in db.execute("SELECT grupo FROM grupos WHERE docente LIKE ?", (f"%{self.docente_nombre}%",)).fetchall()]
        if not self.grupos:
            with self.conectar() as db:
                self.grupos = [row[0] for row in db.execute("SELECT grupo FROM grupos").fetchall()[:1]]

    def configurar_estilos(self):
        s = ttk.Style()
        try: s.theme_use("clam")
        except tk.TclError: pass
        
        fg_tabla = "#F8FAFC" if self.modo_oscuro else "#0A2540"
        bg_tabla = "#0D1B2A" if self.modo_oscuro else "#FFFFFF"
        header_bg = "#1B263B" if self.modo_oscuro else "#0A2540"
        header_fg = "#38BDF8" if self.modo_oscuro else "#FFFFFF"

        s.configure("Treeview", background=bg_tabla, foreground=fg_tabla,
                    fieldbackground=bg_tabla, rowheight=32, borderwidth=0, font=("Arial", 9))
        s.configure("Treeview.Heading", background=header_bg, foreground=header_fg,
                    font=("Arial", 9, "bold"), padding=(6, 8), relief="flat")
        s.map("Treeview", background=[("selected", self.GOLD)], foreground=[("selected", "#FFFFFF" if self.modo_oscuro else "#0A2540")])
        s.configure("TCombobox", padding=5, font=("Arial", 9), fieldbackground=bg_tabla, background=bg_tabla, foreground=fg_tabla)

    def boton(self, parent, texto, comando, color=None, fg=None, compacto=True):
        col = color if color else self.PURPLE
        texto_col = fg if fg else self.WHITE
        b = tk.Button(parent, text=texto, command=comando, bg=col, fg=texto_col,
                      activebackground=self.GOLD_DARK, activeforeground=self.WHITE,
                      font=("Arial", 8 if compacto else 9, "bold"), bd=0, padx=8, pady=5 if compacto else 7,
                      cursor="hand2", wraplength=200, relief="flat", highlightthickness=0)
        b.bind("<Enter>", lambda e: b.configure(highlightthickness=1, highlightbackground=self.TEAL))
        b.bind("<Leave>", lambda e: b.configure(highlightthickness=0))
        return b

    def formulario_modal(self, titulo, campos):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.configure(bg=self.BG)
        ventana.transient(self.root)
        ventana.grab_set()
        ventana.resizable(True, False)
        ventana.geometry("420x{}".format(min(580, 200 + len(campos) * 70)))

        franja = tk.Frame(ventana, bg=self.NAVY, padx=16, pady=12)
        franja.pack(fill="x")
        tk.Frame(franja, bg=self.GOLD, height=3).pack(fill="x", pady=(0, 6))
        tk.Label(franja, text=titulo, bg=self.NAVY, fg=self.TEXT_NAV, font=("Arial", 13, "bold"), wraplength=360, justify="left").pack(anchor="w")

        cuerpo = tk.Frame(ventana, bg=self.BG, padx=18, pady=14)
        cuerpo.pack(fill="both", expand=True)
        controles = {}
        fg_l = self.TEXT_MAIN
        for indice, campo in enumerate(campos):
            etiqueta, valor, opciones = campo
            tk.Label(cuerpo, text=etiqueta, bg=self.BG, fg=fg_l, font=("Arial", 9, "bold")).pack(anchor="w", pady=(4 if indice else 0, 2))
            if opciones:
                control = ttk.Combobox(cuerpo, values=opciones, state="readonly", font=("Arial", 9))
                if valor is not None: control.set(str(valor))
            else:
                control = tk.Entry(cuerpo, font=("Arial", 10), bg=self.WHITE, fg=fg_l, insertbackground=fg_l, relief="flat", highlightthickness=1, highlightbackground=self.BORDER, highlightcolor=self.GOLD, bd=0)
                if valor is not None: control.insert(0, str(valor))
            control.pack(fill="x", ipady=5, pady=(0, 4))
            controles[etiqueta] = control

        pie = tk.Frame(ventana, bg=self.WHITE, padx=16, pady=10, highlightbackground=self.BORDER, highlightthickness=1)
        pie.pack(fill="x", side="bottom")
        resultado = {"valores": None}

        def guardar(event=None):
            valores = {nombre: control.get().strip() for nombre, control in controles.items()}
            if any(not valor for valor in valores.values()):
                messagebox.showwarning("Incompletos", "Completa todos los campos.", parent=ventana)
                return
            resultado["valores"] = valores
            ventana.destroy()

        def cancelar(): ventana.destroy()

        self.boton(pie, "Cancelar", cancelar, self.WHITE, self.NAVY, True).pack(side="right", padx=(6, 0))
        self.boton(pie, "Guardar", guardar, self.GOLD, self.WHITE, True).pack(side="right")
        ventana.bind("<Return>", guardar)
        ventana.bind("<Escape>", lambda e: cancelar())
        ventana.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - ventana.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - ventana.winfo_height()) // 2
        ventana.geometry(f"+{max(0, x)}+{max(0, y)}")
        ventana.wait_window()
        return resultado["valores"]

    def limpiar_raiz(self):
        for w in self.root.winfo_children(): w.destroy()

    def detectar_tamano(self, event):
        if event.widget is not self.root: return
        compacto = event.width < 930
        if compacto != self.compacto:
            self.compacto = compacto
            if self._resize_job: self.root.after_cancel(self._resize_job)
            self._resize_job = self.root.after(100, self.reconstruir_panel)

    def reconstruir_panel(self):
        if not hasattr(self, "contenido") or not self.contenido.winfo_exists(): return
        pagina = self.pagina
        self.crear_panel(pagina)

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar sesión", "¿Deseas salir al inicio de sesión?"):
            self.limpiar_raiz()
            PanelDireccion(self.root, self.modo_oscuro)

    def crear_panel(self, pagina="Mis Alumnos"):
        self.pagina = pagina
        self.limpiar_raiz()
        top = tk.Frame(self.root, bg=self.WHITE, padx=14, pady=8, highlightbackground=self.BORDER, highlightthickness=1)
        top.pack(fill="x")
        tk.Frame(top, bg=self.GOLD, height=3).pack(fill="x", pady=(0, 4))
        
        btn_tema_txt = "🌙 Oscuro" if not self.modo_oscuro else "☀️ Claro"
        self.boton(top, btn_tema_txt, self.cambiar_tema, self.DARK, self.WHITE, True).pack(side="right", padx=(6, 0))

        fg_top = self.TEXT_MAIN
        tk.Label(top, text="PRIMARIA NEZAHUALCÓYOTL", bg=self.WHITE, fg=self.TEAL, font=("Arial", 8, "bold")).pack(anchor="w")
        tk.Label(top, text=f"Panel Docente: {self.docente_nombre}", bg=self.WHITE, fg=fg_top, font=("Arial", 14, "bold")).pack(anchor="w", pady=(1, 0))
        tk.Label(top, text=f"{date.today().strftime('%d/%m/%Y')}", bg=self.WHITE, fg=self.MUTED, font=("Arial", 8)).place(relx=0.85, rely=.5, anchor="e")

        body = tk.Frame(self.root, bg=self.BG)
        body.pack(fill="both", expand=True)
        menu_width = 60 if self.compacto else 210
        self.menu = tk.Frame(body, bg=self.NAVY, width=menu_width)
        self.menu.pack(side="left", fill="y")
        self.menu.pack_propagate(False)

        if self.compacto:
            tk.Label(self.menu, text="PN", bg=self.GOLD, fg=self.WHITE, font=("Arial", 11, "bold"), pady=8).pack(fill="x", padx=4, pady=6)
        else:
            tk.Label(self.menu, text="MENÚ DOCENTE", bg=self.NAVY, fg=self.TEAL, font=("Arial", 9, "bold"), anchor="w").pack(fill="x", padx=12, pady=(10, 4))

        # SE RESTAURARON ALUMNOS, ASISTENCIA Y JUSTIFICANTES; SE QUITARON TAREAS, CALIFICACIONES Y MATERIAL DIDÁCTICO
        nav = [
            ("♙", "Mis Alumnos", "ACADÉMICO"),
            ("✓", "Asistencia", ""),
            ("▤", "Justificantes", ""),
            ("📅", "Horario de Clases", "ORGANIZACIÓN"),
            ("!", "Reportar Incidencia", "SEGUIMIENTO"),
            ("💬", "Mensajes a Dirección", ""),
            ("⚙", "Resumen del Grupo", "INFORMACIÓN")]
        
        for icon, label, category in nav:
            if category and not self.compacto:
                tk.Label(self.menu, text=category, bg=self.NAVY, fg=self.GOLD, font=("Arial", 7, "bold"), anchor="w").pack(fill="x", padx=12, pady=(5, 1))
            text = icon if self.compacto else f"{icon}  {label}"
            
            if self.pagina == label:
                color_btn = self.GOLD
                fg_btn = "#FFFFFF"
            else:
                color_btn = self.NAVY
                fg_btn = self.TEXT_NAV

            self.boton(self.menu, text, lambda p=label: self.mostrar(p), color_btn, fg_btn, True).pack(fill="x", padx=4, pady=1)
            
        tk.Frame(self.menu, bg=self.NAVY).pack(fill="both", expand=True)
        self.boton(self.menu, "⇦" if self.compacto else "Cerrar sesión", self.cerrar_sesion, self.DARK, self.WHITE, True).pack(fill="x", padx=4, pady=6)

        area = tk.Frame(body, bg=self.BG)
        area.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(area, bg=self.BG, highlightthickness=0)
        scroll = ttk.Scrollbar(area, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.contenido = tk.Frame(self.canvas, bg=self.BG)
        self.window_id = self.canvas.create_window((0, 0), window=self.contenido, anchor="nw")
        self.contenido.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window_id, width=e.width))
        self.mostrar(pagina)

    def titulo(self, texto, subtitulo="Gestión de grupo y alumnos asignados"):
        fg_t = self.TEXT_MAIN
        head = tk.Frame(self.contenido, bg=self.BG)
        head.pack(fill="x", padx=14, pady=(12, 6))
        tk.Label(head, text=texto, bg=self.BG, fg=fg_t, font=("Arial", 16, "bold")).pack(anchor="w")
        tk.Frame(head, bg=self.GOLD, height=2, width=50).pack(anchor="w", pady=(4, 3))
        tk.Label(head, text=subtitulo, bg=self.BG, fg=self.MUTED, font=("Arial", 8)).pack(anchor="w")

    def seccion(self, parent, texto):
        fg_sec = self.TEXT_MAIN
        return tk.LabelFrame(parent, text=f"  {texto}  ", bg=self.WHITE, fg=fg_sec, font=("Arial", 9, "bold"), padx=10, pady=10, bd=1, relief="solid", highlightthickness=0, labelanchor="nw")

    def crear_tabla(self, parent, columnas, filas, anchos=None, height=7):
        frame = tk.Frame(parent, bg=self.WHITE)
        frame.pack(fill="both", expand=True)
        tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=height)
        vs = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
        hs = ttk.Scrollbar(frame, orient="horizontal", command=tabla.xview)
        tabla.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)
        vs.pack(side="right", fill="y")
        hs.pack(side="bottom", fill="x")
        tabla.pack(side="left", fill="both", expand=True)
        for col in columnas:
            tabla.heading(col, text=col)
            ancho = (anchos or {}).get(col, 100)
            tabla.column(col, width=ancho, minwidth=40, anchor="w" if col in ("Alumno", "Motivo", "Descripción", "Nota", "Título", "Asunto", "Mensaje") else "center", stretch=True)
        for fila in filas: tabla.insert("", "end", values=fila)
        return tabla

    def mostrar(self, pagina):
        self.pagina = pagina
        for w in self.contenido.winfo_children(): w.destroy()
        self.canvas.yview_moveto(0)
        subtitulos = {
            "Mis Alumnos": "Alumnos inscritos en tus grupos asignados",
            "Asistencia": "Registro diario y consulta del historial de asistencia",
            "Justificantes": "Visualización y registro de justificantes de alumnos",
            "Horario de Clases": "Organización semanal de materias y horarios",
            "Reportar Incidencia": "Registro y notificación de situaciones de conducta",
            "Mensajes a Dirección": "Comunicación directa con la administración",
            "Resumen del Grupo": "Estadísticas generales y estado de asistencia"}
        self.titulo(pagina, subtitulos.get(pagina, "Panel Docente"))
        rutas = {
            "Mis Alumnos": self.pagina_mis_alumnos,
            "Asistencia": self.pagina_asistencia,
            "Justificantes": self.pagina_justificantes,
            "Horario de Clases": self.pagina_horario,
            "Reportar Incidencia": self.pagina_reportar_incidencia,
            "Mensajes a Dirección": self.pagina_mensajes,
            "Resumen del Grupo": self.pagina_resumen_grupo}
        rutas.get(pagina, self.pagina_mis_alumnos)()

    def obtener_alumnos_docente(self):
        with self.conectar() as db:
            if not self.grupos: return []
            placeholders = ",".join(["?"] * len(self.grupos))
            return db.execute(f"SELECT id, nombre, grupo, retardos, faltas FROM alumnos WHERE grupo IN ({placeholders}) ORDER BY grupo, nombre", self.grupos).fetchall()

    def pagina_mis_alumnos(self):
        box = self.seccion(self.contenido, f"Alumnos: {', '.join(self.grupos)}")
        box.pack(fill="both", padx=14, pady=4)
        actions = tk.Frame(box, bg=self.WHITE)
        actions.pack(fill="x", pady=(0, 6))
        self.boton(actions, "Seguimiento", self.seguimiento_docente, self.GOLD, self.WHITE).pack(side="left", padx=(0, 4))
        self.boton(actions, "Actualizar", lambda: self.mostrar("Mis Alumnos"), self.BLUE_SOFT, self.NAVY).pack(side="left")

        filas = []
        for ident, nombre, grupo, retardos, faltas in self.obtener_alumnos_docente():
            estado = "Atención" if faltas >= UMBRAL_FALTAS else "Retardos" if retardos else "Regular"
            filas.append((ident, nombre, grupo, retardos, faltas, estado))
        self.tabla_alumnos_doc = self.crear_tabla(box, ("ID", "Alumno", "Grupo", "Retardos", "Faltas", "Estado"), filas, {"Alumno": 180, "Estado": 120}, 8)
        self.tabla_alumnos_doc.tag_configure("retardo", background=self.YELLOW_SOFT)
        self.tabla_alumnos_doc.tag_configure("falta", background=self.RED_SOFT)
        for item in self.tabla_alumnos_doc.get_children():
            vals = self.tabla_alumnos_doc.item(item, "values")
            if int(vals[4]) >= UMBRAL_FALTAS: self.tabla_alumnos_doc.item(item, tags=("falta",))
            elif int(vals[3]) > 0: self.tabla_alumnos_doc.item(item, tags=("retardo",))

    def seguimiento_docente(self):
        tabla = getattr(self, "tabla_alumnos_doc", None)
        if not tabla or not tabla.selection():
            messagebox.showwarning("Selecciona", "Selecciona un alumno de la tabla.")
            return
        fila = tabla.item(tabla.selection()[0], "values")
        alumno_id, nombre = int(fila[0]), fila[1]
        datos = self.formulario_modal("Registrar seguimiento", [(f"Nota para {nombre}", "", None)])
        if not datos: return
        nota = datos[f"Nota para {nombre}"]
        with self.conectar() as db:
            db.execute("INSERT INTO seguimientos(alumno_id,fecha,nota) VALUES (?,?,?)", (alumno_id, date.today().isoformat(), nota))
        messagebox.showinfo("Guardado", "Nota registrada correctamente.")
        self.mostrar("Mis Alumnos")

    def pagina_asistencia(self):
        box = self.seccion(self.contenido, "Registrar asistencia diaria")
        box.pack(fill="x", padx=14, pady=4)
        alumnos = self.obtener_alumnos_docente()
        if not alumnos:
            tk.Label(box, text="No hay alumnos asignados.", bg=self.WHITE, fg=self.NAVY).pack(anchor="w")
            return
        opts = {f"{a[0]} · {a[1]} ({a[2]})": a[0] for a in alumnos}
        alumno_var = tk.StringVar(value=next(iter(opts)))
        estado_var = tk.StringVar(value="Presente")
        form = tk.Frame(box, bg=self.WHITE)
        form.pack(fill="x")
        fg_l = self.TEXT_MAIN
        tk.Label(form, text="Alumno", bg=self.WHITE, fg=fg_l, font=("Arial", 8, "bold")).pack(anchor="w")
        ttk.Combobox(form, textvariable=alumno_var, values=list(opts), state="readonly").pack(fill="x", pady=(2, 6))
        tk.Label(form, text="Estado", bg=self.WHITE, fg=fg_l, font=("Arial", 8, "bold")).pack(anchor="w")
        ttk.Combobox(form, textvariable=estado_var, values=["Presente", "Retardo", "Falta"], state="readonly").pack(fill="x", pady=(2, 6))

        def guardar():
            alumno_id = opts.get(alumno_var.get())
            if not alumno_id: return
            hoy = date.today().isoformat()
            estado = estado_var.get()
            try:
                with self.conectar() as db:
                    if db.execute("SELECT 1 FROM asistencias WHERE alumno_id=? AND fecha=?", (alumno_id, hoy)).fetchone():
                        messagebox.showwarning("Aviso", "Ya hay asistencia registrada para este alumno hoy.")
                        return
                    db.execute("INSERT INTO asistencias(alumno_id,fecha,estado) VALUES (?,?,?)", (alumno_id, hoy, estado))
                    if estado == "Retardo":
                        db.execute("UPDATE alumnos SET retardos=retardos+1 WHERE id=?", (alumno_id,))
                        r = db.execute("SELECT retardos FROM alumnos WHERE id=?", (alumno_id,)).fetchone()[0]
                        if r % UMBRAL_FALTAS == 0:
                            db.execute("UPDATE alumnos SET faltas=faltas+1 WHERE id=?", (alumno_id,))
                    elif estado == "Falta":
                        db.execute("UPDATE alumnos SET faltas=faltas+1 WHERE id=?", (alumno_id,))
                messagebox.showinfo("Guardado", "Asistencia registrada correctamente.")
                self.mostrar("Asistencia")
            except sqlite3.Error as e:
                messagebox.showerror("Error", str(e))
        self.boton(box, "Guardar asistencia", guardar, self.GOLD, self.WHITE).pack(fill="x", pady=(3, 0))
        hist = self.seccion(self.contenido, "Historial reciente de asistencia")
        hist.pack(fill="both", padx=14, pady=6)
        with self.conectar() as db:
            placeholders = ",".join(["?"] * len(self.grupos)) if self.grupos else "''"
            rows = db.execute(f"""SELECT a.fecha, al.nombre, al.grupo, a.estado FROM asistencias a
                                 JOIN alumnos al ON al.id = a.alumno_id
                                 WHERE al.grupo IN ({placeholders}) ORDER BY a.id DESC LIMIT 40""", self.grupos).fetchall()
        self.crear_tabla(hist, ("Fecha", "Alumno", "Grupo", "Estado"), rows, {"Alumno": 180}, 6)

    def pagina_justificantes(self):
        box = self.seccion(self.contenido, "Justificantes escolares")
        box.pack(fill="x", padx=14, pady=4)
        
        def registrar_justificante():
            alumnos = self.obtener_alumnos_docente()
            nombres_alumnos = [a[1] for a in alumnos]
            datos = self.formulario_modal("Registrar justificante", [
                ("Nombre del alumno", nombres_alumnos[0] if nombres_alumnos else "", nombres_alumnos if nombres_alumnos else None),
                ("Motivo", "", None)
            ])
            if not datos: return
            nombre_al = datos["Nombre del alumno"]
            grupo_al = next((a[2] for a in alumnos if a[1] == nombre_al), self.grupos[0])
            with self.conectar() as db:
                db.execute("INSERT INTO justificantes(alumno, grupo, fecha, motivo) VALUES (?,?,?,?)",
                           (nombre_al, grupo_al, date.today().isoformat(), datos["Motivo"]))
            messagebox.showinfo("Guardado", "Justificante registrado.")
            self.mostrar("Justificantes")

        self.boton(box, "＋ Registrar justificante", registrar_justificante, self.GOLD, self.WHITE).pack(fill="x")

        listing = self.seccion(self.contenido, "Justificantes de tus grupos")
        listing.pack(fill="both", padx=14, pady=6)
        with self.conectar() as db:
            placeholders = ",".join(["?"] * len(self.grupos)) if self.grupos else "''"
            rows = db.execute(f"SELECT id, alumno, grupo, fecha, motivo, estado FROM justificantes WHERE grupo IN ({placeholders}) ORDER BY id DESC", self.grupos).fetchall()
        self.crear_tabla(listing, ("ID", "Alumno", "Grupo", "Fecha", "Motivo", "Estado"), rows, {"Alumno": 140, "Motivo": 180}, 6)

    def pagina_horario(self):
        box = self.seccion(self.contenido, "Horario de Clases Semanal")
        box.pack(fill="both", padx=14, pady=4)
        fg_l = self.TEXT_MAIN
        tk.Label(box, text=f"Distribución de horarios para los grupos: {', '.join(self.grupos)}", bg=self.WHITE, fg=fg_l, font=("Arial", 9, "bold")).pack(anchor="w", pady=(0, 8))
        
        horario_ejemplo = [
            ("Lunes", "08:00 - 09:00", "Español", self.grupos[0] if self.grupos else "2° A"),
            ("Lunes", "09:00 - 10:00", "Matemáticas", self.grupos[0] if self.grupos else "2° A"),
            ("Martes", "08:00 - 09:00", "Ciencias Naturales", self.grupos[0] if self.grupos else "2° A"),
            ("Miércoles", "10:00 - 11:00", "Educación Física", self.grupos[0] if self.grupos else "2° A"),
            ("Jueves", "09:00 - 10:00", "Historia / Geografía", self.grupos[0] if self.grupos else "2° A"),
            ("Viernes", "08:00 - 09:00", "Artes y Manualidades", self.grupos[0] if self.grupos else "2° A")
        ]
        self.crear_tabla(box, ("Día", "Horario", "Asignatura", "Grupo"), horario_ejemplo, {"Día": 100, "Horario": 120, "Asignatura": 160}, 6)

    def pagina_mensajes(self):
        box = self.seccion(self.contenido, "Mensajes y Solicitudes a Dirección")
        box.pack(fill="x", padx=14, pady=4)
        
        def enviar_mensaje():
            datos = self.formulario_modal("Nuevo Mensaje", [("Asunto", "", None), ("Mensaje", "", None)])
            if not datos: return
            with self.conectar() as db:
                db.execute("INSERT INTO mensajes_docente(docente, fecha, asunto, mensaje) VALUES (?,?,?,?)",
                           (self.docente_nombre, date.today().isoformat(), datos["Asunto"], datos["Mensaje"]))
            messagebox.showinfo("Enviado", "Mensaje enviado a la dirección correctamente.")
            self.mostrar("Mensajes a Dirección")

        self.boton(box, "＋ Enviar mensaje a dirección", enviar_mensaje, self.GOLD, self.WHITE).pack(fill="x")

        listing = self.seccion(self.contenido, "Historial de Mensajes Enviados")
        listing.pack(fill="both", padx=14, pady=6)
        with self.conectar() as db:
            rows = db.execute("SELECT fecha, asunto, mensaje FROM mensajes_docente WHERE docente=? ORDER BY id DESC", (self.docente_nombre,)).fetchall()
        if not rows:
            rows = [("2026-10-28", "Solicitud de material deportivo", "Requerimos balones para la clase de educación física.")]
        self.crear_tabla(listing, ("Fecha", "Asunto", "Mensaje"), rows, {"Asunto": 160, "Mensaje": 260}, 5)

    def pagina_reportar_incidencia(self):
        box = self.seccion(self.contenido, "Reportar incidencia")
        box.pack(fill="x", padx=14, pady=4)
        alumnos = self.obtener_alumnos_docente()
        if not alumnos:
            tk.Label(box, text="No hay alumnos.", bg=self.WHITE, fg=self.NAVY).pack(anchor="w")
            return
        opts = {f"{a[0]} · {a[1]} ({a[2]})": a[0] for a in alumnos}
        alumno_var = tk.StringVar(value=next(iter(opts)))
        fg_l = self.TEXT_MAIN
        tk.Label(box, text="Alumno", bg=self.WHITE, fg=fg_l, font=("Arial", 8, "bold")).pack(anchor="w")
        ttk.Combobox(box, textvariable=alumno_var, values=list(opts), state="readonly").pack(fill="x", pady=(2, 6))

        datos = [("Tipo", "", None), ("Descripción", "", None)]
        controles = {}
        for campo, val, opts_c in datos:
            tk.Label(box, text=campo, bg=self.WHITE, fg=fg_l, font=("Arial", 8, "bold")).pack(anchor="w", pady=(2, 1))
            c = tk.Entry(box, font=("Arial", 9), bg=self.WHITE, fg=fg_l, relief="solid", bd=1)
            c.pack(fill="x", ipady=4, pady=(0, 4))
            controles[campo] = c

        def guardar():
            alumno_id = opts.get(alumno_var.get())
            tipo = controles["Tipo"].get().strip()
            desc = controles["Descripción"].get().strip()
            if not tipo or not desc:
                messagebox.showwarning("Incompletos", "Completa todos los campos.")
                return
            with self.conectar() as db:
                db.execute("INSERT INTO incidencias(alumno_id, fecha, tipo, descripcion, estado) VALUES (?,?,?,?, 'Pendiente')",
                           (alumno_id, date.today().isoformat(), tipo, desc))
            messagebox.showinfo("Enviado", "Incidencia reportada a dirección.")
            self.mostrar("Reportar Incidencia")

        self.boton(box, "Enviar a dirección", guardar, self.GOLD, self.WHITE).pack(fill="x", pady=(3, 0))

    def pagina_resumen_grupo(self):
        box = self.seccion(self.contenido, "Estadísticas y Gráfica del Grupo")
        box.pack(fill="fill", padx=14, pady=4)
        alumnos = self.obtener_alumnos_docente()
        total = len(alumnos)
        con_faltas = sum(1 for a in alumnos if a[4] >= UMBRAL_FALTAS)
        con_retardos = sum(1 for a in alumnos if a[3] > 0 and a[4] < UMBRAL_FALTAS)
        regulares = total - con_faltas - con_retardos

        fg_lbl = self.TEXT_MAIN
        tk.Label(box, text=f"Docente: {self.docente_nombre}", bg=self.WHITE, fg=fg_lbl, font=("Arial", 9, "bold")).pack(anchor="w", pady=2)
        tk.Label(box, text=f"Grupos a cargo: {', '.join(self.grupos)}", bg=self.WHITE, fg=self.MUTED, font=("Arial", 8)).pack(anchor="w", pady=1)
        tk.Label(box, text=f"Total de alumnos matriculados: {total}", bg=self.WHITE, fg=fg_lbl, font=("Arial", 8)).pack(anchor="w", pady=(1, 8))

        tk.Label(box, text="📊 Distribución de Estado del Grupo", bg=self.WHITE, fg=self.TEAL, font=("Arial", 9, "bold")).pack(anchor="w", pady=(4, 4))
        
        max_val = max(total, 1)
        categorias = [
            ("Regulares / Normales", regulares, self.TEAL),
            ("Con Retardos", con_retardos, self.GOLD_DARK),
            ("Con Faltas (Alerta)", con_faltas, self.RED)
        ]
        
        for label, count, color in categorias:
            fila_grafica = tk.Frame(box, bg=self.WHITE)
            fila_grafica.pack(fill="x", pady=3)
            tk.Label(fila_grafica, text=label, bg=self.WHITE, fg=fg_lbl, font=("Arial", 8), width=20, anchor="w").pack(side="left")
            tk.Label(fila_grafica, text=str(count), bg=self.WHITE, fg=color, font=("Arial", 9, "bold"), width=4).pack(side="left")
            
            barra_fondo = tk.Frame(box, bg=self.BORDER, height=14)
            barra_fondo.pack(fill="x", pady=(0, 4))
            barra_progreso = tk.Frame(barra_fondo, bg=color, height=14)
            barra_progreso.place(relx=0, rely=0, relheight=1, relwidth=min(count / max_val, 1))


if __name__ == "__main__":
    ventana = tk.Tk()
    app = PanelDireccion(ventana)
    ventana.mainloop()