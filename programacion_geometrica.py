import tkinter as tk
from tkinter import messagebox
import cvxpy as cp

class ProgramacionGeometricaVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Programación Geométrica")
        self.geometry("700x500")

        self.func_objetivo_label = tk.Label(self, text="Ingrese los coeficientes de la función objetivo:")
        self.func_objetivo_label.pack(pady=10)

        self.coef_lineales_label = tk.Label(self, text="Coeficientes lineales:")
        self.coef_lineales_label.pack(pady=5)

        self.coef_lineales_entry = tk.Entry(self, width=50)
        self.coef_lineales_entry.pack(pady=5)

        self.coef_cuadraticos_label = tk.Label(self, text="Coeficientes cuadráticos:")
        self.coef_cuadraticos_label.pack(pady=5)

        self.coef_cuadraticos_entry = tk.Entry(self, width=50)
        self.coef_cuadraticos_entry.pack(pady=5)

        self.restricciones_label = tk.Label(self, text="Ingrese las restricciones:")
        self.restricciones_label.pack(pady=10)

        self.restricciones_entries = []

        self.agregar_restriccion_button = tk.Button(self, text="Agregar Restricción", command=self.agregar_restriccion)
        self.agregar_restriccion_button.pack(pady=10)

        self.resolver_button = tk.Button(self, text="Resolver", command=self.resolver)
        self.resolver_button.pack(pady=20)

    def agregar_restriccion(self):
        restriccion_frame = tk.Frame(self)
        restriccion_frame.pack(pady=5)

        tk.Label(restriccion_frame, text="Coeficientes:").grid(row=0, column=0)
        coef_entry = tk.Entry(restriccion_frame, width=30)
        coef_entry.grid(row=0, column=1)

        tk.Label(restriccion_frame, text="Constante:").grid(row=0, column=2)
        constante_entry = tk.Entry(restriccion_frame, width=10)
        constante_entry.grid(row=0, column=3)

        tk.Label(restriccion_frame, text="Tipo (<=, >=, =):").grid(row=0, column=4)
        tipo_entry = tk.Entry(restriccion_frame, width=10)
        tipo_entry.grid(row=0, column=5)

        self.restricciones_entries.append((coef_entry, constante_entry, tipo_entry))

    def resolver(self):
        try:
            coef_lineales = self.coef_lineales_entry.get().strip()
            coef_cuadraticos = self.coef_cuadraticos_entry.get().strip()
    
            if not coef_lineales or not coef_cuadraticos:
                messagebox.showerror("Error", "Por favor, ingrese todos los campos de la función objetivo.")
                return

            try:
                coef_lineales = list(map(float, coef_lineales.split(','))) 
                coef_cuadraticos = list(map(float, coef_cuadraticos.split(',')))  
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para los coeficientes.")
                return

            num_variables = len(coef_lineales)

            x = cp.Variable(num_variables, nonneg=True)

            lambda_penalizacion = 100 

            Z = sum(coef_lineales[i] * x[i] for i in range(num_variables)) + sum(coef_cuadraticos[i] * (x[i]**2) for i in range(num_variables)) - lambda_penalizacion * (x[1] - 1.089)**2

            restricciones = []
            for coef_entry, constante_entry, tipo_entry in self.restricciones_entries:
                coef_str = coef_entry.get().strip()
                constante_str = constante_entry.get().strip()
                tipo_restriccion = tipo_entry.get().strip().lower()

                if not coef_str or not constante_str or not tipo_restriccion:
                    messagebox.showerror("Error", "Por favor, complete todos los campos de las restricciones.")
                    return

                try:
                    coef = list(map(float, coef_str.split(',')))  
                    constante = float(constante_str)
                except ValueError:
                    messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para los coeficientes y la constante.")
                    return

                if tipo_restriccion == "=":
                    restricciones.append(cp.sum([coef[i] * x[i] for i in range(num_variables)]) == constante)
                elif tipo_restriccion == "<=":
                    restricciones.append(cp.sum([coef[i] * x[i] for i in range(num_variables)]) <= constante)
                elif tipo_restriccion == ">=":
                    restricciones.append(cp.sum([coef[i] * x[i] for i in range(num_variables)]) >= constante)
                else:
                    messagebox.showerror("Error", "El tipo de restricción debe ser <=, >= o =.")
                    return

            problema = cp.Problem(cp.Maximize(Z), restricciones)

            resultado = problema.solve()

            if resultado is not None:
                solucion = [round(val, 3) for val in x.value]
                resultado_texto = f"Valor óptimo de Z: {resultado:.2f}\nSolución óptima: {solucion}"
                messagebox.showinfo("Resultado", resultado_texto)
            else:
                messagebox.showerror("Error", "No se pudo resolver el problema.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al resolver el problema: {e}")

