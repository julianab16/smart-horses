from game import tableroObj, algoritmoMinMax
import tkinter as tk
from tkinter import  ttk
import pygame
import os

class JuegoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Caballos - Minimax")
        self.root.geometry("950x720")
        self.root.configure(bg="#1c1c1c")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1c1c1c")
        style.configure("Title.TLabel", background="#1c1c1c", foreground="white",
                        font=("Consolas", 30, "bold"))
        style.configure("Sub.TLabel", background="#1c1c1c", foreground="#cccccc",
                        font=("Consolas", 14))
        style.configure("Menu.TButton", font=("Consolas", 16, "bold"),
                        padding=10, width=18)

        self.tablero = None
        self.jugador = None
        self.maquina = None
        self.minmax = None
        self.turno = 0
        self.movimientos_validos_pos = {}
        self.inicializar_musica_sin_reproducir()
        self.crear_pantalla_inicio()
        self.heuristica = 0
    
    def inicializar_musica_sin_reproducir(self):
        """Inicializa pygame mixer SIN reproducir música"""
        try:
            pygame.mixer.init()
            self.musica_activada = True
            self.musica_cargada = False  # ✅ Nueva variable para controlar si ya se cargó
            print("🎵 Sistema de audio inicializado (música en espera)")
        except pygame.error:
            print("No se pudo inicializar el sistema de audio")
            self.musica_activada = False
            self.musica_cargada = False

    def cargar_y_reproducir_musica(self):
        if not self.musica_activada or self.musica_cargada:
            return
            
        try:
            # ✅ Buscar archivo de música
            archivos_musica = [
                "musica/musica_deftones.mp3",
                "musica/background_music.mp3",
            ]
            archivo_encontrado = None
            
            for archivo in archivos_musica:
                if os.path.exists(archivo):
                    archivo_encontrado = archivo
                    break
            
            if archivo_encontrado:
                pygame.mixer.music.load(archivo_encontrado)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)  # Repetir infinitamente
                self.musica_cargada = True
                print(f"🎵 Música iniciada: {archivo_encontrado}")
            else:
                print("⚠️ No se encontró archivo de música")
                self.musica_activada = False
                
        except pygame.error as e:
            print(f"Error cargando música: {e}")
            self.musica_activada = False

    def toggle_musica(self):
        """Activar/Desactivar música"""
        if not self.musica_activada:
            return
            
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            return False  # Música pausada
        else:
            pygame.mixer.music.unpause()
            return True   # Música reproduciendo
    
    def crear_pantalla_inicio(self):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # ✅ Fondo con degradado simulado que se ajusta al tamaño
        main_frame = tk.Frame(self.root, bg="#1a0f3e")
        main_frame.pack(fill="both", expand=True)
        
        # Canvas para el fondo degradado
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # ✅ Variables para almacenar las windows de los botones
        botones_windows = {}
        
        # ✅ Función para redibujar el degradado cuando cambia el tamaño
        def redibujar_degradado(event=None):
            # Obtener tamaño actual del canvas
            ancho = canvas.winfo_width()
            alto = canvas.winfo_height()
            
            # Limpiar solo las líneas del degradado y textos, NO los botones
            canvas.delete("degradado")
            canvas.delete("titulo")
            canvas.delete("subtitulo")
            
            # Crear degradado ajustado
            for i in range(max(1, alto)):
                r = int(26 + (75-26) * i/max(1, alto))
                g = int(15 + (0-15) * i/max(1, alto))
                b = int(62 + (130-62) * i/max(1, alto))
                color = f'#{r:02x}{g:02x}{b:02x}'
                canvas.create_line(0, i, ancho, i, fill=color, tags="degradado")
            
            # ✅ Bajar el degradado al fondo
            canvas.tag_lower("degradado")
            
            # ✅ Calcular posiciones relativas al centro
            centro_x = ancho / 2
            
            # Título principal (25% desde arriba)
            canvas.create_text(centro_x, alto * 0.25, text="🐴 SMART HORSES 🐴",
                              font=("Consolas", 39, "bold"), 
                              fill="white", tags="titulo")
            
            canvas.create_text(centro_x, alto * 0.39, text="Selecciona Dificultad",
                              font=("Consolas", 24, "bold"), 
                              fill="white", tags="subtitulo")
            
            # ✅ Reposicionar botones solo si ya existen
            if botones_windows:
                y_botones = alto * 0.66
                separacion = ancho * 0.29
                canvas.coords(botones_windows['principiante'], centro_x - separacion, y_botones)
                canvas.coords(botones_windows['amateur'], centro_x, y_botones)
                canvas.coords(botones_windows['experto'], centro_x + separacion, y_botones)
        
        # ✅ Función para crear los botones DESPUÉS de que el canvas tenga tamaño
        def crear_botones():
            ancho = canvas.winfo_width()
            alto = canvas.winfo_height()
            centro_x = ancho / 2
            y_botones = alto * 0.58
            separacion = ancho * 0.11
            
            # BOTÓN PRINCIPIANTE (Verde)
            btn_principiante = tk.Frame(canvas, bg="#22c55e", 
                                        highlightbackground="#16a34a", 
                                        highlightthickness=3,
                                        )
            
            btn_p = tk.Button(btn_principiante, 
                             text="🎯",
                             font=("Consolas", 48),
                             bg="#22c55e", 
                             fg="white",
                             activebackground="#16a34a",
                             relief="flat",
                             bd=0,
                             width=6, height=1,
                             command=lambda: self.iniciar_juego(2))
            btn_p.pack(pady=(10, 5))
            
            tk.Label(btn_principiante, text="PRINCIPIANTE",
                    font=("Consolas", 18, "bold"),
                    bg="#22c55e", fg="white").pack(pady=(0, 0))
            
            tk.Label(btn_principiante, text="Profundidad: 2",
                    font=("Consolas", 11),
                    bg="#22c55e", fg="white").pack(pady=(5, 0))
            
            tk.Label(btn_principiante, text="Ideal para aprender",
                    font=("Consolas", 9, "italic"),
                    bg="#22c55e", fg="white").pack(pady=(2, 10))
            
            botones_windows['principiante'] = canvas.create_window(
                centro_x - separacion, y_botones, anchor="center", window=btn_principiante)
            
            # BOTÓN AMATEUR (Amarillo)
            btn_amateur = tk.Frame(canvas, bg="#eab308",
                                  highlightbackground="#ca8a04",
                                  highlightthickness=3)
            
            btn_a = tk.Button(btn_amateur,
                             text="⚡",
                             font=("Consolas", 48),
                             bg="#eab308",
                             fg="white",
                             activebackground="#ca8a04",
                             relief="flat",
                             bd=0,
                             width=6, height=1,
                             command=lambda: self.iniciar_juego(4))
            btn_a.pack(pady=(10, 5))
            
            tk.Label(btn_amateur, text="AMATEUR",
                    font=("Consolas", 18, "bold"),
                    bg="#eab308", fg="white").pack()
            
            tk.Label(btn_amateur, text="Profundidad: 4",
                    font=("Consolas", 11),
                    bg="#eab308", fg="white").pack(pady=(5, 0))
            
            tk.Label(btn_amateur, text="Desafío medio",
                    font=("Consolas", 9, "italic"),
                    bg="#eab308", fg="white").pack(pady=(2, 10))
            
            botones_windows['amateur'] = canvas.create_window(
                centro_x, y_botones, anchor="center", window=btn_amateur)
            
            # BOTÓN EXPERTO (Rojo)
            btn_experto = tk.Frame(canvas, bg="#ef4444",
                                  highlightbackground="#dc2626",
                                  highlightthickness=3)
            
            btn_e = tk.Button(btn_experto,
                             text="⚔️",
                             font=("Consolas", 48),
                             bg="#ef4444",
                             fg="white",
                             activebackground="#dc2626",
                             relief="flat",
                             bd=0,
                             width=6, height=1,
                             command=lambda: self.iniciar_juego(6))
            btn_e.pack(pady=(10, 5))
            
            tk.Label(btn_experto, text="EXPERTO",
                    font=("Consolas", 18, "bold"),
                    bg="#ef4444", fg="white").pack()
            
            tk.Label(btn_experto, text="Profundidad: 6",
                    font=("Consolas", 11),
                    bg="#ef4444", fg="white").pack(pady=(5, 0))
            
            tk.Label(btn_experto, text="Máximo desafío",
                    font=("Consolas", 9, "italic"),
                    bg="#ef4444", fg="white").pack(pady=(2, 10))
            
            botones_windows['experto'] = canvas.create_window(
                centro_x + separacion, y_botones, anchor="center", window=btn_experto)
            
            # Efectos hover
            def on_enter(event, frame, color_hover):
                frame.config(bg=color_hover)
                for child in frame.winfo_children():
                    if isinstance(child, (tk.Label, tk.Button)):
                        child.config(bg=color_hover)
            
            def on_leave(event, frame, color_normal):
                frame.config(bg=color_normal)
                for child in frame.winfo_children():
                    if isinstance(child, (tk.Label, tk.Button)):
                        child.config(bg=color_normal)
            
            btn_principiante.bind("<Enter>", lambda e: on_enter(e, btn_principiante, "#16a34a"))
            btn_principiante.bind("<Leave>", lambda e: on_leave(e, btn_principiante, "#22c55e"))
            btn_p.bind("<Enter>", lambda e: on_enter(e, btn_principiante, "#16a34a"))
            btn_p.bind("<Leave>", lambda e: on_leave(e, btn_principiante, "#22c55e"))
            
            btn_amateur.bind("<Enter>", lambda e: on_enter(e, btn_amateur, "#ca8a04"))
            btn_amateur.bind("<Leave>", lambda e: on_leave(e, btn_amateur, "#eab308"))
            btn_a.bind("<Enter>", lambda e: on_enter(e, btn_amateur, "#ca8a04"))
            btn_a.bind("<Leave>", lambda e: on_leave(e, btn_amateur, "#eab308"))
            
            btn_experto.bind("<Enter>", lambda e: on_enter(e, btn_experto, "#dc2626"))
            btn_experto.bind("<Leave>", lambda e: on_leave(e, btn_experto, "#ef4444"))
            btn_e.bind("<Enter>", lambda e: on_enter(e, btn_experto, "#dc2626"))
            btn_e.bind("<Leave>", lambda e: on_leave(e, btn_experto, "#ef4444"))
            musica_frame = tk.Frame(canvas, bg="#1a0f3e")

            # BOTÓN DE MÚSICA (esquina superior derecha)
            if self.musica_cargada and pygame.mixer.music.get_busy():
                texto_musica = "🎵 ON"
            else:
                texto_musica = "🎵 OFF"
            
            self.btn_musica = tk.Button(musica_frame,
                                    text=texto_musica,
                                    font=("Consolas", 12, "bold"),
                                    bg="#4a5568",
                                    fg="white",
                                    activebackground="#6b7280",
                                    relief="flat",
                                    bd=0,
                                    padx=15,
                                    pady=8,
                                    command=self.toggle_musica_btn)
            self.btn_musica.pack()
            
            # Redibujar el degradado después de crear los botones
            redibujar_degradado()
        
        # ✅ Vincular el evento de redimensionamiento
        canvas.bind("<Configure>", redibujar_degradado)
        
        # ✅ Esperar a que el canvas se renderice y luego crear botones
        canvas.update_idletasks()
        canvas.after(100, crear_botones)  # Esperar 100ms para asegurar que el canvas tenga tamaño

    def toggle_musica_btn(self):
        """Alternar música desde botón"""
        if self.musica_activada:
            musica_activa = self.toggle_musica()
            self.btn_musica.config(text="🎵 ON" if musica_activa else "🎵 OFF")
    
        
    def iniciar_juego(self, profundidad):
        if not self.musica_cargada:
            self.cargar_y_reproducir_musica()
    
        self.heuristica = profundidad
        self.minmax = algoritmoMinMax(profundidad)
        self.tablero = tableroObj()
        self.jugador = self.tablero.setCaballo(es_maquina=False)
        self.maquina = self.tablero.setCaballo(es_maquina=True)
        self.turno = 0
        self.crear_interfaz_juego()
        self.lbl_mensaje.config(text="Maquina pensando primer movimiento...")
        self.root.after(2100, self.turno_maquina)

    def crear_interfaz_juego(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
        # ✅ Frame principal con fondo degradado
        main_frame = tk.Frame(self.root, bg="#1e293b")
        main_frame.pack(fill="both", expand=True)
        
        # Canvas para degradado de fondo
        canvas = tk.Canvas(main_frame, highlightthickness=0, bg="#1e293b")
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        # ✅ Frame scrollable con ANCHO FIJO (para evitar que se expanda)
        scrollable_frame = tk.Frame(canvas, bg="#1e293b")
        content_box = tk.Frame(scrollable_frame, bg="#2d3748", 
                        highlightbackground="#4a5568",
                        highlightthickness=2,
                        padx=40, pady=20)
        content_box.pack(padx=40, pady=20)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # ✅ Crear window CENTRADO HORIZONTALMENTE pero arriba verticalmente
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # ✅ Función para centrar SOLO horizontalmente
        def centrar_horizontal(event=None):
            canvas_width = event.width if event else canvas.winfo_width()
            # y=0 para que empiece arriba y pueda hacer scroll
            canvas.coords(canvas_window, (canvas_width // 2, 0))
        canvas.bind("<Configure>", centrar_horizontal)
        
    
        # ✅ Empaquetar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ✅ Scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # ✅ HEADER
        header = tk.Frame(scrollable_frame, bg="#1e293b")
        header.pack(pady=(0, 0))
        
        tk.Label(header, text="SMART HORSES",
                font=("Consolas", 32, "bold"),
                bg="#1e293b", fg="white").pack()
        
        
        dificultad_texto = {2: "PRINCIPIANTE", 4: "AMATEUR", 6: "EXPERTO"}
        profundidad = self.minmax.profundidad
        
        tk.Label(header, text=f"Dificultad: {dificultad_texto.get(profundidad, 'DESCONOCIDA')}",
                font=("Consolas", 16),
                bg="#1e293b", fg="#fbbf24").pack()

        
        marcadores_frame = tk.Frame(scrollable_frame, bg="#1e293b")
        marcadores_frame.pack(pady=10)
        
        # Marcador JUGADOR (Azul)
        jugador_frame = tk.Frame(marcadores_frame, bg="#2563eb",
                                highlightbackground="#fbbf24",
                                highlightthickness=0)
        jugador_frame.grid(row=0, column=0, padx=20, sticky="ew")
        
        jugador_inner = tk.Frame(jugador_frame, bg="#2563eb",  width=335, height=70)
        jugador_inner.pack(padx=15, pady=5)
        jugador_inner.pack_propagate(False)  
        
        tk.Label(jugador_inner, text="TÚ",
                font=("Consolas", 10),
                bg="#2563eb", fg="#bfdbfe").pack(anchor="w", padx=16, pady=(5, 0))
        
        self.lbl_jugador = tk.Label(jugador_inner, text=str(self.jugador.puntaje),
                                   font=("Consolas", 24, "bold"),
                                   bg="#2563eb", fg="white")
        self.lbl_jugador.pack(anchor="w", padx=8, pady=(0, 5))
        
        # Marcador MÁQUINA (Gris)
        maquina_frame = tk.Frame(marcadores_frame, bg="#4b5563",
                        highlightbackground="#fbbf24",
                        highlightthickness=0)
        maquina_frame.grid(row=0, column=1, padx=20, sticky="ew")

        maquina_inner = tk.Frame(maquina_frame, bg="#4b5563", width=334, height=70)
        maquina_inner.pack(padx=19, pady=5)
        maquina_inner.pack_propagate(False)  # ✅ IMPORTANTE: mantener después de pack()

        tk.Label(maquina_inner, text="MÁQUINA",
                font=("Consolas", 10),
                bg="#4b5563", fg="#d1d5db").pack(anchor="w", padx=4, pady=(5, 0))

        self.lbl_maquina = tk.Label(maquina_inner, text=str(self.maquina.puntaje),
                                font=("Consolas", 24, "bold"),
                                bg="#4b5563", fg="white")
        self.lbl_maquina.pack(anchor="w", padx=8, pady=(0, 5))


        # Guardar referencias para resaltar turno actual
        self.jugador_frame = jugador_frame
        self.maquina_frame = maquina_frame
        
        # ✅ CONTENEDOR PARA TABLERO Y LEYENDA (lado a lado)
        tablero_y_leyenda = tk.Frame(scrollable_frame, bg="#1e293b")
        tablero_y_leyenda.pack(pady=10)
        
        # ✅ TABLERO (columna izquierda)
        tablero_frame = tk.Frame(tablero_y_leyenda, bg="#1e293b")
        tablero_frame.grid(row=0, column=0, padx=15)
        
        tablero_outer = tk.Frame(tablero_frame, bg="#92400e", padx=15, pady=15)
        tablero_outer.pack()
        
        tablero_container = tk.Frame(tablero_outer, bg="#111827", padx=8, pady=8)
        tablero_container.pack()
        
        self.botones_tablero = []
        for i in range(8):
            fila = []
            for j in range(8):
                color = "#f5f5f5" if (i + j) % 2 == 0 else "#d4d4d4"
                
                btn = tk.Button(tablero_container,
                               width=5, height=2,
                               bg=color,
                               activebackground=color,
                               font=("Consolas", 11, "bold"),
                               relief="flat",
                               bd=0,
                               compound="center",
                               command=lambda x=i, y=j: self.click_casilla(x, y))
                btn.grid(row=i, column=j, padx=1, pady=1)
                fila.append(btn)
            self.botones_tablero.append(fila)
        
        columna_derecha = tk.Frame(tablero_y_leyenda, bg="#1e293b")
        columna_derecha.grid(row=0, column=1, padx=16, sticky="n")

        mensaje_frame = tk.Frame(columna_derecha, bg="#1e293b")
        mensaje_frame.pack(pady=(25, 0))
    
        self.lbl_mensaje = tk.Label(mensaje_frame,
                                text="",
                                font=("Consolas", 12, "bold"),
                                bg="#fbbf24", fg="#1e293b",
                                padx=15, pady=10,
                                width=22,        
                                height=2,        
                                wraplength=250,  
                                justify="center",
                                anchor="center") 
        self.lbl_mensaje.pack()
        
        # ✅ LEYENDA (arriba)
        leyenda_frame = tk.Frame(columna_derecha, bg="#1e293b")
        leyenda_frame.pack()
        
        leyenda_inner = tk.Frame(leyenda_frame, bg="white", relief="flat")
        leyenda_inner.pack(padx=12, pady=30)
        
        # Título de leyenda
        tk.Label(leyenda_inner, text="LEYENDA",
                font=("Consolas", 14, "bold"),
                bg="white", fg="#1e293b").grid(row=0, column=0, columnspan=2, pady=(21, 1))
        
        # Items de leyenda (ahora en vertical)
        items_leyenda = [
            ("♞", "Tu caballo (Negro)", 1),
            ("♘", "Máquina (Blanco)", 2),
            ("+", "Puntos positivos", 3, "#22c55e"),
            ("-", "Puntos negativos", 4, "#ef4444"),
        ]
        
        for item in items_leyenda:
            if len(item) == 3:
                icono, texto, row = item
                color_bg = "#1e293b"
            else:
                icono, texto, row, color_bg = item
            
            item_frame = tk.Frame(leyenda_inner, bg="#ffffff")
            item_frame.grid(row=row, column=0, padx=19, pady=8, sticky="w")
            
            if icono in ["+", "-"]:
                icono_label = tk.Label(item_frame,
                                      text=icono,
                                      font=("Consolas", 12, "bold"),
                                      bg=color_bg, fg="white",
                                      width=2, height=1)
            else:
                icono_label = tk.Label(item_frame,
                                      text=icono,
                                      font=("Consolas", 20),
                                      bg="#ffffff", fg="#1e293b")
            
            icono_label.pack(side="left", padx=(0, 10))
            
            tk.Label(item_frame, text=texto,
                    font=("Consolas", 11),
                    bg="#ffffff", fg="#1e293b").pack(side="left")
        
        # Espaciado final en leyenda
        tk.Label(leyenda_inner, text="",
                bg="white", height=1).grid(row=5, column=0, pady=5)
        
        
        boton_volver_frame = tk.Frame(columna_derecha, bg="#1e293b")
        boton_volver_frame.pack(fill="x", pady=(3, 15))
        
        tk.Button(boton_volver_frame, text="← VOLVER AL MENÚ",
                font=("Consolas", 13, "bold"),
                bg="#f59e0b", fg="white",
                activebackground="#d97706",
                relief="flat",
                padx=15, pady=8,
                command=self.crear_pantalla_inicio).pack()
        
        # ✅ CONTROLES DE MÚSICA
        musica_controls_frame = tk.Frame(columna_derecha, bg="#1e293b")
        musica_controls_frame.pack(fill="x", pady=(9, 5))
        
        # Botón ON/OFF
        self.btn_musica_juego = tk.Button(musica_controls_frame,
                                    text="🎵 ON" if pygame.mixer.music.get_busy() else "🎵 OFF",
                                    font=("Consolas", 12, "bold"),  # Aumentado de 10 a 12
                                    bg="#4a5568",
                                    fg="white",
                                    activebackground="#6b7280",
                                    relief="flat",
                                    bd=0,
                                    padx=20,  # Aumentado de 10 a 20
                                    pady=8,   # Aumentado de 5 a 8
                                    cursor="hand2",
                                    command=self.toggle_musica_juego)
        self.btn_musica_juego.pack()
        
        # Inicializar tablero y centrar
        self.actualizar_tablero()
        self.actualizar_info()

    def toggle_musica_juego(self):
        """Alternar música desde interfaz del juego"""
        if not self.musica_cargada:
            return
        if self.musica_activada:
            musica_activa = self.toggle_musica()
            self.btn_musica_juego.config(text="🎵 ON" if musica_activa else "🎵 OFF")

    def __del__(self):
        """Limpiar pygame al cerrar la aplicación"""
        if hasattr(self, 'musica_activada') and self.musica_activada:
            pygame.mixer.quit()

    
    def resaltar_turno_actual(self, es_jugador=True):
        """Resalta el marcador del jugador actual"""
        if es_jugador:
            self.jugador_frame.config(highlightthickness=4)
            self.maquina_frame.config(highlightthickness=0)
        else:
            self.jugador_frame.config(highlightthickness=0)
            self.maquina_frame.config(highlightthickness=4)
    
    
    def ejecutar_movimiento_jugador(self, movimiento):
        nueva_x, nueva_y = self.jugador.calcularNuevaPosicion(movimiento)
        
        self.tablero.moverCaballo(self.jugador, movimiento)
        
        # Mensaje detallado
        mensaje = f"Jugador movió a la posición ({nueva_x}, {nueva_y})"
        
        self.lbl_mensaje.config(text=mensaje)
        self.actualizar_info()
        self.actualizar_tablero()
            
        self.root.after(2100, self.turno_maquina)
    
    def actualizar_tablero(self):
        for i in range(8):
            for j in range(8):
                casilla = self.tablero.tablero[i][j]
                btn = self.botones_tablero[i][j]
                
                color = "#eeeeee" if (i + j) % 2 == 0 else "#bbbbbb"

                btn.config(
                    bg=color, 
                    activebackground=color, 
                    image="", 
                    text="", 
                    compound="center",
                    width=5,   
                    height=2   
                )

                if casilla == 0:
                    if self.jugador.posX == i and self.jugador.posY == j:
                        # ✅ Jugador = ♞ (Negro)
                        btn.config(text="♞", fg="#000000", font=("Consolas", 15, "bold"))
                    elif self.maquina.posX == i and self.maquina.posY == j:
                        # ✅ Máquina = ♘ (Blanco)
                        btn.config(text="♘", fg="#000000", font=("Consolas", 15, "bold"))
                elif casilla == "X":
                    btn.config(bg="#050505", activebackground="#050505", text="")
                elif casilla is None:
                    btn.config(text="", fg="#666", font=("Consolas", 15))
                elif isinstance(casilla, int):
                    color_texto = "#4CAF50" if casilla > 0 else "#F44336"
                    texto = f"+{casilla}" if casilla > 0 else str(casilla)
                    btn.config(text=texto, fg=color_texto, font=("Consolas", 15, "bold"))

    def click_casilla(self, x, y):
        if (x, y) in self.movimientos_validos_pos:
            movimiento = self.movimientos_validos_pos[(x, y)]
            self.ejecutar_movimiento_jugador(movimiento)

    def resaltar_movimientos_validos(self):
        self.movimientos_validos_pos = {}
        self.tablero.calcularMovimientosValidosCaballo(self.jugador)
        
        for mov in self.jugador.movimientosPosibles:
            nx, ny = self.jugador.calcularNuevaPosicion(mov)
            self.movimientos_validos_pos[(nx, ny)] = mov
            btn = self.botones_tablero[nx][ny]
            btn.config(bg="#90EE90", activebackground="#7CFC00")


    def turno_maquina(self):
        self.turno += 1

        self.tablero.calcularMovimientosValidosCaballo(self.maquina)

        if len(self.maquina.movimientosPosibles):
            movimiento = self.minmax.mejorMovimiento(self.tablero, self.maquina, self.jugador)
            
            # Obtener información antes de mover
            nueva_x, nueva_y = self.maquina.calcularNuevaPosicion(movimiento)
            
            self.tablero.moverCaballo(self.maquina, movimiento)
            
            # Mensaje mejorado
            mensaje = f"Máquina movió a la posición ({nueva_x}, {nueva_y})"
            
            self.lbl_mensaje.config(text=mensaje)
        else:
            self.maquina.changePuntaje(-4)
            self.lbl_mensaje.config(text="Máquina sin movimientos    Ahora es tu turno")

        self.actualizar_info()
        self.actualizar_tablero()

        if self.verificar_fin_juego():
            return
        self.tablero.calcularMovimientosValidosCaballo(self.jugador)
    
        # Si el jugador tiene movimientos, resaltarlos
        if len(self.jugador.movimientosPosibles) > 0:
            self.resaltar_movimientos_validos()

            self.lbl_mensaje.config(text="Es tu turno, selecciona una casilla verde")
        else:
            # Si no tiene movimientos, aplicar penalización y pasar turno
            self.jugador.changePuntaje(-4)
            self.lbl_mensaje.config(text="No tienes movimientos    La máquina juega")
            self.actualizar_info()
            
            # Verificar si el juego terminó después de la penalización
            if self.verificar_fin_juego():
                return
            
            # La máquina juega de nuevo
            self.root.after(2100, self.turno_maquina)

    def actualizar_info(self):
        self.lbl_jugador.config(text=f"♞  Jugador    {self.jugador.puntaje}")
        self.lbl_maquina.config(text=f"♘  Máquina    {self.maquina.puntaje}")

    def verificar_fin_juego(self):
        self.tablero.calcularMovimientosValidosCaballo(self.jugador)
        self.tablero.calcularMovimientosValidosCaballo(self.maquina)
    
        if (len(self.jugador.movimientosPosibles) == 0 and 
            len(self.maquina.movimientosPosibles) == 0):
    
            self.mostrar_pantalla_game_over()
            return True
    
        return False
    
    def mostrar_pantalla_game_over(self):
        """Pantalla de fin de juego inspirada en el diseño React con scroll"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Determinar ganador
        player_won = self.jugador.puntaje > self.maquina.puntaje
        tie = self.jugador.puntaje == self.maquina.puntaje
        
        if player_won:
            mensaje = "🎉 ¡GANASTE! 🎉"
            color_icono = "#fbbf24"  # Amarillo dorado
        elif tie:
            mensaje = "⚖️ EMPATE"
            color_icono = "#9ca3af"  # Gris
        else:
            mensaje = "💻 LA MÁQUINA GANÓ"
            color_icono = "#9ca3af"  # Gris
        
        main_frame = tk.Frame(self.root, bg="#1a0f3e")
        main_frame.pack(fill="both", expand=True)

        # ✅ Contenedor central (centrado vertical y horizontalmente)
        center_frame = tk.Frame(main_frame, bg="#1a0f3e")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        
        # ✅ TÍTULO
        tk.Label(center_frame,
                text=mensaje,
                font=("Consolas", 36, "bold"),  # Reducido de 48 a 36
                bg="#1a0f3e",
                fg="white").pack(pady=10)
        
        # ✅ CONTENEDOR DE RESULTADOS
        resultado_frame = tk.Frame(center_frame,
                                  bg="#2d3748",
                                  highlightbackground="#4a5568",
                                  highlightthickness=2)
        resultado_frame.pack(pady=20, padx=30)
        
        # Título de resultados
        tk.Label(resultado_frame,
                text="RESULTADO FINAL",
                font=("Consolas", 22, "bold"),  # Reducido de 28 a 22
                bg="#2d3748",
                fg="#fbbf24").pack(pady=(20, 15))
        
        # ✅ Grid de puntajes
        puntajes_container = tk.Frame(resultado_frame, bg="#2d3748")
        puntajes_container.pack(pady=15, padx=30)
        
        # ✅ PUNTAJE JUGADOR
        jugador_bg = "#22c55e" if player_won else "#2563eb"
        jugador_frame_score = tk.Frame(puntajes_container,
                                      bg=jugador_bg,
                                      highlightbackground=jugador_bg,
                                      highlightthickness=2,
                                      width=180,  # Reducido de 200 a 180
                                      height=120)  # Reducido de 150 a 120
        jugador_frame_score.grid(row=0, column=0, padx=15, pady=10)
        jugador_frame_score.pack_propagate(False)
        
        tk.Label(jugador_frame_score,
                text="TÚ",
                font=("Consolas", 16),  # Reducido de 18 a 16
                bg=jugador_bg,
                fg="white").pack(pady=(15, 5))
        
        tk.Label(jugador_frame_score,
                text=str(self.jugador.puntaje),
                font=("Consolas", 42, "bold"),  # Reducido de 56 a 42
                bg=jugador_bg,
                fg="white").pack(pady=5)
        
        # ✅ PUNTAJE MÁQUINA
        maquina_bg = "#4b5563" if not player_won and not tie else "#6b7280"
        maquina_frame_score = tk.Frame(puntajes_container,
                                      bg=maquina_bg,
                                      highlightbackground=maquina_bg,
                                      highlightthickness=2,
                                      width=180,  # Reducido de 200 a 180
                                      height=120)  # Reducido de 150 a 120
        maquina_frame_score.grid(row=0, column=1, padx=15, pady=10)
        maquina_frame_score.pack_propagate(False)
        
        tk.Label(maquina_frame_score,
                text="MÁQUINA",
                font=("Consolas", 16),  # Reducido de 18 a 16
                bg=maquina_bg,
                fg="white").pack(pady=(15, 5))
        
        tk.Label(maquina_frame_score,
                text=str(self.maquina.puntaje),
                font=("Consolas", 42, "bold"),  # Reducido de 56 a 42
                bg=maquina_bg,
                fg="white").pack(pady=5)
        
        # ✅ Información de turnos
        tk.Label(resultado_frame,
                text=f"Turnos jugados: {self.turno}",
                font=("Consolas", 14),  # Reducido de 16 a 14
                bg="#2d3748",
                fg="white").pack(pady=(15, 20))
        
        # ✅ BOTONES DE ACCIÓN
        botones_frame = tk.Frame(center_frame, bg="#1a0f3e")
        botones_frame.pack(pady=25)
        
        # Botón JUGAR DE NUEVO
        btn_jugar = tk.Button(botones_frame,
                             text="🔄 JUGAR DE NUEVO",
                             font=("Consolas", 14, "bold"),  # Reducido de 16 a 14
                             bg="#22c55e",
                             fg="white",
                             activebackground="#16a34a",
                             activeforeground="white",
                             relief="flat",
                             bd=0,
                             padx=25,  # Reducido de 30 a 25
                             pady=12,  # Reducido de 15 a 12
                             cursor="hand2",
                             command=lambda: self.iniciar_juego(self.heuristica))
        btn_jugar.grid(row=0, column=0, padx=12)
        
        # Efecto hover botón jugar
        def on_enter_jugar(e):
            btn_jugar.config(bg="#16a34a")
        
        def on_leave_jugar(e):
            btn_jugar.config(bg="#22c55e")
        
        btn_jugar.bind("<Enter>", on_enter_jugar)
        btn_jugar.bind("<Leave>", on_leave_jugar)
        
        # Botón MENÚ PRINCIPAL
        btn_menu = tk.Button(botones_frame,
                            text="🏠 MENÚ PRINCIPAL",
                            font=("Consolas", 14, "bold"),  # Reducido de 16 a 14
                            bg="#4a5568",
                            fg="white",
                            activebackground="#6b7280",
                            activeforeground="white",
                            relief="flat",
                            bd=0,
                            padx=25,  # Reducido de 30 a 25
                            pady=12,  # Reducido de 15 a 12
                            cursor="hand2",
                            command=self.crear_pantalla_inicio)
        btn_menu.grid(row=0, column=1, padx=12)
        
        # Efecto hover botón menú
        def on_enter_menu(e):
            btn_menu.config(bg="#6b7280")
        
        def on_leave_menu(e):
            btn_menu.config(bg="#4a5568")
        
        btn_menu.bind("<Enter>", on_enter_menu)
        btn_menu.bind("<Leave>", on_leave_menu)
    
    def _resultado_final(self):
        """Método legacy - ya no se usa con la nueva pantalla"""
        if self.jugador.puntaje > self.maquina.puntaje:
            estado = "🎉 ¡GANASTE! 🎉"
        elif self.maquina.puntaje > self.jugador.puntaje:
            estado = "💻 LA MÁQUINA GANÓ"
        else:
            estado = "⚖️ EMPATE"
    
        return (f"{estado}\n\n"
                f"Jugador:  {self.jugador.puntaje}\n"
                f"Máquina:  {self.maquina.puntaje}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoGUI(root)
    root.mainloop()