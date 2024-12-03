import tkinter as tk
from tkinter import messagebox
import cvxpy as cp
import sympy as sp

class ProgramacionSeparableVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Programación Separable")
        self.geometry("700x600")

        self.variables_frame = tk.Frame(self)
        self.variables_frame.pack(pady=10)

        tk.Label(self.variables_frame, text="Número de variables:").grid(row=0, column=0, padx=5, pady=5)
        self.num_variables_entry = tk.Entry(self.variables_frame)
        self.num_variables_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self, text="Configurar Variables", command=self.configurar_variables).pack(pady=20)

        self.num_variables = 0
        self.obj_func_entries = []
        self.restricciones_entries = []
        self.num_restriccion = 0

    def configurar_variables(self):
        try:
            self.num_variables = int(self.num_variables_entry.get())
            if self.num_variables < 1:
                raise ValueError("El número de variables debe ser al menos 1.")

            for widget in self.winfo_children():
                widget.pack_forget()

            tk.Label(self, text="Ingrese las funciones separables de la función objetivo:").pack(pady=10)

            self.obj_frame = tk.Frame(self)
            self.obj_frame.pack(pady=10)
            self.obj_func_entries = []

            for i in range(self.num_variables):
                tk.Label(self.obj_frame, text=f"f(x{i + 1}):").grid(row=i, column=0, padx=5, pady=5)
                entry = tk.Entry(self.obj_frame)
                entry.grid(row=i, column=1, padx=5, pady=5)
                self.obj_func_entries.append(entry)

            tk.Button(self, text="Agregar Restricciones", command=self.agregar_restricciones).pack(pady=20)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def agregar_restricciones(self):
        try:
            for widget in self.winfo_children():
                widget.pack_forget()

            tk.Label(self, text="Ingrese las restricciones (coeficientes y constante):").pack(pady=10)

            self.restricciones_frame = tk.Frame(self)
            self.restricciones_frame.pack(pady=10)

            self.restricciones_entries = []
            self.num_restriccion = 0
            self.agregar_fila_restriccion()

            tk.Button(self, text="Agregar Otra Restricción", command=self.agregar_fila_restriccion).pack(pady=10)
            tk.Button(self, text="Resolver", command=self.resolver).pack(pady=20)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def agregar_fila_restriccion(self):
        row = self.num_restriccion + 1
        tk.Label(self.restricciones_frame, text=f"Restricción {self.num_restriccion + 1}").grid(row=row, column=0, padx=5)

        restriccion_entries = []
        for i in range(self.num_variables):
            entry = tk.Entry(self.restricciones_frame)
            entry.grid(row=row, column=i + 1, padx=5)
            restriccion_entries.append(entry)

        constante_entry = tk.Entry(self.restricciones_frame)
        constante_entry.grid(row=row, column=self.num_variables + 1, padx=5)
        restriccion_entries.append(constante_entry)

        self.restricciones_entries.append(restriccion_entries)
        self.num_restriccion += 1

    def resolver(self):
        try:
            from sympy import symbols, sympify, Eq, solve

            # Crear variables simbólicas
            x = symbols(f"x1:{self.num_variables + 1}")  # Crear variables x1, x2, ..., xn

            # Crear función objetivo como suma de funciones separables
            funciones_objetivo = []
            for i, entry in enumerate(self.obj_func_entries):
                funcion = sympify(entry.get())  # Convertir la entrada de texto a expresión simbólica
                funciones_objetivo.append(funcion)

            objetivo = sum(funciones_objetivo)

            # Derivar la función objetivo respecto a cada variable para encontrar puntos críticos
            derivadas = [objetivo.diff(var) for var in x]
            solucion_critica = solve(derivadas, x)

            # Verificar si la solución cumple las restricciones
            restricciones = []
            for restriccion_entries in self.restricciones_entries:
                coeficientes = [float(entry.get()) for entry in restriccion_entries[:-1]]
                constante = float(restriccion_entries[-1].get())
                restriccion = sum(coef * x_var for coef, x_var in zip(coeficientes, x)) - constante
                restricciones.append(restriccion)

            # Evaluar si las restricciones se cumplen
            solucion_valida = all(restriccion.subs(solucion_critica) <= 0 for restriccion in restricciones)

            # Mostrar resultados
            if solucion_valida:
                resultado_texto = f"Valor óptimo de Z: {objetivo.subs(solucion_critica):.2f}\n"
                resultado_texto += "\n".join(f"{var}: {valor}" for var, valor in solucion_critica.items())
                messagebox.showinfo("Resultado", resultado_texto)
            else:
                messagebox.showerror("Error", "La solución óptima no cumple con las restricciones.")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al resolver el problema: {e}")

