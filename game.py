import random

def getRandomPos():
    return [random.randint(0,9),random.randint(0,9)]
        
class caballoObj:
    posX: int = None
    posY: int = None
    puntaje: int = 0
    movimientos = ["UL","UR","RU","RD","DL","DR","LU", "LD"]
    movimientosPosibles = []

    def __init__(self, pos: list):
        self.posX = pos[0]
        self.posY = pos[1]
        
    def changePuntaje(self, puntos:int):
        self.puntaje = self.puntaje + puntos

    def moverCaballo(self, movimiento: str):

        if movimiento == "UL":
            self.posX = self.posX - 2
            self.posY = self.posY - 1

        elif movimiento == "UR":
            self.posX = self.posX - 2
            self.posY = self.posY + 1

        elif movimiento == "RU":
            self.posX = self.posX - 1
            self.posY = self.posY + 2

        elif movimiento == "RD":
            self.posX = self.posX + 1
            self.posY = self.posY + 2
        
        elif movimiento == "DL":
            self.posX = self.posX + 2
            self.posY = self.posY - 1

        elif movimiento == "DR":
            self.posX = self.posX + 2
            self.posY = self.posY + 1

        elif movimiento == "LU":
            self.posX = self.posX - 1
            self.posY = self.posY - 2

        elif movimiento == "LD":
            self.posX = self.posX + 1
            self.posY = self.posY - 2
        
        else:
            "Movimientos no valido"

    def calcularNuevaPosicion(self, movimiento):

        movimientos_dict = {
            'UL': (-2, -1), 'UR': (-2, 1),
            'RU': (-1, 2), 'RD': (1, 2),
            'DR': (2, 1), 'DL': (2, -1),
            'LD': (1, -2), 'LU': (-1, -2)
        }
        
        dx, dy = movimientos_dict[movimiento]
        return self.posX + dx, self.posY + dy
    
    def clonar(self):
        nuevo = caballoObj([self.posX, self.posY])
        nuevo.puntaje = self.puntaje
        return nuevo

    def printPuntaje(self):
        print("El puntaje del caballo es:" + str(self.puntaje))

class tableroObj:

    def __init__(self):
        # Generar tablero aleatorio automáticamente
        self.tablero = [[None for _ in range(8)] for _ in range(8)]
        self.puntos_restantes = 10
        puntajes = [-10, -5, -4, -3, -1, 1, 3, 4, 5, 10]
        
        posiciones_usadas = set()
        
        # Colocar puntos aleatoriamente
        for puntaje in puntajes:
            while True:
                x, y = random.randint(0, 7), random.randint(0, 7)
                if (x, y) not in posiciones_usadas:
                    self.tablero[x][y] = puntaje
                    posiciones_usadas.add((x, y))
                    break
        
        # Guardar posiciones usadas para los caballos
        self.posiciones_usadas = posiciones_usadas


    def setCaballo(self, es_maquina=False):
        """Coloca un caballo en posición aleatoria disponible"""
        while True:
            x, y = random.randint(0, 7), random.randint(0, 7)
            if (x, y) not in self.posiciones_usadas:
                caballo = caballoObj([x, y])
                self.tablero[x][y] = 0
                self.posiciones_usadas.add((x, y))
                
                # Mostrar símbolo del caballo
                simbolo = "♞" if es_maquina else "♟"
                print(f"Caballo {'BLANCO (Máquina)' if es_maquina else 'NEGRO (Jugador)'} {simbolo} colocado en ({x}, {y})")
                return caballo
    
    def moverCaballo(self,caballo: caballoObj, movimiento: str):

            self.tablero[caballo.posX][caballo.posY] = "X"

            caballo.moverCaballo(movimiento)

            valorCasilla = self.tablero[caballo.posX][caballo.posY]

            if valorCasilla != None:
                caballo.changePuntaje(valorCasilla)
                self.puntos_restantes -= 1
            
            self.tablero[caballo.posX][caballo.posY] = 0

    def calcularMovimientosValidosCaballo(self, caballo: caballoObj):
        caballo.movimientosPosibles.clear()
        
        for movimiento in caballo.movimientos:
            nuevaX, nuevaY = caballo.calcularNuevaPosicion(movimiento)
            
            if 0 <= nuevaX < 8 and 0 <= nuevaY < 8:
                casilla = self.tablero[nuevaX][nuevaY]
                if (casilla is None or isinstance(casilla, int) and casilla!=0):
                    caballo.movimientosPosibles.append(movimiento)
            

    def clonar(self):
        nuevo = tableroObj.__new__(tableroObj) 
        nuevo.tablero = [fila.copy() for fila in self.tablero]
        nuevo.puntos_restantes = self.puntos_restantes
        return nuevo
        
    def printTablero(self):
        print("\nTABLERO:")
        print("-" * 50)
        for i, fila in enumerate(self.tablero):
            fila_formateada = []
            for j, x in enumerate(fila):
                if x == 0:
                    # Verificar qué caballo está aquí
                    fila_formateada.append("  ♞" if hasattr(self, '_es_maquina_pos') and (i,j) in self._es_maquina_pos else "  ♟")
                elif x is not None:
                    fila_formateada.append(f"{str(x):>3}")
                else:
                    fila_formateada.append("  .")
            print(" ".join(fila_formateada))
        print("-" * 50)
    
