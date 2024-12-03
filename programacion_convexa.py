import tkinter as tk
from tkinter import messagebox
import cvxpy as cp
import numpy as np
import ast

class ProgramacionConvexaVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Programación Convexa")
        self.geometry("700x500")

        self.num_variables = 0
        self.obj_lineales = []
        self.obj_cuadraticos = []
        self.restricciones_entries = []
        self.num_restriccion = 0

        self.variables_frame = tk.Frame(self)
        self.variables_frame.pack(pady=10)
        tk.Label(self.variables_frame, text="Número de variables:").grid(row=0, column=0, padx=5, pady=5)
        self.num_variables_entry = tk.Entry(self.variables_frame)
        self.num_variables_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="Configurar Variables", command=self.configurar_variables).pack(pady=20)

    def validar_entrada(self, entrada):
        try:
            return float(entrada.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido.")
            raise ValueError("Entrada inválida")

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

            self.obj_lineales = []
            self.obj_cuadraticos = []
            for i in range(self.num_variables):
                tk.Label(self.obj_frame, text=f"x{i+1} (lineal):").grid(row=i, column=0, padx=5)
                linear_entry = tk.Entry(self.obj_frame)
                linear_entry.grid(row=i, column=1, padx=5)
                self.obj_lineales.append(linear_entry)

                tk.Label(self.obj_frame, text=f"x{i+1}^2 (cuadrático):").grid(row=i, column=2, padx=5)
                quad_entry = tk.Entry(self.obj_frame)
                quad_entry.grid(row=i, column=3, padx=5)
                self.obj_cuadraticos.append(quad_entry)

            tk.Button(self, text="Agregar Restricciones", command=self.agregar_restricciones).pack(pady=20)

        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido de variables.")

    def agregar_restricciones(self):
        try:
            self.lineales = [self.validar_entrada(entry) for entry in self.obj_lineales]
            self.cuadraticos = [self.validar_entrada(entry) for entry in self.obj_cuadraticos]

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
            P = np.diag(self.cuadraticos)
            q = np.array(self.lineales)

            restricciones = []
            constantes = []
            for restriccion in self.restricciones_entries:
                coeficientes = [float(entry.get()) for entry in restriccion[:-1]]
                constante = float(restriccion[-1].get())
                restricciones.append(coeficientes)
                constantes.append(constante)

            variables = cp.Variable(self.num_variables)
            objetivo = cp.Minimize(0.5 * cp.quad_form(variables, P) + q @ variables)

            restricciones_cp = [
                sum(restricciones[i][j] * variables[j] for j in range(self.num_variables)) == constantes[i]
                for i in range(len(restricciones))
            ]
            restricciones_cp += [variables >= 0]

            problema = cp.Problem(objetivo, restricciones_cp)
            resultado = problema.solve()

            solucion = variables.value
            resultado_texto = f"Valor óptimo de Z: {resultado:.2f}\nSolución óptima: {solucion}"
            messagebox.showinfo("Resultado", resultado_texto)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al resolver el problema: {e}")


