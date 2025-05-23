import random
import os
import time

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def _repr(self, level=0):
        result = "  " * level + f"{self.value}\n"
        for child in self.children:
            result += child._repr(level + 1)
        return result

    def __repr__(self):
        return self._repr()

class GeneralTree:
    def __init__(self, root: Node = None):
        self.root = root

    def insert(self, parent, child, current_node=None):
        if current_node is None:
            current_node = self.root

        if self.root is None:
            parent = Node(parent)
            child = Node(child)
            parent.children.append(child)
            self.root = parent
            return True
        
        if current_node.value == parent:
            current_node.children.append(Node(child))
            return True

        for i in current_node.children:
            if self.insert(parent, child, i):
                return True
        return False

    def buscar(self, value, current_node=None):
        if current_node is None:
            current_node = self.root

        if value == current_node.value:
            return True
        
        for i in current_node.children:
            if self.buscar(value, i):
                return True
            
        return False

class Personita:
    def __init__(self):
        self.simbolo = "🚶"
        self.posicion = []

class Celda:
    def __init__(self, elemento=""):
        self.elemento: str = elemento

    def asignar_elemento(self, elemento: str = ""):
        self.elemento = elemento
    
    def __repr__(self):
        return self.elemento if self.elemento else "  "

class Laberinto:
    def __init__(self, tamaño: int):
        self.tamaño = tamaño
        self.laberinto_obj: list[list[Celda]] = []
    
    def crear_matriz(self):
        self.laberinto_obj = [[Celda() for _ in range(self.tamaño)] for _ in range(self.tamaño)]

    def __repr__(self):
        laberinto_format = ""
        for fila in self.laberinto_obj:
            laberinto_format += " | ".join(str(celda) for celda in fila) + "\n"
        return laberinto_format

class MazeOfTerror:
    def __init__(self):
        self.personitas = []

    def iniciar_laberitno(self, numero_personas=1):
        tamaño_laberinto = int(input("Ingresa el tamaño de la matriz NxN: "))
        self.mi_laberinto = Laberinto(tamaño=tamaño_laberinto)
        self.mi_laberinto.crear_matriz()
        self.tamaño = tamaño_laberinto

        self.colocar_persona(tamaño_laberinto, numero_personas)
        self.asignar_salida()

        if tamaño_laberinto <= 5:
            for _ in range(3):
                self.colocar_bloqueos()
                self.colocar_retrasadores()
                self.colocar_trampas()

    def asignar_salida(self):
        while True:
            fila = random.randint(0, self.tamaño - 1)
            columna = random.randint(0, self.tamaño - 1)
            if self.mi_laberinto.laberinto_obj[fila][columna].elemento == "":
                self.salida = [fila, columna]
                self.mi_laberinto.laberinto_obj[fila][columna].elemento = "🏁"
                break

    def colocar_persona(self, tamaño_laberinto, numero_personas=1):
        for _ in range(numero_personas):
            while True:
                fila = random.randint(0, tamaño_laberinto - 1)
                columna = random.randint(0, tamaño_laberinto - 1)
                if self.mi_laberinto.laberinto_obj[fila][columna].elemento == "":
                    personita = Personita()
                    personita.posicion = [fila, columna]
                    self.mi_laberinto.laberinto_obj[fila][columna].elemento = personita.simbolo
                    self.personitas.append(personita)
                    break

    def colocar_bloqueos(self):
        self._colocar_elemento("B ")

    def colocar_trampas(self):
        self._colocar_elemento("T ")

    def colocar_retrasadores(self):
        self._colocar_elemento("R ")

    def _colocar_elemento(self, simbolo):
        while True:
            fila = random.randint(0, self.tamaño - 1)
            columna = random.randint(0, self.tamaño - 1)
            if self.mi_laberinto.laberinto_obj[fila][columna].elemento == "":
                self.mi_laberinto.laberinto_obj[fila][columna].elemento = simbolo
                break

    def imprimir(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.mi_laberinto)
        time.sleep(0.5)

    def mover_personas(self):
        for persona in self.personitas:
            fila, col = persona.posicion
            posibles_movimientos = [
                (fila - 1, col), (fila + 1, col), (fila, col - 1), (fila, col + 1)
            ]
            for nueva_fila, nueva_col in posibles_movimientos:
                if 0 <= nueva_fila < self.tamaño and 0 <= nueva_col < self.tamaño:
                    celda_destino = self.mi_laberinto.laberinto_obj[nueva_fila][nueva_col]
                    if celda_destino.elemento == "" or celda_destino.elemento == "🏁":
                        self.mi_laberinto.laberinto_obj[fila][col].elemento = ""
                        celda_destino.elemento = persona.simbolo
                        persona.posicion = [nueva_fila, nueva_col]
                        break

    def iterar_juego(self):
        self.mover_personas()
        self.imprimir()

    def menu(self):
        flag_ciclo = True
        flag_imprimir = False

        while flag_ciclo:
            if flag_imprimir:
                self.imprimir()
            try:
                print("\n🧭 Menú Interactivo")
                print("1.   Iniciar simulación")
                print("2.   Colocar bloqueos")
                print("3.   Colocar trampas")
                print("4.   Colocar retrasadores")
                print("5.   Ejecutar siguiente iteración")
                print("6.   Salir del juego")
                eleccion = int(input("Selecciona: "))
                flag_ciclo = self.elegir_accion(eleccion)
                flag_imprimir = True
            
            except Exception as e:
                print("Por favor inicia el laberinto (opción 1.)")
                continue

    def elegir_accion(self, eleccion: int):
        match eleccion:
            case 1:
                numero_personas = int(input("Ingrese el número de personas: "))
                self.iniciar_laberitno(numero_personas)
                return True
            case 2:
                self.colocar_bloqueos()
                return True
            case 3:
                self.colocar_trampas()
                return True
            case 4:
                self.colocar_retrasadores()
                return True
            case 5:
                self.iterar_juego()
                return True
            case 6:
                return False

if __name__ == "__main__":
    MazeOfTerror().menu()
