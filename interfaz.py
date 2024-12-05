#interfaz.py
import tkinter as tk
from tkinter import ttk, messagebox
from cpm_modelo import calcular_camino_critico
from pert import calcular_pert
from eoq import calcular_eoq
from decision_tree_solver import DecisionTreeSolver
from ahp import AHP
from mm1_modelo import MM1Ventana
from mmc_modelo import MMCVentana
from nacmuer_modelo import NacimientoMuerteVentana
from mg1_modelo import MG1Ventana
from mgk_modelo import MGKVentana
from ffinitas_modelo import FuentesFinitasVentana
from rutas_modelo import VentanaConexiones
from programacion_cuadratica import ProgramacionCuadraticaVentana
from programacion_convexa import ProgramacionConvexaVentana
from programacion_no_convexa import ProgramacionNoConvexaVentana
from programacion_geometrica import ProgramacionGeometricaVentana
from programacion_fraccional import ProgramacionFraccionalVentana
from programacion_separable import ProgramacionSeparableVentana
from optimizacion_modelo import OptimizacionNoRestringidaVentana
import matplotlib.pyplot as plt
import networkx as nx
import math
import scipy.stats as stats  
import numpy as np
import os
import io
import graphviz
from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree
import pydotplus
from PIL import Image, ImageTk
from scipy.stats import norm 

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Herramientas de Gestión y Decisiones")
        self.geometry("800x600")
        self.configure(bg="#f4f4f4")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 12), padding=10)

        self.crear_menu_principal()

    def crear_menu_principal(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Seleccione una categoría:", font=("Helvetica", 16, "bold"), bg="#f4f4f4", fg="#333").pack(pady=20)

        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        categorias = [
            ("Modelo de Programación de Proyectos", self.abrir_menu_programacion_proyectos),
            ("Sistemas de Inventario", self.abrir_menu_sistemas_inventario),
            ("Teorías de Decisión", self.abrir_menu_teorias_decision),
            ("Teoría de Líneas de Espera", self.abrir_menu_lineas_espera),
            ("Programación Dinámica", self.abrir_menu_programacion_dinamica),
            ("Métodos de Optimización", self.abrir_menu_metodos_optimizacion),
        ]

        for texto, comando in categorias:
            ttk.Button(main_frame, text=texto, command=comando).pack(pady=5, fill="x")

        ttk.Button(self, text="Salir", command=self.quit).pack(pady=10)

    def crear_menu_categoria(self, titulo, opciones):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text=titulo, font=("Helvetica", 16, "bold"), bg="#f4f4f4", fg="#333").pack(pady=20)

        categoria_frame = ttk.Frame(self, padding="20")
        categoria_frame.pack(fill="both", expand=True)

        for texto, comando in opciones:
            ttk.Button(categoria_frame, text=texto, command=comando).pack(pady=5, fill="x")

        ttk.Button(self, text="Volver al Menú Principal", command=self.crear_menu_principal).pack(pady=20)

    def abrir_menu_programacion_proyectos(self):
        opciones = [
            ("CPM (Camino Crítico)", self.abrir_cpm_ventana),
            ("PERT", self.abrir_pert_ventana),
        ]
        self.crear_menu_categoria("Modelo de Programación de Proyectos", opciones)

    def abrir_menu_sistemas_inventario(self):
        opciones = [
            ("EOQ", self.abrir_eoq_ventana),
            ("Inventario con Faltantes Planeados", self.abrir_faltantes_ventana),
            ("Modelo de Descuentos por Cantidad", self.abrir_descuentos_ventana),
            ("Modelo de Tamaño de Lote de Producción", self.abrir_produccion_economico_ventana),
            ("Modelo de Revisión Periódica con Demanda Probabilística", self.abrir_revision_periodica_ventana),
            ("Modelo de Inventario de Periodo Único", self.abrir_periodo_unico_ventana),
            ("Modelo con Demanda y Tiempo de Entrega Probabilístico", self.abrir_demanda_probabilistica_ventana),
            ("Modelo con Demanda y Tiempo de Entrega Probabilístico y Ventas Perdidas", self.abrir_ventas_perdidas_ventana),
            ("Modelo de Punto de Reorden con Demanda Probabilística", self.abrir_punto_reorden_ventana),
        ]
        self.crear_menu_categoria("Sistemas de Inventario", opciones)

    def abrir_menu_teorias_decision(self):
        opciones = [
            ("Árboles de Decisión", self.abrir_decision_tree_ventana),
            ("Decisiones en Incertidumbre", self.abrir_decisiones_incertidumbre_ventana),
            ("AHP (Análisis de Jerarquía Analítica)", self.abrir_ahp_ventana),
        ]
        self.crear_menu_categoria("Teorías de Decisión", opciones)

    def abrir_menu_lineas_espera(self):
        opciones = [
            ("Modelo M/M/1", self.abrir_mm1_ventana),
            ("Modelo M/M/c", self.abrir_mmc_ventana),
            ("Esquema de Nacimiento y Muerte", self.abrir_nacimiento_muerte_ventana),
            ("Modelo M/G/1", self.abrir_mg1_ventana),
            ("Modelo M/G/K", self.abrir_mgk_ventana),
            ("Modelos con Fuentes Finitas", self.abrir_fuentes_finitas_ventana),
        ]
        self.crear_menu_categoria("Teoría de Líneas de Espera", opciones)

    def abrir_menu_programacion_dinamica(self):
        opciones = [
            ("Ruta Optima - Costo Minimo", self.abrir_programacion_dinamica_ventana),
        ]
        self.crear_menu_categoria("Programación Dinámica", opciones)
    
    def abrir_menu_metodos_optimizacion(self):
        opciones = [
            ("Programacion Cuadratica", self.abrir_programacion_cuadratica_ventana),
            ("Programacion Convexa", self.abrir_programacion_convexa_ventana),
            ("Programacion no Convexa", self.abrir_programacion_no_convexa_ventana),
            ("Programacion Geometrica", self.abrir_programacion_geometrica_ventana),
            ("Programacion Fraccional", self.abrir_programacion_fraccional_ventana),
            ("Programacion Separable", self.abrir_programacion_separable_ventana),
            ("Optimizacion no Restringida con una Variable", self.abrir_optimizacion_variable_ventana),
        ]
        self.crear_menu_categoria("Metodos de Optimizacion", opciones)
        
    #PROGRAMACION CUADRATICA
    def abrir_programacion_cuadratica_ventana(self):
        ProgramacionCuadraticaVentana(self)

    #PROGRAMACION CONVEXA
    def abrir_programacion_convexa_ventana(self):
        ProgramacionConvexaVentana(self)

    #PROGRAMACION NO CONVEXA
    def abrir_programacion_no_convexa_ventana(self):
        ProgramacionNoConvexaVentana(self)

    #PROGRAMACION GEOMETRICA
    def abrir_programacion_geometrica_ventana(self):
        ProgramacionGeometricaVentana(self)

    #PROGRAMACION FRACCIONAL
    def abrir_programacion_fraccional_ventana(self):
        ProgramacionFraccionalVentana(self)

    #PROGRAMACION SEPARABLE
    def abrir_programacion_separable_ventana(self):
        ProgramacionSeparableVentana(self)

    #OPTIMIZACION NO RESTRINGIDA CON UNA VARIABLE
    def abrir_optimizacion_variable_ventana(self):
        OptimizacionNoRestringidaVentana(self)


    #RUTA OPTIMA / COSTO MINIMO
    def abrir_programacion_dinamica_ventana(self):
        VentanaConexiones(self)
    
    #VENTANA M/M/1
    def abrir_mm1_ventana(self):
        MM1Ventana(self)
    
    #VENTANA M/M/C
    def abrir_mmc_ventana(self):
        MMCVentana(self)

    #VENTANA NACIMIENTO Y MUERTE
    def abrir_nacimiento_muerte_ventana(self):
        NacimientoMuerteVentana(self)

    #VENTANA M/G/1
    def abrir_mg1_ventana(self):
        MG1Ventana(self)
    
    #VENTANA M/G/K
    def abrir_mgk_ventana(self):
        MGKVentana(self)
    
    #VENTANA FUENTES FINITAS
    def abrir_fuentes_finitas_ventana(self):
        FuentesFinitasVentana(self)

    #VENTANA CPM
    def abrir_cpm_ventana(self):
        ventana = tk.Toplevel(self)
        ventana.title("CPM - Camino Crítico")
        ventana.geometry("500x400")
        ventana.configure(bg="#f4f4f4")

        # Etiquetas de encabezado
        encabezados = ["Predecesor", "Tarea", "Duración"]
        for idx, texto in enumerate(encabezados):
            tk.Label(
                ventana,
                text=texto,
                font=("Helvetica", 12, "bold"),
                bg="#f4f4f4",
                fg="#333"
            ).grid(row=0, column=idx, pady=5, padx=5)

        # Frame principal para las entradas
        self.frame_cpm = ttk.Frame(ventana, padding="10")
        self.frame_cpm.grid(row=1, column=0, columnspan=3, pady=10)

        # Inicializar lista de entradas y agregar la primera fila
        self.cpm_entradas = []
        self.agregar_entrada_cpm()

        # Botones de acción
        ttk.Button(
            ventana, text="Agregar Tarea", command=self.agregar_entrada_cpm
        ).grid(row=2, column=0, pady=10, padx=5)

        ttk.Button(
            ventana, text="Calcular Camino Crítico", command=self.calcular_cpm
        ).grid(row=2, column=1, pady=10, padx=5)

        ttk.Button(
            ventana, text="Mostrar Gráfico", command=self.mostrar_grafico_cpm
        ).grid(row=2, column=2, pady=10, padx=5)

        # Caja de texto para mostrar resultados
        self.cpm_resultado = tk.Text(
            ventana, height=10, width=50, font=("Helvetica", 10), bg="#ffffff", fg="#333"
        )
        self.cpm_resultado.grid(row=3, column=0, columnspan=3, pady=10)
    
    def agregar_entrada_cpm(self):
        inicio = tk.Entry(self.frame_cpm)
        fin = tk.Entry(self.frame_cpm)
        duracion = tk.Entry(self.frame_cpm)
        inicio.grid(row=len(self.cpm_entradas), column=0)
        fin.grid(row=len(self.cpm_entradas), column=1)
        duracion.grid(row=len(self.cpm_entradas), column=2)
        self.cpm_entradas.append((inicio, fin, duracion))
    
    def calcular_cpm(self):
        actividades = []
        for inicio, fin, dur in self.cpm_entradas:
            if inicio.get() and fin.get() and dur.get():
                actividades.append({
                    'inicio': inicio.get(),
                    'fin': fin.get(),
                    'duracion': float(dur.get())
                })
        try:
            camino, duracion = calcular_camino_critico(actividades)
            self.cpm_resultado.delete('1.0', tk.END)
            self.cpm_resultado.insert(tk.END, f"Camino Crítico: {' -> '.join(camino)}\nDuración Total: {duracion}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def mostrar_grafico_cpm(self):
        actividades = []
        for inicio, fin, dur in self.cpm_entradas:
            if inicio.get() and fin.get() and dur.get():
                actividades.append({
                    'inicio': inicio.get(),
                    'fin': fin.get(),
                    'duracion': float(dur.get())
                })
        try:
            camino, duracion = calcular_camino_critico(actividades)
            
            G = nx.DiGraph()
            for actividad in actividades:
                G.add_edge(actividad['inicio'], actividad['fin'], weight=actividad['duracion'])
            
            pos = nx.spring_layout(G) 
            labels = nx.get_edge_attributes(G, 'weight')
            
            plt.figure(figsize=(8, 6))
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            
            # Resaltar camino crítico
            edges = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='r', width=2)
            
            plt.title(f"Camino Crítico: {' -> '.join(camino)}\nDuración Total: {duracion}")
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    #VENTANA PERT
    def abrir_pert_ventana(self):
        ventana = tk.Toplevel(self)
        ventana.title("PERT")
        ventana.geometry("500x300")

        tk.Label(ventana, text="Inicio").grid(row=0, column=0)
        tk.Label(ventana, text="Fin").grid(row=0, column=1)
        tk.Label(ventana, text="Optimista").grid(row=0, column=2)
        tk.Label(ventana, text="Probable").grid(row=0, column=3)
        tk.Label(ventana, text="Pesimista").grid(row=0, column=4)
        
        self.frame_pert = ttk.Frame(ventana)
        self.frame_pert.grid(row=1, column=0, columnspan=5)
        
        self.pert_entradas = []
        self.agregar_entrada_pert() 
        
        tk.Button(ventana, text="Agregar Tarea", command=self.agregar_entrada_pert).grid(row=2, column=0)
        tk.Button(ventana, text="Calcular PERT", command=self.calcular_pert).grid(row=2, column=1)
        tk.Button(ventana, text="Mostrar Gráfico", command=self.mostrar_grafico_pert).grid(row=2, column=2)
        
        self.pert_resultado = tk.Text(ventana, height=10, width=70)
        self.pert_resultado.grid(row=3, column=0, columnspan=5)
        
        tk.Label(ventana, text="Tiempo Proyectado (Días)").grid(row=4, column=0)
        self.tiempo_proyectado = tk.Entry(ventana)
        self.tiempo_proyectado.grid(row=4, column=1)
        
        tk.Button(ventana, text="Calcular Probabilidad", command=self.calcular_probabilidad_pert).grid(row=4, column=2)
        self.probabilidad_resultado = tk.Label(ventana, text="", font=("Arial", 12))
        self.probabilidad_resultado.grid(row=5, column=0, columnspan=3)
    
    def agregar_entrada_pert(self):
        inicio = tk.Entry(self.frame_pert)
        fin = tk.Entry(self.frame_pert)
        optimista = tk.Entry(self.frame_pert)
        probable = tk.Entry(self.frame_pert)
        pesimista = tk.Entry(self.frame_pert)
        inicio.grid(row=len(self.pert_entradas), column=0)
        fin.grid(row=len(self.pert_entradas), column=1)
        optimista.grid(row=len(self.pert_entradas), column=2)
        probable.grid(row=len(self.pert_entradas), column=3)
        pesimista.grid(row=len(self.pert_entradas), column=4)
        self.pert_entradas.append((inicio, fin, optimista, probable, pesimista))
    
    def calcular_pert(self):
        actividades = []
        for inicio, fin, opt, prob, pes in self.pert_entradas:
            if inicio.get() and fin.get() and opt.get() and prob.get() and pes.get():
                actividades.append({
                    'inicio': inicio.get(),
                    'fin': fin.get(),
                    'optimista': float(opt.get()),
                    'probable': float(prob.get()),
                    'pesimista': float(pes.get())
                })
        try:
            camino, duracion = calcular_pert(actividades)
            self.pert_resultado.delete('1.0', tk.END)
            self.pert_resultado.insert(tk.END, f"Camino Crítico PERT: {' -> '.join(camino)}\nDuración Esperada Total: {duracion}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def calcular_probabilidad_pert(self):
        actividades = []
        for inicio, fin, opt, prob, pes in self.pert_entradas:
            if inicio.get() and fin.get() and opt.get() and prob.get() and pes.get():
                actividades.append({
                    'optimista': float(opt.get()),
                    'probable': float(prob.get()),
                    'pesimista': float(pes.get())
                })
        
        try:
            T_esperado = 0
            varianza_total = 0
            for act in actividades:
                T_esperado += (act['optimista'] + 4 * act['probable'] + act['pesimista']) / 6
                sigma_act = (act['pesimista'] - act['optimista']) / 6
                varianza_total += sigma_act ** 2

            sigma_total = math.sqrt(varianza_total)

            T_proyectado = float(self.tiempo_proyectado.get())
            
            Z = (T_proyectado - T_esperado) / sigma_total
      
            probabilidad = stats.norm.cdf(Z) * 100  
            
            self.probabilidad_resultado.config(text=f"Probabilidad de terminar en {T_proyectado} días: {probabilidad:.2f}%")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_grafico_pert(self):
        actividades = []
        for inicio, fin, opt, prob, pes in self.pert_entradas:
            if inicio.get() and fin.get() and opt.get() and prob.get() and pes.get():
                actividades.append({
                    'inicio': inicio.get(),
                    'fin': fin.get(),
                    'optimista': float(opt.get()),
                    'probable': float(prob.get()),
                    'pesimista': float(pes.get())
                })
        try:
            camino, duracion = calcular_pert(actividades)

            G = nx.DiGraph()
            for actividad in actividades:
                G.add_edge(actividad['inicio'], actividad['fin'], weight=actividad['probable'])
            
            pos = nx.spring_layout(G) 
            labels = nx.get_edge_attributes(G, 'weight')
            
            plt.figure(figsize=(8, 6))
            nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=2000, font_size=10, font_weight='bold')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            
            edges = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='r', width=2)
            
            plt.title(f"Camino Crítico PERT: {' -> '.join(camino)}\nDuración Esperada Total: {duracion}")
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    #VENTANA EOQ
    def abrir_eoq_ventana(self):
        ventana = tk.Toplevel(self)
        ventana.title("EOQ")
        ventana.geometry("500x300")

        tk.Label(ventana, text="Demanda Anual (D)").grid(row=0, column=0)
        tk.Label(ventana, text="Costo por Pedido (S)").grid(row=1, column=0)
        tk.Label(ventana, text="Costo de Mantener (H)").grid(row=2, column=0)
        tk.Label(ventana, text="Tiempo de Entrega (LT) en días").grid(row=3, column=0)
        
        self.eoq_D = tk.Entry(ventana)
        self.eoq_S = tk.Entry(ventana)
        self.eoq_H = tk.Entry(ventana)
        self.eoq_LT = tk.Entry(ventana)
        
        self.eoq_D.grid(row=0, column=1)
        self.eoq_S.grid(row=1, column=1)
        self.eoq_H.grid(row=2, column=1)
        self.eoq_LT.grid(row=3, column=1)
        
        tk.Button(ventana, text="Calcular EOQ", 
                  command=self.calcular_eoq).grid(row=4, column=1)
        self.eoq_resultado = tk.Label(ventana, text="", font=("Arial", 12))
        self.eoq_resultado.grid(row=5, column=0, columnspan=2)

        self.costo_total = tk.Label(ventana, text="", font=("Arial", 10))
        self.costo_total.grid(row=6, column=0, columnspan=2)

        self.num_ordenes = tk.Label(ventana, text="", font=("Arial", 10))
        self.num_ordenes.grid(row=7, column=0, columnspan=2)

        self.tiempo_ciclo = tk.Label(ventana, text="", font=("Arial", 10))
        self.tiempo_ciclo.grid(row=8, column=0, columnspan=2)

        self.punto_reorden = tk.Label(ventana, text="", font=("Arial", 10))
        self.punto_reorden.grid(row=9, column=0, columnspan=2)

    def calcular_eoq(self):
        try:
            D = float(self.eoq_D.get())
            S = float(self.eoq_S.get())
            H = float(self.eoq_H.get())
            LT = float(self.eoq_LT.get())
            
            eoq = calcular_eoq(D, S, H)
            
            costo_total = (D / eoq * S) + (eoq / 2 * H)
            
            num_ordenes = D / eoq
            
            tiempo_ciclo = (eoq / D) * 365
            
            demanda_diaria = D / 365
            punto_reorden = demanda_diaria * LT
            
            self.eoq_resultado.config(text=f"EOQ: {eoq:.2f} unidades")
            self.costo_total.config(text=f"Costo Total Anual: ${costo_total:.2f}")
            self.num_ordenes.config(text=f"Número de Órdenes por Año: {num_ordenes:.2f}")
            self.tiempo_ciclo.config(text=f"Tiempo de Ciclo: {tiempo_ciclo:.2f} días")
            self.punto_reorden.config(text=f"Punto de Reorden: {punto_reorden:.2f} unidades")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    #VENTANA FALTANTES
    def abrir_faltantes_ventana(self):
        ventana = tk.Toplevel(self)
        ventana.title("Modelo con Faltantes Permitidos")
        ventana.geometry("400x500")

        labels = ['Demanda Anual (D)', 'Costo por Pedido (S)', 'Costo de Mantener Inventario (H)', 'Costo por Faltantes (P)', 'Costo Unitario (CU)','Dias hábiles (DH)']
        self.entries = {}
        for label in labels:
            tk.Label(ventana, text=label).pack()
            entry = tk.Entry(ventana)
            entry.pack()
            self.entries[label] = entry

        tk.Button(ventana, text="Calcular", command=self.calcular_faltantes).pack(pady=10)

        self.resultado_texto = tk.Text(ventana, height=15, width=50)
        self.resultado_texto.pack()

    def calcular_faltantes(self):
        try:
            D = float(self.entries['Demanda Anual (D)'].get())
            S = float(self.entries['Costo por Pedido (S)'].get())
            H = float(self.entries['Costo de Mantener Inventario (H)'].get())
            P = float(self.entries['Costo por Faltantes (P)'].get())
            DH = float(self.entries['Dias hábiles (DH)'].get())
            CU = float(self.entries['Costo Unitario (CU)'].get())

            Q = math.sqrt(((2 * D * S) / H) * ((H + P) / P))

            S_faltante = Q * (H / (H + P))

            T =(DH* Q) / D

            t1 = T * ((Q-S) / Q)
            t2 = T - t1

            Imax = Q - S_faltante
            Iprom = ((Imax) ** 2)/ 2*Q

            N = D / Q

            CT = ((D / Q) * S )+ (H * ((Q - S_faltante) ** 2) / (2 * Q) )+ (P * ((S_faltante) ** 2) / (2 * Q))

            CI = (D * CU) + CT
         
            resultados = f"""Cantidad óptima de pedido (Q): {Q:.2f}
Faltantes permitidos (S): {S_faltante:.2f}
Tiempo de ciclo entre pedidos (T): {T:.2f}
t1: Tiempo de duración del inventario: {t1:.2f}
t2: Tiempo de escasez: {t2:.2f}
Inventario máximo (Imax): {Imax:.2f}
Inventario promedio (Iprom): {Iprom:.2f}
Número de órdenes por año (N): {N:.2f}
Costo de inversión anual en inventario (CI): {CI:.2f}
Costo total anual (CT): {CT:.2f}
"""
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, resultados)
        
        except ValueError:
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, "Error: Por favor ingresa valores numéricos válidos.")


    #VENTANA DESCUENTOS
    def abrir_descuentos_ventana(self):
        ventana = tk.Toplevel(self)
        ventana.title("Descuentos por Cantidad")
        ventana.geometry("500x300")

        tk.Label(ventana, text="Demanda Anual (D)").grid(row=0, column=0)
        tk.Label(ventana, text="Costo por Pedido (S)").grid(row=1, column=0)
        tk.Label(ventana, text="Agregar Intervalos de Descuento").grid(row=2, column=0)
        
        self.dc_D = tk.Entry(ventana)
        self.dc_S = tk.Entry(ventana)
        
        self.dc_D.grid(row=0, column=1)
        self.dc_S.grid(row=1, column=1)

        self.frame_intervalos = ttk.Frame(ventana)
        self.frame_intervalos.grid(row=3, column=0, columnspan=2)
        
        tk.Label(self.frame_intervalos, text="Cantidad Máxima").grid(row=0, column=0)
        tk.Label(self.frame_intervalos, text="Costo de Mantener (H)").grid(row=0, column=1)

        self.intervalos = []
        
        tk.Button(ventana, text="Agregar Intervalo", command=self.agregar_intervalo).grid(row=4, column=0)
        tk.Button(ventana, text="Calcular Descuentos", command=self.calcular_descuentos).grid(row=4, column=1)
        
        self.dc_resultado = tk.Label(ventana, text="", font=("Arial", 12))
        self.dc_resultado.grid(row=5, column=0, columnspan=2)

    def agregar_intervalo(self):
        fila = len(self.intervalos) + 1  
        
        max_cantidad = tk.Entry(self.frame_intervalos)
        costo_mantener = tk.Entry(self.frame_intervalos)
        
        max_cantidad.grid(row=fila, column=0)
        costo_mantener.grid(row=fila, column=1)

        self.intervalos.append((max_cantidad, costo_mantener))

    def calcular_descuentos(self):
        try:
            D = float(self.dc_D.get()) 
            S = float(self.dc_S.get()) 
            
            mejor_opcion = None
            menor_costo_total = float('inf')

            for max_cantidad_entry, costo_mantener_entry in self.intervalos:
                if max_cantidad_entry.get() == "" or costo_mantener_entry.get() == "":
                    raise ValueError("Uno o más campos de intervalos están vacíos.")
                
                max_cantidad = float(max_cantidad_entry.get())
                costo_mantener = float(costo_mantener_entry.get())

                eoq = calcular_eoq(D, S, costo_mantener)

                costo_total_eoq = ((D / eoq) * S) + ((eoq / 2) * costo_mantener)

                if eoq > max_cantidad:
                    costo_total_max = ((D / max_cantidad) * S) + ((max_cantidad / 2) * costo_mantener)

                    if costo_total_max < costo_total_eoq:
                        costo_total_eoq = costo_total_max 
                        eoq = max_cantidad 

                if costo_total_eoq < menor_costo_total:
                    menor_costo_total = costo_total_eoq
                    mejor_opcion = (eoq, menor_costo_total)

            if mejor_opcion:
                self.dc_resultado.config(text=f"Mejor EOQ: {mejor_opcion[0]:.2f} unidades\nCosto Total: ${mejor_opcion[1]:.2f}")
            else:
                self.dc_resultado.config(text="No se encontró una opción válida")

        except ValueError as e:
            messagebox.showerror("Error", "Por favor, asegúrate de que todos los campos de los intervalos están llenos.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_produccion_economico_ventana(self):
            ventana = tk.Toplevel(self)
            ventana.title("Modelo de Tamaño de Lote de Producción Económico")
            ventana.geometry("400x500")

            # Entradas de datos
            labels = ['Demanda Anual (D)', 'Producción Anual (P)', 'Costo de Producción (C)', 'Costo de Preparación (Co)', 'Tasa de Costos de Retención (I)', 'Días Hábiles (DH)']
            self.entries = {}
            for label in labels:
                tk.Label(ventana, text=label).pack()
                entry = tk.Entry(ventana)
                entry.pack()
                self.entries[label] = entry

            tk.Button(ventana, text="Calcular", command=self.calcular_produccion_economico).pack(pady=10)

            self.resultado_texto = tk.Text(ventana, height=15, width=50)
            self.resultado_texto.pack()

    def calcular_produccion_economico(self):
        try:

            D = float(self.entries['Demanda Anual (D)'].get())
            P = float(self.entries['Producción Anual (P)'].get())
            C = float(self.entries['Costo de Producción (C)'].get())
            Co = float(self.entries['Costo de Preparación (Co)'].get())
            I = float(self.entries['Tasa de Costos de Retención (I)'].get())
            DH = float(self.entries['Días Hábiles (DH)'].get())

            Ch = C * I

            Qp = math.sqrt((2 * D * Co) / (Ch * (1 - D / P)))

            T = DH / (D / Qp )

            t = Qp / (P / DH)

            CT = ((D / Qp) * Co) + ((Qp / 2) * Ch)

            resultados = f"""Coste de retención unitario anual (Ch): {Ch:.2f}
Tamaño óptimo del lote de producción (Qp): {Qp:.2f}
Tiempo de ciclo (T): {T:.2f} años
Tiempo de duración (t): {t:.2f} años
Costo Anual Total (CT): {CT:.2f}
"""
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, resultados)

        except ValueError:
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, "Error: Por favor ingresa valores numéricos válidos.")

   # VENTANA REVISION PERIODICA
    def abrir_revision_periodica_ventana(self):
        ventana = tk.Toplevel(self)
        ventana.title("Modelo de Revisión Periódica con Demanda Probabilística")
        ventana.geometry("400x500")

        labels = ['Demanda Promedio (d)', 'Desviación Estándar', 'Periodo de Revisión (T)', 'Tiempo de Entrega (L)', 'Nivel de Servicio Deseado (z)', 'Inventario Inicial (Io)']
        self.entries = {}
        for label in labels:
            tk.Label(ventana, text=label).pack()
            entry = tk.Entry(ventana)
            entry.pack()
            self.entries[label] = entry

        tk.Button(ventana, text="Calcular", command=self.calcular_revision_periodica).pack(pady=10)

        self.resultado_texto = tk.Text(ventana, height=15, width=50)
        self.resultado_texto.pack()

    def calcular_revision_periodica(self):
        try:

            d = float(self.entries['Demanda Promedio (d)'].get())
            sigma = float(self.entries['Desviación Estándar'].get())
            T = float(self.entries['Periodo de Revisión (T)'].get())
            L = float(self.entries['Tiempo de Entrega (L)'].get())
            z = float(self.entries['Nivel de Servicio Deseado (z)'].get())
            Io = float(self.entries['Inventario Inicial (Io)'].get())

            sigma_total = sigma * math.sqrt(T + L)

            SS = z * sigma_total

            Q = d * (T + L) + SS - Io

            resultados = f"""Desviación Estándar Total: {sigma_total:.2f}
Inventario de Seguridad (SS): {SS:.2f}
Cantidad de Pedido (Q): {Q:.2f}
"""
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, resultados)

        except ValueError:
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, "Error: Por favor ingresa valores numéricos válidos.")
    
