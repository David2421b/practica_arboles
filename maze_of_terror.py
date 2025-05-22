import random

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

    def buscar(self, value, current_node = None):
        if current_node is None:
            current_node = self.root

        if value == current_node.value:
            return True
        
        for i in current_node.children:
            if (self.buscar(value, i) == True):
                return True
            
        return False


class Personita:
    def __init__(self):
        self.simbolo = "🚶"
        self.posicion = []


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
            
class MazeOfTerror:

    def iniciar_laberitno(self, numero_personas = 1):
        tamaño_laberinto = int(input("Ingresa el tamaño de la matriz NxN: "))
        self.mi_laberinto = Laberinto(tamaño = tamaño_laberinto)
        self.mi_laberinto.crear_matriz()

        self.colocar_persona(tamaño_laberinto, numero_personas)
        self.asignar_salida()

        if tamaño_laberinto <= 5:
            for _ in range(3):
                self.colocar_bloqueos()
                self.colocar_retrasadores()
                self.colocar_trampas()
    
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
        flag_imprimir = False

        while flag_ciclo:
            if flag_imprimir:
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
                flag_imprimir = True
            
            except Exception as e:
                print("Por favor inicia el laberinto (opcion 1.)")
                continue

    
    def elegir_accion(self, eleccion: int):
        match eleccion:
            case 1:
                numero_personas = int(input("Ingrese el numero de personas: "))
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
            
            case 6:
                return False



if __name__ == "__main__":
    MazeOfTerror().menu()