import random
import os
class Celda:
    def __init__(self, elemento = ""):
        self.elemento: str = elemento

    def asignar_elemento(self, elemento: str = ""):
        self.elemento = elemento
    
    def __repr__(self):
        return self.elemento


class Laberinto:
    def __init__(self, tamaño: int):
        self.tamaño = tamaño
        self.laberinto_obj: list[list[Celda]] = []
    
    def crear_matriz(self):
        self.laberinto_obj = []
        for _ in range(self.tamaño):
            fila = []
            for _ in range(self.tamaño):
                celda = Celda()
                fila.append(celda)
            self.laberinto_obj.append(fila)
        return

    def __repr__(self):
            laberinto_format = ""
            for fila in self.laberinto_obj:
                laberinto_format += " | ".join(str(celda) if celda.elemento else "  " for celda in fila) + "\n"
            return laberinto_format

class Personita:
    def __init__(self):
        self.simbolo = "🚶"
        self.posicion = []
        self.movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.arbol: GeneralTree = None
        self.retraso = False

    def iniciar_arbol(self, laberinto: Laberinto):
        self.arbol = GeneralTree(Node(tuple(self.posicion)))
    
    def mover_por_ruta(self, laberinto: Laberinto):
        flag = True
        
        if not self.arbol or not self.arbol.ruta_mas_corta:
            print("¡Ay Muchachos!!!!")
            return False
        
        if self.retraso:
            self.retraso = False
            return True

        fila, columna = self.posicion
        laberinto.laberinto_obj[fila][columna].elemento = ""
        self.ruta = self.arbol.ruta_mas_corta[1:]  

        for _ in self.ruta:
            if laberinto.laberinto_obj[fila][columna].elemento == "":
                laberinto.laberinto_obj[fila][columna].elemento = "👣"

        for paso in self.ruta:

            fila, columna = paso
            self.posicion = [fila, columna]
            elemento_destino = laberinto.laberinto_obj[fila][columna].elemento

            if elemento_destino == "T ":
                movimiento_a_eliminar = random.choice(self.movimientos)
                self.movimientos.remove(movimiento_a_eliminar)
                print(self.movimientos)

            elif elemento_destino == "R ":
                self.retraso = True
            
            elif elemento_destino == "🏁":
                laberinto.laberinto_obj[fila][columna].elemento = f"🏁{self.simbolo}"
                print(f"    \nFelicidades saliste\n")
                flag = -1
                break

            laberinto.laberinto_obj[fila][columna].elemento = self.simbolo
            break
        return flag


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def _repr(self, level = 0):
        result = "  " * level + f"{self.value}\n"
        for child in self.children:
            result += child._repr(level + 1)
        return result

    def __repr__(self):
        return self._repr()


class GeneralTree:
    def __init__(self, root: Node = None):
        self.root = root
        self.ruta_mas_corta = []

    def insert(self, parent, child, current_node = None):
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
            if(self.insert(parent, child, i) == True):
                return True
        return False
    
    def buscar_salida(self, laberinto: Laberinto, persona: Personita, nodo_actual=None, visitados=None, ruta_actual=None):
        if self.root is None:
            self.root = Node(tuple(persona.posicion))

        if nodo_actual is None:
            nodo_actual = self.root
        if visitados is None:
            visitados = set()
        if ruta_actual is None:
            ruta_actual = []

        fila, columna = nodo_actual.value

        if (fila, columna) in visitados:
            return

        visitados.add((fila, columna))
        ruta_actual.append((fila, columna))

        celda_actual = laberinto.laberinto_obj[fila][columna].elemento

        if celda_actual == "🏁":
            if not self.ruta_mas_corta or len(ruta_actual) < len(self.ruta_mas_corta):
                self.ruta_mas_corta = list(ruta_actual)
            ruta_actual.pop()
            visitados.remove((fila, columna))
            return

        for dx, dy in persona.movimientos:
            nueva_fila, nueva_columna = fila + dx, columna + dy

            if 0 <= nueva_fila < laberinto.tamaño and 0 <= nueva_columna < laberinto.tamaño:
                nueva_celda = laberinto.laberinto_obj[nueva_fila][nueva_columna].elemento
                if nueva_celda not in ["B ", persona.simbolo] and (nueva_fila, nueva_columna) not in visitados:
                    nuevo_nodo = Node((nueva_fila, nueva_columna))
                    nodo_actual.children.append(nuevo_nodo)
                    self.buscar_salida(laberinto, persona, nuevo_nodo, visitados, ruta_actual)

        ruta_actual.pop()
        visitados.remove((fila, columna))