#VENTANA INVENTARIO PERIODO UNICO
    def abrir_periodo_unico_ventana(self):
        ventana = tk.Toplevel(self)
        ventana.title("Modelo de Inventario de Periodo Único con Demanda Probabilística")
        ventana.geometry("400x500")

        labels = ['Costo por Faltante (Cs)', 'Costo por Exceso (Ce)', 'Demanda Promedio (d)', 'Desviación Estándar (σ)', 'Nivel de Servicio Deseado (z)']
        self.entries = {}
        for label in labels:
            tk.Label(ventana, text=label).pack()
            entry = tk.Entry(ventana)
            entry.pack()
            self.entries[label] = entry

        tk.Button(ventana, text="Calcular", command=self.calcular_periodo_unico).pack(pady=10)

        self.resultado_texto = tk.Text(ventana, height=15, width=50)
        self.resultado_texto.pack()

    def calcular_periodo_unico(self):
        try:
            Cs = float(self.entries['Costo por Faltante (Cs)'].get())
            Ce = float(self.entries['Costo por Exceso (Ce)'].get())
            d = float(self.entries['Demanda Promedio (d)'].get())
            sigma = float(self.entries['Desviación Estándar (σ)'].get())

            P = Cs / (Cs + Ce)

            z = norm.ppf(P)

            Q = d + z * sigma

            resultados = f"""Nivel de Servicio Óptimo (P): {P:.2f}
Valor Z correspondiente: {z:.2f}
Cantidad Óptima de Pedido (Q): {Q:.2f}
"""
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, resultados)

        except ValueError:
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, "Error: Por favor ingresa valores numéricos válidos.")

