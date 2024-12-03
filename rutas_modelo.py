import tkinter as tk
from tkinter import messagebox
import heapq

class Grafo:
    def __init__(self, num_conexiones):
        self.num_conexiones = num_conexiones
        self.grafo = {}
    
    def agregar_conexion(self, inicio, destino, distancia):
        if inicio not in self.grafo:
            self.grafo[inicio] = []
        self.grafo[inicio].append((destino, distancia))
        
        # Si el grafo es no dirigido, agrega la conexión inversa
        if destino not in self.grafo:
            self.grafo[destino] = []
        self.grafo[destino].append((inicio, distancia))
    
    def dijkstra(self, inicio, destino):
        # Algoritmo de Dijkstra para encontrar la ruta más corta
        dist = {nodo: float('inf') for nodo in self.grafo}
        dist[inicio] = 0
        prev = {nodo: None for nodo in self.grafo}
        pq = [(0, inicio)]  # (distancia, nodo)

        while pq:
            d, nodo = heapq.heappop(pq)

            if d > dist[nodo]:
                continue

            for vecino, distancia in self.grafo[nodo]:
                nueva_dist = dist[nodo] + distancia
                if nueva_dist < dist[vecino]:
                    dist[vecino] = nueva_dist
                    prev[vecino] = nodo
                    heapq.heappush(pq, (nueva_dist, vecino))

        # Reconstruir la ruta más corta
        ruta = []
        nodo = destino
        while prev[nodo] is not None:
            ruta.insert(0, (prev[nodo], nodo, dist[nodo] - dist[prev[nodo]]))
            nodo = prev[nodo]
        
        return ruta, dist[destino]

class VentanaConexiones(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ingreso de Conexiones del Grafo")
        self.geometry("600x700")
        
        self.grafo = None

        # Etiqueta y entrada para la cantidad de conexiones
        tk.Label(self, text="Ingrese la cantidad total de conexiones (aristas) del grafo:").pack(pady=10)
        self.num_conexiones_entry = tk.Entry(self)
        self.num_conexiones_entry.pack(pady=5)

        # Botón para continuar
        tk.Button(self, text="Aceptar", command=self.crear_tabla).pack(pady=20)

    def crear_tabla(self):
        try:
            num_conexiones = int(self.num_conexiones_entry.get())
            
            if num_conexiones <= 0:
                messagebox.showerror("Error", "La cantidad de conexiones debe ser positiva.")
                return
            
            # Crear el objeto grafo
            self.grafo = Grafo(num_conexiones)

            # Crear la tabla para ingresar las conexiones
            self.mostrar_tabla(num_conexiones)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un número válido de conexiones.")

    def mostrar_tabla(self, num_conexiones):
        # Ocultar la entrada de número de conexiones
        self.num_conexiones_entry.pack_forget()

        # Crear la tabla con campos para Nodo de Inicio, Nodo de Destino y Distancia
        self.tabla_frame = tk.Frame(self)
        self.tabla_frame.pack(pady=10)

        # Títulos de las columnas
        tk.Label(self.tabla_frame, text="Conexión #").grid(row=0, column=0)
        tk.Label(self.tabla_frame, text="Nodo de Inicio").grid(row=0, column=1)
        tk.Label(self.tabla_frame, text="Nodo de Destino").grid(row=0, column=2)
        tk.Label(self.tabla_frame, text="Distancia").grid(row=0, column=3)

        # Crear campos para cada conexión
        self.conexion_entries = []
        for i in range(num_conexiones):
            tk.Label(self.tabla_frame, text=str(i + 1)).grid(row=i + 1, column=0)
            inicio_entry = tk.Entry(self.tabla_frame)
            inicio_entry.grid(row=i + 1, column=1)
            destino_entry = tk.Entry(self.tabla_frame)
            destino_entry.grid(row=i + 1, column=2)
            distancia_entry = tk.Entry(self.tabla_frame)
            distancia_entry.grid(row=i + 1, column=3)
            self.conexion_entries.append((inicio_entry, destino_entry, distancia_entry))

        # Botón para procesar la tabla
        tk.Button(self, text="Aceptar Conexiones", command=self.procesar_conexiones).pack(pady=20)

        # Entrada para el nodo de inicio
        tk.Label(self, text="Nodo de Inicio:").pack(pady=5)
        self.nodo_inicio_entry = tk.Entry(self)
        self.nodo_inicio_entry.pack(pady=5)

        # Entrada para el nodo de destino
        tk.Label(self, text="Nodo de Destino:").pack(pady=5)
        self.nodo_destino_entry = tk.Entry(self)
        self.nodo_destino_entry.pack(pady=5)

    def procesar_conexiones(self):
        try:
            # Recoger los datos de las conexiones
            for inicio_entry, destino_entry, distancia_entry in self.conexion_entries:
                inicio = int(inicio_entry.get())
                destino = int(destino_entry.get())
                distancia = float(distancia_entry.get())
                
                if inicio < 0 or destino < 0 or distancia <= 0:
                    messagebox.showerror("Error", "Los valores de los nodos y las distancias deben ser positivos.")
                    return
                
                # Agregar la conexión al grafo
                self.grafo.agregar_conexion(inicio, destino, distancia)
            
            # Obtener los nodos de inicio y destino
            nodo_inicio = int(self.nodo_inicio_entry.get())
            nodo_destino = int(self.nodo_destino_entry.get())

            # Obtener la ruta óptima
            ruta, distancia_total = self.grafo.dijkstra(nodo_inicio, nodo_destino)
            
            # Mostrar la tabla de resultados
            self.mostrar_resultados(ruta, distancia_total)
        
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos para todos los campos.")

    def mostrar_resultados(self, ruta, distancia_total):
        # Mostrar los resultados de la ruta óptima
        resultados_texto = "Ruta Óptima:\n"
        acumulada = 0
        for i, (inicio, destino, distancia) in enumerate(ruta):
            acumulada += distancia
            resultados_texto += f"Conexión {i + 1}: Nodo {inicio} -> Nodo {destino}, Distancia: {distancia}, Distancia Acumulada: {acumulada}\n"
        
        resultados_texto += f"\nDistancia Total: {distancia_total}"
        
        # Mostrar resultados en una ventana
        messagebox.showinfo("Ruta Óptima", resultados_texto)