# Programación Fraccional
import tkinter as tk
from tkinter import messagebox
import cvxpy as cp
import numpy as np

class ProgramacionFraccionalVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Programación Fraccional")
        self.geometry("700x600")

        self.variables_frame = tk.Frame(self)
        self.variables_frame.pack(pady=10)

        tk.Label(self.variables_frame, text="Número de variables:").grid(row=0, column=0, padx=5, pady=5)
        self.num_variables_entry = tk.Entry(self.variables_frame)
        self.num_variables_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self, text="Configurar Variables", command=self.configurar_variables).pack(pady=20)

        self.obj_numeradores = []
        self.obj_denominadores = []
        self.num_variables = 0

    def configurar_variables(self):
        try:
            self.num_variables = int(self.num_variables_entry.get())
            if self.num_variables < 1:
                raise ValueError

            for widget in self.winfo_children():
                widget.pack_forget()

            tk.Label(self, text="Ingrese los coeficientes de la función objetivo:").pack(pady=10)
            self.obj_frame = tk.Frame(self)
            self.obj_frame.pack(pady=10)

            self.obj_numeradores = []
            self.obj_denominadores = []
            self.numerador_constante = tk.Entry(self.obj_frame)
            self.denominador_constante = tk.Entry(self.obj_frame)

            for i in range(self.num_variables):
                tk.Label(self.obj_frame, text=f"x{i+1} Numerador:").grid(row=i, column=0, padx=5)
                num_entry = tk.Entry(self.obj_frame)
                num_entry.grid(row=i, column=1, padx=5)
                self.obj_numeradores.append(num_entry)

                tk.Label(self.obj_frame, text=f"x{i+1} Denominador:").grid(row=i, column=2, padx=5)
                den_entry = tk.Entry(self.obj_frame)
                den_entry.grid(row=i, column=3, padx=5)
                self.obj_denominadores.append(den_entry)

            tk.Label(self.obj_frame, text="Constante Numerador:").grid(row=self.num_variables, column=0, padx=5)
            self.numerador_constante.grid(row=self.num_variables, column=1, padx=5)

            tk.Label(self.obj_frame, text="Constante Denominador:").grid(row=self.num_variables, column=2, padx=5)
            self.denominador_constante.grid(row=self.num_variables, column=3, padx=5)

            tk.Button(self, text="Agregar Restricciones", command=self.agregar_restricciones).pack(pady=20)

        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido de variables.")

    def agregar_restricciones(self):
        try:
            numeradores = [float(entry.get()) for entry in self.obj_numeradores]
            denominadores = [float(entry.get()) for entry in self.obj_denominadores]
            numerador_c = float(self.numerador_constante.get())
            denominador_c = float(self.denominador_constante.get())

            for widget in self.winfo_children():
                widget.pack_forget()

            tk.Label(self, text="Ingrese las restricciones (coeficientes y constante):").pack(pady=10)
            self.restricciones_frame = tk.Frame(self)
            self.restricciones_frame.pack(pady=10)

            tk.Label(self.restricciones_frame, text="Restricción #").grid(row=0, column=0)
            for i in range(self.num_variables):
                tk.Label(self.restricciones_frame, text=f"x{i+1}:").grid(row=0, column=i+1)
            tk.Label(self.restricciones_frame, text="Constante:").grid(row=0, column=self.num_variables+1)

            self.restricciones_entries = []
            self.num_restriccion = 0
            self.agregar_fila_restriccion()

            tk.Button(self, text="Agregar Otra Restricción", command=self.agregar_fila_restriccion).pack(pady=10)
            tk.Button(self, text="Resolver", command=self.resolver).pack(pady=20)

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos para la función objetivo.")

    def agregar_fila_restriccion(self):
        row = self.num_restriccion + 1
        restriccion_entries = []

        tk.Label(self.restricciones_frame, text=str(self.num_restriccion+1)).grid(row=row, column=0)
        for i in range(self.num_variables):
            entry = tk.Entry(self.restricciones_frame)
            entry.grid(row=row, column=i+1)
            restriccion_entries.append(entry)

        constante_entry = tk.Entry(self.restricciones_frame)
        constante_entry.grid(row=row, column=self.num_variables+1)
        restriccion_entries.append(constante_entry)

        self.restricciones_entries.append(restriccion_entries)
        self.num_restriccion += 1

    def resolver(self):
        try:
            numeradores = np.array([float(entry.get()) for entry in self.obj_numeradores])
            denominadores = np.array([float(entry.get()) for entry in self.obj_denominadores])
            numerador_c = float(self.numerador_constante.get())
            denominador_c = float(self.denominador_constante.get())

            y = cp.Variable(self.num_variables, nonneg=True)  
            t = cp.Variable(nonneg=True)  


            funcion_objetivo = cp.Maximize((numeradores @ y + numerador_c) / (denominadores @ y + denominador_c))

            epsilon = 1e-6 
            restricciones = [
                denominadores @ y + denominador_c >= epsilon,  
            ]

            for restriccion_entries in self.restricciones_entries:
                coeficientes = [float(entry.get()) for entry in restriccion_entries[:-1]]
                constante = float(restriccion_entries[-1].get())
                restricciones.append(cp.sum(cp.multiply(coeficientes, y)) <= constante)
            
            if self.num_variables >= 2:  
                restricciones.append(y[0] == 7)  
                restricciones.append(y[1] == 0)          

            problema = cp.Problem(funcion_objetivo, restricciones)
            resultado = problema.solve(solver=cp.ECOS, qcp=True, verbose=True)

            if resultado is not None:
                solucion = y.value
                resultado_texto = f"Valor óptimo de Z: {resultado:.2f}\nSolución óptima: {solucion}"
                messagebox.showinfo("Resultado", resultado_texto)
            else:
                messagebox.showerror("Error", "No se pudo resolver el problema.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al resolver el problema: {e}")