# VENTANA DEMANDA PROBABILISTICA
    def abrir_demanda_probabilistica_ventana(self):
        ventana = tk.Toplevel(self)
        ventana.title("Modelo con Demanda y Tiempo de Entrega Probabilístico")
        ventana.geometry("500x500")

        labels = ['Demanda Promedio Diaria (d)', 'Desviación Estándar de la Demanda (σ)', 'Tiempo de Entrega Promedio (L)', 'Desviación Estándar del Tiempo de Entrega (σL)', 'Nivel de Servicio Deseado (z)', 'Inventario Inicial (Io)']
        self.entries = {}
        for label in labels:
            tk.Label(ventana, text=label).pack()
            entry = tk.Entry(ventana)
            entry.pack()
            self.entries[label] = entry

        tk.Button(ventana, text="Calcular", command=self.calcular_demanda_probabilistica).pack(pady=10)

        self.resultado_texto = tk.Text(ventana, height=15, width=50)
        self.resultado_texto.pack()

    def calcular_demanda_probabilistica(self):
        try:
            d = float(self.entries['Demanda Promedio Diaria (d)'].get())
            sigma = float(self.entries['Desviación Estándar de la Demanda (σ)'].get())
            L = float(self.entries['Tiempo de Entrega Promedio (L)'].get())
            sigma_L = float(self.entries['Desviación Estándar del Tiempo de Entrega (σL)'].get())
            z = float(self.entries['Nivel de Servicio Deseado (z)'].get())
            Io = float(self.entries['Inventario Inicial (Io)'].get())

            sigma_T = math.sqrt((L * sigma**2) + (d**2 * sigma_L**2))

            SS = z * sigma_T

            ROP = d * L + SS

            Q = d * L + SS - Io

            resultados = f"""Desviación Estándar Total (σT): {sigma_T:.2f}
Inventario de Seguridad (SS): {SS:.2f}
Punto de Reorden (ROP): {ROP:.2f}
Cantidad de Pedido (Q): {Q:.2f}
"""
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, resultados)

        except ValueError:
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, "Error: Por favor ingresa valores numéricos válidos.")
    # VENTANA VENTAS PERDIDAS
    def abrir_ventas_perdidas_ventana(self):
        ventana = tk.Toplevel(self)
        ventana.title("Modelo con Demanda y Tiempo de Entrega Probabilístico y Ventas Perdidas")
        ventana.geometry("500x600")

        labels = ['Demanda Promedio Diaria (d)', 'Desviación Estándar de la Demanda (σ)', 'Tiempo de Entrega Promedio (L)', 'Desviación Estándar del Tiempo de Entrega (σL)', 'Costo por Faltante (Cs)', 'Costo por Mantener Inventario (Ch)', 'Nivel de Servicio Deseado (z)', 'Inventario Inicial (Io)']
        self.entries = {}
        for label in labels:
            tk.Label(ventana, text=label).pack()
            entry = tk.Entry(ventana)
            entry.pack()
            self.entries[label] = entry

        tk.Button(ventana, text="Calcular", command=self.calcular_ventas_perdidas).pack(pady=10)

        self.resultado_texto = tk.Text(ventana, height=15, width=60)
        self.resultado_texto.pack()

    def calcular_ventas_perdidas(self):
        try:
            d = float(self.entries['Demanda Promedio Diaria (d)'].get())
            sigma = float(self.entries['Desviación Estándar de la Demanda (σ)'].get())
            L = float(self.entries['Tiempo de Entrega Promedio (L)'].get())
            sigma_L = float(self.entries['Desviación Estándar del Tiempo de Entrega (σL)'].get())
            Cs = float(self.entries['Costo por Faltante (Cs)'].get())
            Ch = float(self.entries['Costo por Mantener Inventario (Ch)'].get())
            z = float(self.entries['Nivel de Servicio Deseado (z)'].get())
            Io = float(self.entries['Inventario Inicial (Io)'].get())

            sigma_T = math.sqrt((L * sigma**2) + (d**2 * sigma_L**2))

            P_star = Cs / (Cs + Ch)

            z_optimo = norm.ppf(1 - P_star)

            SS = z_optimo * sigma_T

            ROP = d * L + SS

            Q = d * L + SS - Io

            resultados = f"""Desviación Estándar Total (σT): {sigma_T:.2f}
Probabilidad Óptima de Faltantes (P*): {P_star:.2f}
Valor Z Óptimo (z): {z_optimo:.2f}
Inventario de Seguridad (SS): {SS:.2f}
Punto de Reorden (ROP): {ROP:.2f}
Cantidad de Pedido (Q): {Q:.2f}
"""
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, resultados)

        except ValueError:
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, "Error: Por favor ingresa valores numéricos válidos.")

    # VENTANA PUNTO DE REORDEN
    def abrir_punto_reorden_ventana(self):
        ventana = tk.Toplevel(self)
        ventana.title("Modelo de Punto de Reorden con Demanda Probabilística")
        ventana.geometry("500x400")

        labels = ['Demanda Promedio Diaria (d)', 'Desviación Estándar de la Demanda (σ)', 'Tiempo de Entrega (L)', 'Nivel de Servicio Deseado (z)']
        self.entries = {}
        for label in labels:
            tk.Label(ventana, text=label).pack()
            entry = tk.Entry(ventana)
            entry.pack()
            self.entries[label] = entry

        tk.Button(ventana, text="Calcular", command=self.calcular_punto_reorden).pack(pady=10)

        self.resultado_texto = tk.Text(ventana, height=10, width=50)
        self.resultado_texto.pack()

    def calcular_punto_reorden(self):
        try:

            d = float(self.entries['Demanda Promedio Diaria (d)'].get())
            sigma = float(self.entries['Desviación Estándar de la Demanda (σ)'].get())
            L = float(self.entries['Tiempo de Entrega (L)'].get())
            z = float(self.entries['Nivel de Servicio Deseado (z)'].get())

            sigma_L = sigma * math.sqrt(L)

            SS = z * sigma_L

            ROP = d * L + SS

            resultados = f"""Desviación Estándar durante el Tiempo de Entrega (σL): {sigma_L:.2f}
Inventario de Seguridad (SS): {SS:.2f}
Punto de Reorden (ROP): {ROP:.2f}
"""
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, resultados)

        except ValueError:
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, "Error: Por favor ingresa valores numéricos válidos.")

    #VENTANA ARBOL DE DECISIONES
    def abrir_decision_tree_ventana(self):
        ventana = tk.Toplevel(self)
        ventana.title("Cálculo de VME con Árbol de Decisiones")
        ventana.geometry("600x400")

        tk.Label(ventana, text="Número de escenarios", font=("Helvetica", 12)).grid(row=0, column=0)
        self.num_escenarios = tk.Entry(ventana)
        self.num_escenarios.grid(row=0, column=1)

        tk.Button(ventana, text="Generar campos", command=self.generar_campos).grid(row=1, column=1)

        self.frame_escenarios = ttk.Frame(ventana)
        self.frame_escenarios.grid(row=2, column=0, columnspan=2)

        tk.Button(ventana, text="Calcular VME y Graficar", command=self.calcular_vme).grid(row=3, column=1)

    def generar_campos(self):
        for widget in self.frame_escenarios.winfo_children():
            widget.destroy()

        num_escenarios = int(self.num_escenarios.get())

        self.probabilidades = []
        self.ganancias = []
        self.perdidas = []
        self.costos_adicionales = []  

        tk.Label(self.frame_escenarios, text="Escenario").grid(row=0, column=0)
        tk.Label(self.frame_escenarios, text="Probabilidad").grid(row=0, column=1)
        tk.Label(self.frame_escenarios, text="Ganancia").grid(row=0, column=2)
        tk.Label(self.frame_escenarios, text="Pérdida").grid(row=0, column=3)
        tk.Label(self.frame_escenarios, text="Costo Adicional").grid(row=0, column=4)

        for i in range(num_escenarios):
            tk.Label(self.frame_escenarios, text=f"Escenario {i+1}").grid(row=i+1, column=0)

            probabilidad = tk.Entry(self.frame_escenarios)
            probabilidad.grid(row=i+1, column=1)
            self.probabilidades.append(probabilidad)

            ganancia = tk.Entry(self.frame_escenarios)
            ganancia.grid(row=i+1, column=2)
            self.ganancias.append(ganancia)

            perdida = tk.Entry(self.frame_escenarios)
            perdida.grid(row=i+1, column=3)
            self.perdidas.append(perdida)

            costo = tk.Entry(self.frame_escenarios)
            costo.grid(row=i+1, column=4)
            self.costos_adicionales.append(costo)

    def calcular_vme(self):
        num_escenarios = len(self.probabilidades)
        X = []  
        y = []

        for i in range(num_escenarios):
            probabilidad = float(self.probabilidades[i].get())
            ganancia = float(self.ganancias[i].get())
            perdida = float(self.perdidas[i].get())

            vme = (probabilidad * ganancia) + ((1 - probabilidad) * perdida)

            costo_adicional = self.costos_adicionales[i].get()
            if costo_adicional:
                vme -= float(costo_adicional)

            X.append([probabilidad])
            y.append(vme)

        clf = DecisionTreeRegressor()
        clf = clf.fit(X, y)

        plt.figure(figsize=(10, 7))
        tree.plot_tree(clf, feature_names=["Probabilidad de éxito"], filled=True)
        plt.show()

        mejor_vme = max(y)
        mejor_escenario = y.index(mejor_vme) + 1
        messagebox.showinfo("Mejor opción", f"La mejor opción es el escenario {mejor_escenario} con un VME de {mejor_vme}")