class algoritmoMinMax:
    profundidad: int = 0

    def __init__(self, profundidad: int):
        self.profundidad = profundidad

    # Heurística 

    def evaluar(self, tablero, maquina, jugador):
        puntaje_final = 0
        
        puntaje_final += maquina.puntaje * 2.0
        
        puntaje_final += (maquina.puntaje - jugador.puntaje) * 1.0
        
        tablero.calcularMovimientosValidosCaballo(maquina)
        movimientos_maquina = len(maquina.movimientosPosibles)
        tablero.calcularMovimientosValidosCaballo(jugador)
        movimientos_jugador = len(jugador.movimientosPosibles)
        
        puntaje_final += movimientos_maquina * 0.3
        puntaje_final -= movimientos_jugador * 0.2
        
        riesgo_maquina = self.calcular_riesgo(tablero, maquina)
        puntaje_final -= riesgo_maquina * 1.5
        
        return puntaje_final
    
    def calcular_riesgo(self, tablero, caballo):
        """Calcula cuánto riesgo hay de caer en casillas negativas"""
        riesgo = 0
        tablero.calcularMovimientosValidosCaballo(caballo)
        
        for movimiento in caballo.movimientosPosibles:
            nueva_x, nueva_y = caballo.calcularNuevaPosicion(movimiento)
            if 0 <= nueva_x < 8 and 0 <= nueva_y < 8:
                valor = tablero.tablero[nueva_x][nueva_y]
                if isinstance(valor, int) and valor < 0:
                    riesgo += abs(valor)  

        return riesgo

    # Minimax 

    def minimax(self, tablero, maquina, jugador, profundidad, esMax):
        
        # Caso base - usar la nueva heurística con acceso al tablero
        if profundidad == 0 or tablero.puntos_restantes == 0:
            return self.evaluar(tablero, maquina, jugador)

        # Turno MAX (la máquina)
        if esMax:
            mejorValor = float("-inf")

            tablero.calcularMovimientosValidosCaballo(maquina)
            movimientos = maquina.movimientosPosibles.copy()

            if len(movimientos) == 0:
                return self.evaluar(tablero, maquina, jugador) - 8

            for mov in movimientos:
                t2 = tablero.clonar()
                m2 = maquina.clonar()
                j2 = jugador.clonar()

                t2.moverCaballo(m2, mov)
                valor = self.minimax(t2, m2, j2, profundidad - 1, False)
                mejorValor = max(mejorValor, valor)

            return mejorValor

        # Turno MIN (el jugador)
        else:
            peorValor = float("inf")

            tablero.calcularMovimientosValidosCaballo(jugador)
            movimientos = jugador.movimientosPosibles.copy()

            if len(movimientos) == 0:
                return self.evaluar(tablero, maquina, jugador) + 8 

            for mov in movimientos:
                t2 = tablero.clonar()
                m2 = maquina.clonar()
                j2 = jugador.clonar()

                t2.moverCaballo(j2, mov)
                valor = self.minimax(t2, m2, j2, profundidad - 1, True)
                peorValor = min(peorValor, valor)

            return peorValor

    # Seleccionar el mejor movimiento de la máquina
    def mejorMovimiento(self, tablero, maquina, jugador):
        mejorMov = None
        mejorValor = float("-inf")

        tablero.calcularMovimientosValidosCaballo(maquina)
        
        if len(maquina.movimientosPosibles) == 0:
            return None

        movimientos_validos = maquina.movimientosPosibles.copy()
        
        print("\n=== ANÁLISIS DE MOVIMIENTOS ===")
        for mov in movimientos_validos:
            nueva_x, nueva_y = maquina.calcularNuevaPosicion(mov)
            valor_casilla = tablero.tablero[nueva_x][nueva_y] if 0 <= nueva_x < 8 and 0 <= nueva_y < 8 else "FUERA"
            print(f"Movimiento {mov}: posición ({nueva_x}, {nueva_y}) -> valor: {valor_casilla}")
        
        for mov in movimientos_validos:
            t2 = tablero.clonar()
            m2 = maquina.clonar()
            j2 = jugador.clonar()
            
            # Verificar el valor inmediato de este movimiento
            nueva_x, nueva_y = m2.calcularNuevaPosicion(mov)
            valor_inmediato = t2.tablero[nueva_x][nueva_y] if 0 <= nueva_x < 8 and 0 <= nueva_y < 8 else 0
            
            print(f"\nEvaluando movimiento: {mov} (valor inmediato: {valor_inmediato})")
            
            t2.moverCaballo(m2, mov)
            valor = self.minimax(t2, m2, j2, self.profundidad - 1, False)

            print(f"Valor heurístico total: {valor}")
            
            if valor > mejorValor:
                mejorValor = valor
                mejorMov = mov
                print(f"*** NUEVO MEJOR MOVIMIENTO: {mov} con valor {valor} ***")

        print(f"\n=== MOVIMIENTO ELEGIDO: {mejorMov} ===")
        return mejorMov
    
