#mm1_modelo.py
import tkinter as tk
from tkinter import messagebox

class MM1Ventana(tk.Toplevel):
    def __init__(self, parent): 
        super().__init__(parent) 
        self.title("Modelo M/M/1")
        self.geometry("400x400")
        
        tk.Label(self, text="Ratio de servicios (μ):").pack(pady=5)
        self.mu_entry = tk.Entry(self)
        self.mu_entry.pack(pady=5)
        
        tk.Label(self, text="Ratio de llegadas (λ):").pack(pady=5)
        self.lambda_entry = tk.Entry(self)
        self.lambda_entry.pack(pady=5)
        
        tk.Button(self, text="Calcular", command=self.calcular).pack(pady=20)
        
        self.resultados = tk.Text(self, height=10, width=50, state="disabled")
        self.resultados.pack(pady=10)
        
        tk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)

    def calcular(self):
        try:
            mu = float(self.mu_entry.get())
            lam = float(self.lambda_entry.get())
            
            if lam >= mu:
                messagebox.showerror("Error", "λ debe ser menor que μ para que el sistema sea estable.")
                return
            
            rho = lam / mu
            p0 = 1 - rho
            lq = (rho ** 2) / (1 - rho)
            wq = lq / lam
            l = lam / (mu - lam)
            w = l / lam
            
            resultados_texto = (
                f"Resultados:\n"
                f"Utilización del servidor (ρ): {rho:.4f}\n"
                f"Probabilidad de que no haya unidades en el sistema (p0): {p0:.4f}\n"
                f"Número promedio de clientes en la cola (Lq): {lq:.4f}\n"
                f"Número promedio de clientes en el sistema (L): {l:.4f}\n"
                f"Tiempo promedio en la cola (Wq): {wq:.4f}\n"
                f"Tiempo promedio en el sistema (W): {w:.4f}\n"
            )
            self.resultados.config(state="normal")
            self.resultados.delete("1.0", tk.END)
            self.resultados.insert(tk.END, resultados_texto)
            self.resultados.config(state="disabled")
        
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")