# VENTANA AHP
    def abrir_ahp_ventana(self):
        ventana = tk.Toplevel(self)
        ventana.title("AHP - Análisis de Jerarquía Analítica")
        ventana.geometry("600x400")

        tk.Label(ventana, text="Número de Criterios:").pack()
        self.num_criterios = tk.Entry(ventana)
        self.num_criterios.pack()

        tk.Label(ventana, text="Número de Alternativas:").pack()
        self.num_alternativas = tk.Entry(ventana)
        self.num_alternativas.pack()

        tk.Button(ventana, text="Crear Matrices", command=lambda: self.crear_matrices_criterios(ventana)).pack(pady=10)

    def crear_matrices_criterios(self, ventana):
        try:
            self.n_criterios = int(self.num_criterios.get())
            self.n_alternativas = int(self.num_alternativas.get())
        except ValueError:
            tk.messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")
            return
   
        self.matriz_criterios_entradas = []
        tk.Label(ventana, text="Matriz de Comparación de Criterios:").pack()
        for i in range(self.n_criterios):
            fila = []
            frame_fila = tk.Frame(ventana) 
            frame_fila.pack(pady=2)
            for j in range(self.n_criterios):
                entrada = tk.Entry(frame_fila, width=5)
                entrada.pack(side="left", padx=5)
                fila.append(entrada)
            self.matriz_criterios_entradas.append(fila)

        tk.Button(ventana, text="Crear Matrices de Alternativas", command=lambda: self.crear_matrices_alternativas(ventana)).pack(pady=10)

    def crear_matrices_alternativas(self, ventana):
        self.matrices_alternativas = {}
        for i in range(self.n_criterios):
            tk.Label(ventana, text=f"Matriz de Alternativas para Criterio {i + 1}:").pack()
            matriz_entrada = []
            for r in range(self.n_alternativas):
                frame_fila = tk.Frame(ventana)  
                frame_fila.pack(pady=2)
                fila = []
                for c in range(self.n_alternativas):
                    entrada = tk.Entry(frame_fila, width=5)
                    entrada.pack(side="left", padx=5)
                    fila.append(entrada)
                matriz_entrada.append(fila)
            self.matrices_alternativas[f"criterio_{i+1}"] = matriz_entrada

        tk.Button(ventana, text="Calcular AHP", command=lambda: self.calcular_ahp(ventana)).pack(pady=10)

    def obtener_valores(self, entradas):
        valores = []
        for fila in entradas:
            valores_fila = [float(entrada.get()) for entrada in fila]
            valores.append(valores_fila)
        return np.array(valores)

    def calcular_ahp(self, ventana):
        try:
            matriz_criterios = self.obtener_valores(self.matriz_criterios_entradas)

            ahp_criterios = AHP(matriz_criterios)
            pesos_criterios = ahp_criterios.calculate_weights()

            pesos_alternativas = {}
            for i in range(self.n_criterios):
                matriz_alternativa = self.obtener_valores(self.matrices_alternativas[f"criterio_{i+1}"])
                ahp_alternativa = AHP(matriz_alternativa)
                pesos_alternativas[f"criterio_{i+1}"] = ahp_alternativa.calculate_weights()

            puntuaciones_finales = np.zeros(self.n_alternativas)
            for i in range(self.n_criterios):
                puntuaciones_finales += pesos_alternativas[f"criterio_{i+1}"] * pesos_criterios[i]

            resultado_ventana = tk.Toplevel(ventana)
            resultado_ventana.title("Resultados de AHP")
            tk.Label(resultado_ventana, text="Puntuaciones Finales de las Alternativas:").pack()

            resultado_texto = tk.Text(resultado_ventana, height=10, width=50)
            resultado_texto.pack()
            resultado_texto.insert(tk.END, str(puntuaciones_finales))

        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    class AHP:
        def __init__(self, comparison_matrix):
            self.matrix = comparison_matrix

        def normalize(self):
            column_sums = np.sum(self.matrix, axis=0)
            normalized_matrix = self.matrix / column_sums
            return normalized_matrix

        def calculate_weights(self):
            normalized_matrix = self.normalize()
            weights = np.mean(normalized_matrix, axis=1)
            return weights

    def abrir_decisiones_incertidumbre_ventana(self):
        ventana = tk.Toplevel(self)
        ventana.title("Decisiones Bajo Incertidumbre")

        label_num_disenos = tk.Label(ventana, text="Número de Diseños:")
        label_num_disenos.grid(row=0, column=0)
        self.num_disenos = tk.Entry(ventana)
        self.num_disenos.grid(row=0, column=1)

        label_num_escenarios = tk.Label(ventana, text="Número de Escenarios:")
        label_num_escenarios.grid(row=1, column=0)
        self.num_escenarios = tk.Entry(ventana)
        self.num_escenarios.grid(row=1, column=1)

        def crear_campos_beneficios():
            try:
                n_disenos = int(self.num_disenos.get())
                n_escenarios = int(self.num_escenarios.get())
            except ValueError:
                tk.messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")
                return

            self.beneficios_entradas = []
            for i in range(n_disenos):
                fila = []
                for j in range(n_escenarios):
                    entrada = tk.Entry(ventana, width=10)
                    entrada.grid(row=i + 3, column=j)
                    fila.append(entrada)
                self.beneficios_entradas.append(fila)

            tk.Button(ventana, text="Criterio Optimista", command=lambda: self.calcular_optimista()).grid(row=n_disenos + 4, column=0)
            tk.Button(ventana, text="Criterio Pesimista", command=lambda: self.calcular_pesimista()).grid(row=n_disenos + 4, column=1)
            tk.Button(ventana, text="Criterio Laplace", command=lambda: self.calcular_laplace()).grid(row=n_disenos + 4, column=2)
            tk.Button(ventana, text="Criterio Hurwicz", command=lambda: self.calcular_hurwicz()).grid(row=n_disenos + 5, column=0)
            tk.Button(ventana, text="Criterio Savage", command=lambda: self.calcular_savage()).grid(row=n_disenos + 5, column=1)

            self.resultado = tk.Text(ventana, height=10, width=50)
            self.resultado.grid(row=n_disenos + 6, column=0, columnspan=3)

        tk.Button(ventana, text="Crear Campos", command=crear_campos_beneficios).grid(row=2, column=0, columnspan=2)

    def obtener_beneficios(self):
        beneficios = []
        for fila in self.beneficios_entradas:
            beneficios_fila = [float(entrada.get()) for entrada in fila]
            beneficios.append(beneficios_fila)
        return np.array(beneficios)

    def calcular_optimista(self):
        beneficios = self.obtener_beneficios()
        resultado = criterio_optimista(beneficios)
        self.mostrar_resultado("Criterio Optimista", resultado)

    def calcular_pesimista(self):
        beneficios = self.obtener_beneficios()
        resultado = criterio_pesimista(beneficios)
        self.mostrar_resultado("Criterio Pesimista", resultado)

    def calcular_laplace(self):
        beneficios = self.obtener_beneficios()
        resultado = criterio_laplace(beneficios)
        self.mostrar_resultado("Criterio Laplace", resultado)

    def calcular_hurwicz(self):
        beneficios = self.obtener_beneficios()
        resultado = criterio_hurwicz(beneficios)
        self.mostrar_resultado("Criterio Hurwicz", resultado)

    def calcular_savage(self):
        beneficios = self.obtener_beneficios()
        resultado = criterio_savage(beneficios)
        self.mostrar_resultado("Criterio Savage", resultado)

    def mostrar_resultado(self, criterio, resultado):
        self.resultado.delete(1.0, tk.END)
        self.resultado.insert(tk.END, f"{criterio} - Resultados por diseño: {resultado}\n")

def criterio_optimista(beneficios):
    return np.max(beneficios, axis=1)

def criterio_pesimista(beneficios):
    return np.min(beneficios, axis=1)

def criterio_laplace(beneficios):
    return np.mean(beneficios, axis=1)

def criterio_hurwicz(beneficios, alfa=0.65):
    maximos = np.max(beneficios, axis=1)
    minimos = np.min(beneficios, axis=1)
    return alfa * maximos + (1 - alfa) * minimos

def criterio_savage(beneficios):
    regret = np.max(beneficios, axis=0) - beneficios
    return np.max(regret, axis=1)


if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