def generarMapaAleatorio():
    """Genera un mapa aleatorio con puntos distribuidos aleatoriamente"""
    mapa = [[0 for _ in range(8)] for _ in range(8)]  # Inicializar con casillas vacías (2)
    
    # Definir puntos a distribuir
    puntajes = [-10, -5, -4, -3, -1, 1, 3, 4, 5, 10]
    
    # Colocar puntos aleatoriamente
    posiciones_usadas = set()
    for puntaje in puntajes:
        while True:
            x, y = random.randint(0, 7), random.randint(0, 7)
            if (x, y) not in posiciones_usadas:
                mapa[x][y] = puntaje
                posiciones_usadas.add((x, y))
                break
    
    # Colocar caballos aleatoriamente
    while True:
        x, y = random.randint(0, 7), random.randint(0, 7)
        if (x, y) not in posiciones_usadas:
            mapa[x][y] = 11  # Jugador
            posiciones_usadas.add((x, y))
            break
    
    while True:
        x, y = random.randint(0, 7), random.randint(0, 7)
        if (x, y) not in posiciones_usadas:
            mapa[x][y] = 12  # Máquina
            posiciones_usadas.add((x, y))
            break
    
    return mapa
    
def game():
    minMax = None

    while True:
        userDificultyInput = input("Ingrese que dificultad de juego quiere jugar (principiante, amateur, experto): ")

        if userDificultyInput.lower() == "principiante":
            minMax = algoritmoMinMax(2)
            break
        elif userDificultyInput.lower() == "amateur":
            minMax = algoritmoMinMax(4)
            break
        elif userDificultyInput.lower() == "experto":
            minMax = algoritmoMinMax(6)
            break
        else:
            print("Entrada no valida intente de nuevo")

    print("\n=== GENERANDO TABLERO ALEATORIO ===")
    tablero = tableroObj()
    
    print("\nColocando caballos en posiciones aleatorias...")
    jugador = tablero.setCaballo(es_maquina=False)  # Caballo NEGRO
    maquina = tablero.setCaballo(es_maquina=True)   # Caballo BLANCO

    tablero.printTablero()
    
    turno = 0
    max_turnos = 50
   
    while True:
        turno += 1
        print(f"\n=== TURNO {turno} ===")
        
        if turno >= max_turnos:
            print("\n--- JUEGO TERMINADO ---")
            print("Se alcanzó el límite máximo de turnos")
            break
        
        # TURNO DEL JUGADOR
        tablero.calcularMovimientosValidosCaballo(jugador)
        movimientos_jugador = len(jugador.movimientosPosibles)

        if movimientos_jugador > 0:
            while True:
                print("Tus movimientos posibles:", jugador.movimientosPosibles)
                userMoveInput = input("Ingrese el movimiento que desea ejecutar: ")
                if userMoveInput in jugador.movimientosPosibles: 
                    tablero.moverCaballo(jugador, userMoveInput)
                    break
                print("Movimiento no valido\n")
        else: 
            jugador.changePuntaje(-4)
            print("El jugador no tiene movimientos posibles")
        
        tablero.printTablero()
        print("Puntaje jugador:", jugador.puntaje)

        # TURNO DE LA MÁQUINA
        tablero.calcularMovimientosValidosCaballo(maquina)
        movimientos_maquina = len(maquina.movimientosPosibles)
        
        print("Movimientos posibles máquina:", maquina.movimientosPosibles)

        if movimientos_maquina > 0:
            movMaquina = minMax.mejorMovimiento(tablero, maquina, jugador)
            print("La máquina eligió:", movMaquina)
            tablero.moverCaballo(maquina, movMaquina)
            print("Puntaje máquina:", maquina.puntaje)
        else:
            maquina.changePuntaje(-4)
            print("La máquina no tiene movimientos posibles")

        tablero.printTablero()
        print("Puntaje jugador:", jugador.puntaje)

        # VERIFICAR CONDICIÓN DE FINAL DEL JUEGO
        tablero.calcularMovimientosValidosCaballo(jugador)
        tablero.calcularMovimientosValidosCaballo(maquina)
        
        movimientos_jugador_final = len(jugador.movimientosPosibles)
        movimientos_maquina_final = len(maquina.movimientosPosibles)
        
        if movimientos_jugador_final == 0 and movimientos_maquina_final == 0:
            print("\n--- JUEGO TERMINADO ---")
            print("Ambos jugadores se quedaron sin movimientos posibles")
            break
        
        if tablero.puntos_restantes <= 0:
            print("\n--- JUEGO TERMINADO ---")
            print("No quedan más puntos por recolectar en el tablero")
            break

    # MOSTRAR RESULTADO FINAL
    print("\n" + "="*50)
    print("RESULTADO FINAL")
    print("="*50)
    print(f"Puntaje JUGADOR: {jugador.puntaje}")
    print(f"Puntaje MÁQUINA: {maquina.puntaje}")
    
    if jugador.puntaje > maquina.puntaje:
        print("🎉 ¡FELICIDADES! GANASTE EL JUEGO 🎉")
    elif maquina.puntaje > jugador.puntaje:
        print("💻 La máquina ganó el juego")
    else:
        print("⚖️ El juego terminó en empate")
    
    print(f"Total de turnos jugados: {turno}")
    print("="*50)

