import tkinter as tk
from tkinter import messagebox
import threading
import copy
import heapq
from typing import List, Tuple, Optional, Set, Any

Tablero = List[List[Any]]


class Estado:
    def __init__(self, fichas: Tablero, g: int = 0, anterior: Optional['Estado'] = None,
                 objetivo: Optional[Tablero] = None):
        self.fichas = fichas
        self.g = g
        self.anterior = anterior
        self.h = self._calcular_manhattan(objetivo) if objetivo else 0
        self.f = self.g + self.h

    def _calcular_manhattan(self, objetivo: Tablero) -> int:
        distancia = 0
        n_filas = len(self.fichas)

        for i in range(n_filas):
            for j in range(n_filas):
                valor = self.fichas[i][j]
                if valor != " ":
                    for fila_obj in range(n_filas):
                        for col_obj in range(n_filas):
                            if objetivo[fila_obj][col_obj] == valor:
                                distancia += abs(i - fila_obj) + abs(j - col_obj)
        return distancia

    def obtener_vecinos(self, objetivo: Tablero) -> List['Estado']:
        n_filas = len(self.fichas)
        vecinos = []
        fila_vacia, col_vacia = 0, 0

        for i in range(n_filas):
            for j in range(n_filas):
                if self.fichas[i][j] == " ":
                    fila_vacia, col_vacia = i, j

        movimientos = [
            (fila_vacia - 1, col_vacia),
            (fila_vacia + 1, col_vacia),
            (fila_vacia, col_vacia - 1),
            (fila_vacia, col_vacia + 1)
        ]

        for i, j in movimientos:
            if 0 <= i < n_filas and 0 <= j < n_filas:
                nuevas_fichas = copy.deepcopy(self.fichas)
                nuevas_fichas[fila_vacia][col_vacia], nuevas_fichas[i][j] = nuevas_fichas[i][j], \
                nuevas_fichas[fila_vacia][col_vacia]
                nuevo_estado = Estado(nuevas_fichas, g=self.g + 1, anterior=self, objetivo=objetivo)
                vecinos.append(nuevo_estado)

        return vecinos

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Estado):
            return NotImplemented
        return self.fichas == otro.fichas

    def __hash__(self) -> int:
        return hash(tuple(tuple(fila) for fila in self.fichas))

    def __lt__(self, otro: 'Estado') -> bool:
        return self.f < otro.f


class AgenteAEstrella:
    @staticmethod
    def resolver(tablero_inicial: Tablero, tablero_objetivo: Tablero) -> Tuple[Optional[List[Estado]], int]:
        estado_inicial = Estado(tablero_inicial, g=0, anterior=None, objetivo=tablero_objetivo)

        frontera: List[Estado] = []
        heapq.heappush(frontera, estado_inicial)

        visitados: Set[Estado] = set()
        nodos_evaluados = 0

        while frontera:
            estado_actual = heapq.heappop(frontera)
            nodos_evaluados += 1

            if estado_actual.fichas == tablero_objetivo:
                camino = []
                while estado_actual:
                    camino.append(estado_actual)
                    estado_actual = estado_actual.anterior
                camino.reverse()
                return camino, nodos_evaluados

            visitados.add(estado_actual)

            for vecino in estado_actual.obtener_vecinos(tablero_objetivo):
                if vecino not in visitados:
                    heapq.heappush(frontera, vecino)

        return None, nodos_evaluados


