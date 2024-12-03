import tkinter as tk
from tkinter import messagebox
from scipy.optimize import minimize
import numpy as np

class ProgramacionNoConvexaVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Programación No Convexa")
        self.geometry("700x500")

        # Configuración inicial
        tk.Label(self, text="Número de variables:").pack(pady=10)
        self.num_variables_entry = tk.Entry(self)
        self.num_variables_entry.pack(pady=5)

        tk.Button(self, text="Configurar Variables", command=self.configurar_variables).pack(pady=20)

    def configurar_variables(self):
        try:
            self.num_variables = int(self.num_variables_entry.get())
            if self.num_variables < 1:
                raise ValueError("El número de variables debe ser mayor que cero.")

            # Limpiar ventana
            for widget in self.winfo_children():
                widget.pack_forget()

            # Configurar función objetivo
            tk.Label(self, text="Ingrese la función objetivo (en términos de x0, x1, ...):").pack(pady=10)
            self.func_objetivo_entry = tk.Entry(self, width=50)
            self.func_objetivo_entry.pack(pady=5)

            tk.Button(self, text="Agregar Restricciones", command=self.agregar_restricciones).pack(pady=20)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def agregar_restricciones(self):
        try:
            self.obj_funcion = self.func_objetivo_entry.get()
            if not self.obj_funcion:
                raise ValueError("Debe ingresar una función objetivo.")

            for widget in self.winfo_children():
                widget.pack_forget()

            # Configurar restricciones
            tk.Label(self, text="Ingrese las restricciones (en términos de x0, x1, ...):").pack(pady=10)
            self.restricciones_frame = tk.Frame(self)
            self.restricciones_frame.pack(pady=10)

            self.restricciones_entries = []
            self.agregar_fila_restriccion()

            tk.Button(self, text="Agregar Otra Restricción", command=self.agregar_fila_restriccion).pack(pady=10)
            tk.Button(self, text="Resolver", command=self.resolver).pack(pady=20)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def agregar_fila_restriccion(self):
        row = len(self.restricciones_entries)
        restriccion_entry = tk.Entry(self.restricciones_frame, width=50)
        restriccion_entry.grid(row=row, column=0, padx=5, pady=5)
        self.restricciones_entries.append(restriccion_entry)

    def resolver(self):
        try:
            # Definir función objetivo
            def funcion_objetivo(x):
                return eval(self.obj_funcion)

            # Definir restricciones
            restricciones = []
            for restriccion_entry in self.restricciones_entries:
                restriccion_texto = restriccion_entry.get()
                if restriccion_texto:
                    restricciones.append({
                        'type': 'ineq',
                        'fun': lambda x, expr=restriccion_texto: eval(expr)
                    })

            # Valores iniciales
            x0 = np.zeros(self.num_variables)

            # Resolver problema
            resultado = minimize(funcion_objetivo, x0, constraints=restricciones)

            if resultado.success:
                solucion = resultado.x
                valor_objetivo = resultado.fun
                messagebox.showinfo("Resultado", f"Valor óptimo: {valor_objetivo}\nSolución: {solucion}")
            else:
                messagebox.showerror("Error", "No se encontró solución óptima.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver el problema: {e}")