class MazeOfTerror:
    def limpiar_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def iniciar_laberitno(self, numero_personas = 1):
        tamaño_laberinto = random.randint(5, 7)
        self.mi_laberinto = Laberinto(tamaño = tamaño_laberinto)
        self.mi_laberinto.crear_matriz()
        self.lista_personitas = []

        self.colocar_persona(tamaño_laberinto, numero_personas)
        self.asignar_salida()

        if tamaño_laberinto == 5:
            for _ in range(3):
                self.colocar_bloqueos()
                self.colocar_retrasadores()
                self.colocar_trampas()
            return
        
        elif tamaño_laberinto == 6:
            for _ in range(5):
                self.colocar_bloqueos()
                self.colocar_retrasadores()
                self.colocar_trampas()
            return
        
        elif tamaño_laberinto == 7:
            for _ in range(9):
                self.colocar_bloqueos()
                self.colocar_retrasadores()
                self.colocar_trampas()
            return
    
    def asignar_salida(self):
        flag_posicion = True

        while flag_posicion:
                fila = random.randint(0, len(self.mi_laberinto.laberinto_obj) - 1)
                columna = random.randint(0, len(self.mi_laberinto.laberinto_obj) - 1)
            
                if self.mi_laberinto.laberinto_obj[fila][columna].elemento == "":
                    flag_posicion = False
        
        celda = self.mi_laberinto.laberinto_obj[fila][columna]
        celda.elemento = "🏁"

    
    def colocar_persona(self, tamaño_laberinto, numero_personas = 1):
        for _ in range(numero_personas):
            flag_posicion = True
            personita = Personita()
            
            while flag_posicion:
                fila = random.randint(0, tamaño_laberinto - 1)
                columna = random.randint(0, tamaño_laberinto - 1)
            
                if self.mi_laberinto.laberinto_obj[fila][columna].elemento == "":
                    flag_posicion = False
            
            self.lista_personitas.append(personita)
            celda = self.mi_laberinto.laberinto_obj[fila][columna]
            personita.posicion.extend([fila, columna])
            celda.elemento = personita.simbolo

    def colocar_bloqueos(self):
        flag_posicion = True

        while flag_posicion:
            fila = random.randint(0, len(self.mi_laberinto.laberinto_obj) - 1)
            columna = random.randint(0, len(self.mi_laberinto.laberinto_obj) - 1)

            if self.mi_laberinto.laberinto_obj[fila][columna].elemento == "":
                flag_posicion = False

        celda = self.mi_laberinto.laberinto_obj[fila][columna]
        celda.elemento = "B "
    
    def colocar_trampas(self):
        flag_posicion = True

        while flag_posicion:
            fila = random.randint(0, len(self.mi_laberinto.laberinto_obj) - 1)
            columna = random.randint(0, len(self.mi_laberinto.laberinto_obj) - 1)

            if self.mi_laberinto.laberinto_obj[fila][columna].elemento == "":
                flag_posicion = False

        celda = self.mi_laberinto.laberinto_obj[fila][columna]
        celda.elemento = "T "

    def colocar_retrasadores(self):
        flag_posicion = True

        while flag_posicion:
            fila = random.randint(0, len(self.mi_laberinto.laberinto_obj) - 1)
            columna = random.randint(0, len(self.mi_laberinto.laberinto_obj) - 1)

            if self.mi_laberinto.laberinto_obj[fila][columna].elemento == "":
                flag_posicion = False

        celda = self.mi_laberinto.laberinto_obj[fila][columna]
        celda.elemento = "R "
    
    def imprimir(self):
        print(self.mi_laberinto)

    def menu(self):
        flag_ciclo = True
        self.flag_imprimir = False

        while flag_ciclo:
            self.limpiar_terminal()
            if self.flag_imprimir:
                print(self.mi_laberinto)
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
                self.flag_imprimir = True

                if flag_ciclo == -1:
                    print(self.mi_laberinto)
                    flag_ciclo = False
            
            except Exception as e:
                print("Por favor inicia el laberinto (opcion 1.)")
                continue

    
    def elegir_accion(self, eleccion: int):
        match eleccion:
            case 1:
                self.iniciar_laberitno()
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
                for persona in self.lista_personitas:
                    persona.iniciar_arbol(self.mi_laberinto)
                    persona.arbol.buscar_salida(self.mi_laberinto, persona)
                    flag = persona.mover_por_ruta(self.mi_laberinto)                    
                return flag
            
            case 6:
                return False



if __name__ == "__main__":
    MazeOfTerror().menu()