class JuegoOchoDigitosGUI:
    def __init__(self, ventana_principal: tk.Tk):
        self.ventana_principal = ventana_principal

        self.COLOR_FONDO = "#F0F0F0"
        self.COLOR_TEXTO = "#000000"
        self.COLOR_FICHA = "#E0E0E0"
        self.COLOR_FICHA_VACIA = "#C0C0C0"

        self.ventana_principal.title("agente heurístico (A*)")
        self.ventana_principal.geometry("400x560")
        self.ventana_principal.configure(bg=self.COLOR_FONDO)

        self.tablero_inicial = [
            [7, 2, 4],
            [5, " ", 6],
            [8, 3, 1]
        ]
        self.tablero_objetivo = [
            [" ", 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]

        self.tablero_actual = copy.deepcopy(self.tablero_inicial)
        self.botones_cuadricula: List[List[tk.Button]] = []
        self.bloquear_interfaz = False

        self._construir_interfaz()
        self._actualizar_vista()

    def _construir_interfaz(self):
        tk.Label(
            self.ventana_principal,
            text="Juego 8 Dígitos - A* heurístico",
            font=("Arial", 16, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TEXTO
        ).pack(pady=(15, 5))

        marco_tablero = tk.Frame(self.ventana_principal, bg=self.COLOR_FONDO)
        marco_tablero.pack(pady=10)

        for i in range(3):
            fila_botones = []
            for j in range(3):
                boton = tk.Button(
                    marco_tablero,
                    text="",
                    font=("Arial", 28, "bold"),
                    width=3,
                    height=1,
                    relief="raised",
                    command=lambda f=i, c=j: self.mover_ficha_usuario(f, c)
                )
                boton.grid(row=i, column=j, padx=2, pady=2)
                fila_botones.append(boton)
            self.botones_cuadricula.append(fila_botones)

        self.etiqueta_estado = tk.Label(
            self.ventana_principal,
            text="mueve las piezas o presiona resolver",
            font=("Arial", 10),
            bg=self.COLOR_FONDO, fg="blue"
        )
        self.etiqueta_estado.pack(pady=(5, 5))

        self.etiqueta_estadisticas = tk.Label(
            self.ventana_principal,
            text="nodos evaluados: 0",
            font=("Arial", 10, "italic"),
            bg=self.COLOR_FONDO, fg="#555555"
        )
        self.etiqueta_estadisticas.pack(pady=(0, 10))

        marco_controles = tk.Frame(self.ventana_principal, bg=self.COLOR_FONDO)
        marco_controles.pack(pady=10)

        self.boton_reiniciar = tk.Button(
            marco_controles,
            text="reiniciar",
            font=("Arial", 10),
            command=self.reiniciar_juego,
            width=10
        )
        self.boton_reiniciar.grid(row=0, column=0, padx=10)

        self.boton_resolver = tk.Button(
            marco_controles,
            text="resolver con heurística",
            font=("Arial", 10),
            command=self.iniciar_resolucion_ia,
            width=20
        )
        self.boton_resolver.grid(row=0, column=1, padx=10)

    def _actualizar_vista(self):
        for i in range(3):
            for j in range(3):
                valor = self.tablero_actual[i][j]
                boton = self.botones_cuadricula[i][j]

                if valor == " ":
                    boton.configure(text="", bg=self.COLOR_FICHA_VACIA, state=tk.DISABLED)
                else:
                    boton.configure(
                        text=str(valor),
                        bg=self.COLOR_FICHA,
                        fg=self.COLOR_TEXTO,
                        state=tk.NORMAL if not self.bloquear_interfaz else tk.DISABLED
                    )

        if self.tablero_actual == self.tablero_objetivo:
            self.etiqueta_estado.configure(text="rompecabezas resuelto con éxito", fg="green")
            self.bloquear_interfaz = True
            for fila in self.botones_cuadricula:
                for boton in fila:
                    boton.configure(state=tk.DISABLED)

    def mover_ficha_usuario(self, fila: int, columna: int):
        if self.bloquear_interfaz:
            return

        fila_vacia, columna_vacia = -1, -1
        for i in range(3):
            for j in range(3):
                if self.tablero_actual[i][j] == " ":
                    fila_vacia, columna_vacia = i, j

        es_adyacente = (abs(fila_vacia - fila) + abs(columna_vacia - columna)) == 1

        if es_adyacente:
            self.tablero_actual[fila_vacia][columna_vacia] = self.tablero_actual[fila][columna]
            self.tablero_actual[fila][columna] = " "
            self._actualizar_vista()

    def reiniciar_juego(self):
        self.tablero_actual = copy.deepcopy(self.tablero_inicial)
        self.bloquear_interfaz = False
        self.etiqueta_estado.configure(text="mueve las piezas o presiona resolver", fg="blue")
        self.etiqueta_estadisticas.configure(text="Nodos evaluados: 0")
        self.boton_resolver.configure(state=tk.NORMAL)
        self._actualizar_vista()

    def iniciar_resolucion_ia(self):
        self.bloquear_interfaz = True
        self._actualizar_vista()
        self.boton_resolver.configure(state=tk.DISABLED)
        self.boton_reiniciar.configure(state=tk.DISABLED)
        self.etiqueta_estado.configure(text="IA calculando ruta óptima (A*)...", fg="orange")
        self.etiqueta_estadisticas.configure(text="evaluando...")

        hilo_agente = threading.Thread(target=self._ejecutar_agente)
        hilo_agente.start()

    def _ejecutar_agente(self):
        solucion, nodos_evaluados = AgenteAEstrella.resolver(self.tablero_actual, self.tablero_objetivo)

        if solucion:
            self.ventana_principal.after(0, self._preparar_animacion, solucion, nodos_evaluados)
        else:
            self.ventana_principal.after(0, self._mostrar_error_solucion, nodos_evaluados)

    def _mostrar_error_solucion(self, nodos_evaluados: int):
        self.etiqueta_estado.configure(text="error, no se encontró solución", fg="red")
        self.etiqueta_estadisticas.configure(text=f"nodos evaluados sin éxito: {nodos_evaluados}")
        self.boton_reiniciar.configure(state=tk.NORMAL)

    def _preparar_animacion(self, solucion: List[Estado], nodos_evaluados: int):
        pasos = len(solucion) - 1
        self.etiqueta_estadisticas.configure(text=f"nodos evaluados: {nodos_evaluados}")
        self.etiqueta_estado.configure(
            text=f"Solución encontrada, ejecutando {pasos} pasos",
            fg="green"
        )
        self._animar_paso(solucion, 0, pasos, nodos_evaluados)

    def _animar_paso(self, solucion: List[Estado], indice: int, total_pasos: int, nodos_evaluados: int):
        if indice < len(solucion):
            self.tablero_actual = copy.deepcopy(solucion[indice].fichas)
            self._actualizar_vista()
            self.ventana_principal.after(400, self._animar_paso, solucion, indice + 1, total_pasos, nodos_evaluados)
        else:
            self.boton_reiniciar.configure(state=tk.NORMAL)
            messagebox.showinfo("completado",
                                f"Completado\n\npasos del camino final: {total_pasos}\ntableros (nodos) evaluados por la IA: {nodos_evaluados}")


if __name__ == '__main__':
    raiz = tk.Tk()
    raiz.resizable(False, False)
    app = JuegoOchoDigitosGUI(raiz)
    raiz.mainloop()