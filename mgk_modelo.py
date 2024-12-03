import tkinter as tk
from tkinter import messagebox
from math import factorial

class MGKVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Modelo M/G/K")
        self.geometry("400x500")
        
        # Etiquetas y entradas
        tk.Label(self, text="Tasa de llegada (λ):").pack(pady=5)
        self.lambda_entry = tk.Entry(self)
        self.lambda_entry.pack(pady=5)
        
        tk.Label(self, text="Tasa de servicio promedio (μ):").pack(pady=5)
        self.mu_entry = tk.Entry(self)
        self.mu_entry.pack(pady=5)
        
        tk.Label(self, text="Número de servidores (k):").pack(pady=5)
        self.k_entry = tk.Entry(self)
        self.k_entry.pack(pady=5)
        
        # Botón para calcular
        tk.Button(self, text="Calcular", command=self.calcular).pack(pady=20)
        
        # Área de resultados
        self.resultados = tk.Text(self, height=15, width=50, state="disabled")
        self.resultados.pack(pady=10)
        
        # Botón para cerrar
        tk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)

    def calcular(self):
        try:
            lam = float(self.lambda_entry.get())  # λ
            mu = float(self.mu_entry.get())      # μ
            k = int(self.k_entry.get())          # k (número de servidores)
            
            if lam <= 0 or mu <= 0 or k <= 0:
                messagebox.showerror("Error", "Todos los valores deben ser positivos.")
                return
            
            rho = lam / (k * mu)  # Utilización del sistema
            
            if rho >= 1:
                messagebox.showerror("Error", "El sistema no es estable (ρ debe ser menor a 1).")
                return
            
            # Cálculo de la sumatoria para normalizar probabilidades
            suma = sum((lam / mu) ** i / factorial(i) for i in range(k))
            pk = ((lam / mu) ** k / factorial(k)) / (suma)

            # Cálculo de Pj para j = 0 hasta k
            probabilidades = []
            for j in range(k + 1):
                pj = ((lam / mu) ** j / factorial(j)) / (suma)
                probabilidades.append(f"P({j}) = {pj:.4f}")

            # Número promedio de clientes en el sistema (L)
            L = (lam / mu) * (1 - pk)

            # Mostrar resultados
            resultados_texto = "\n".join(probabilidades)
            resultados_texto += f"\n\nNúmero promedio de clientes en el sistema (L): {L:.4f}\n"
            resultados_texto += f"Probabilidad de que todas las líneas estén ocupadas (P_k): {pk:.4f}\n"
            
            self.resultados.config(state="normal")
            self.resultados.delete("1.0", tk.END)
            self.resultados.insert(tk.END, resultados_texto)
            self.resultados.config(state="disabled")
        
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos.")
