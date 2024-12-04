import tkinter as tk
from tkinter import messagebox
import cvxpy as cp
import numpy as np

class ProgramacionGeometricaVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Programación Geométrica")
        self.geometry("700x500")

        self.variables_frame = tk.Frame(self)
        self.variables_frame.pack(pady=10)

        tk.Label(self.variables_frame, text="Número de variables:").grid(row=0, column=0, padx=5, pady=5)
        self.num_variables_entry = tk.Entry(self.variables_frame)
        self.num_variables_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self, text="Configurar Variables", command=self.configurar_variables).pack(pady=20)

        self.obj_funcion = None  # Para la función objetivo
        self.restricciones = None  # Para las restricciones
        self.num_variables = 0  # Número de variables

    def configurar_variables(self):
        try:
            self.num_variables = int(self.num_variables_entry.get())
            if self.num_variables < 1:
                raise ValueError

            for widget in self.winfo_children():
                widget.pack_forget()

            # Campo para la función objetivo
            tk.Label(self, text="Ingrese la función objetivo:").pack(pady=10)
            self.obj_funcion_entry = tk.Entry(self)
            self.obj_funcion_entry.pack(pady=5)

            # Campo para las restricciones
            tk.Label(self, text="Ingrese las restricciones:").pack(pady=10)
            self.restricciones_entry = tk.Entry(self)
            self.restricciones_entry.pack(pady=5)

            tk.Button(self, text="Resolver", command=self.resolver).pack(pady=20)

        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido de variables.")

    def resolver(self):
        try:
            # Obtener la función objetivo desde el campo de texto
            func_obj_str = self.obj_funcion_entry.get()
            restricciones_str = self.restricciones_entry.get()

            # Crear variables de optimización
            x = cp.Variable(self.num_variables)

            # Evaluar la función objetivo, asumiendo una forma matemática válida
            try:
                # Convertir la cadena de la función objetivo en una expresión matemática válida
                func_obj = eval(func_obj_str)
            except Exception as e:
                messagebox.showerror("Error", f"Error en la función objetivo: {e}")
                return

            # Evaluar las restricciones (asumimos que las restricciones están separadas por ';')
            restricciones = []
            try:
                restricciones_lista = restricciones_str.split(';')
                for restriccion in restricciones_lista:
                    restriccion = restriccion.strip()
                    if restriccion:
                        restricciones.append(eval(restriccion))
            except Exception as e:
                messagebox.showerror("Error", f"Error en las restricciones: {e}")
                return

            # Crear el problema de optimización
            objetivo = cp.Maximize(func_obj)
            problema = cp.Problem(objetivo, restricciones)
            resultado = problema.solve()

            # Mostrar el resultado
            if resultado is not None:
                solucion = x.value
                resultado_texto = f"Valor óptimo de la función objetivo: {resultado:.2f}\nSolución óptima: {solucion}"
                messagebox.showinfo("Resultado", resultado_texto)
            else:
                messagebox.showerror("Error", "No se pudo resolver el problema.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al resolver el problema: {e}")
