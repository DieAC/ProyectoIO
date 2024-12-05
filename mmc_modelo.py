import tkinter as tk
from tkinter import messagebox

class MMCVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Modelo M/M/c")
        self.geometry("400x800")
        
        tk.Label(self, text="Número de servidores (c):").pack(pady=5)
        self.servers_entry = tk.Entry(self)
        self.servers_entry.pack(pady=5)
        
        tk.Label(self, text="Ratio de servicios (μ):").pack(pady=5)
        self.mu_entry = tk.Entry(self)
        self.mu_entry.pack(pady=5)
        
        tk.Label(self, text="Ratio de llegadas (λ):").pack(pady=5)
        self.lambda_entry = tk.Entry(self)
        self.lambda_entry.pack(pady=5)
        
        tk.Button(self, text="Calcular", command=self.calcular).pack(pady=20)
        
        self.resultados = tk.Text(self, height=10, width=50, state="disabled")
        self.resultados.pack(pady=30)
        
        tk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)

    def calcular(self):
        try:
            c = int(self.servers_entry.get()) 
            mu = float(self.mu_entry.get())    
            lam = float(self.lambda_entry.get())
            
            if lam >= mu * c:
                messagebox.showerror("Error", "λ debe ser menor que μ * c para que el sistema sea estable.")
                return
            
            P0 = self.calcular_P0(lam, mu, c)
            rho = lam / (mu * c)
            Lq = (P0 * ((lam / mu) ** c) * rho) / (self.factorial(c) * ((1 - rho) ** 2))
            L = Lq + (lam / mu)
            Wq = Lq / lam
            W = Wq + 1 / mu
            
            resultados_texto = (
                f"Resultados:\n"
                f"Utilización del servidor (ρ): {rho:.4f}\n"
                f"Probabilidad de que no haya unidades en el sistema (ρ0): {P0:.4f}\n"
                f"Número promedio de clientes en la cola (Lq): {Lq:.4f}\n"
                f"Número promedio de clientes en el sistema (L): {L:.4f}\n"
                f"Tiempo promedio en la cola (Wq): {Wq:.4f}\n"
                f"Tiempo promedio en el sistema (W): {W:.4f}\n"
            )
            self.resultados.config(state="normal")
            self.resultados.delete("1.0", tk.END)
            self.resultados.insert(tk.END, resultados_texto)
            self.resultados.config(state="disabled")
        
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")
    
    def calcular_P0(self, lam, mu, c):
        """Método para calcular la probabilidad de que el sistema esté vacío (P0)."""
        factor = self.factor_c(c, lam, mu)
        P0 = 1 / factor
        return P0

    def factor_c(self, c, lam, mu):
        """Calcula el factor que ayuda a obtener P0 y otros parámetros."""
        sumatoria = sum([((lam / mu) ** n )/ self.factorial(n) for n in range(c)])
        factor_c = sumatoria + ((((lam / mu) ** c) / (self.factorial(c))) * (1 /(1- (lam / (mu * c)))))
        return factor_c

    def factorial(self, n):
        """Método para calcular el factorial de un número."""
        if n == 0 or n == 1:
            return 1
        return n * self.factorial(n - 1)