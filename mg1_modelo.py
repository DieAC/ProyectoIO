import tkinter as tk
from tkinter import messagebox

class MG1Ventana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Modelo M/G/1")
        self.geometry("400x500")
        
        # Etiquetas y entradas
        tk.Label(self, text="Ratio de llegadas (λ):").pack(pady=5)
        self.lambda_entry = tk.Entry(self)
        self.lambda_entry.pack(pady=5)
        
        tk.Label(self, text="Ratio de servicio (μ):").pack(pady=5)
        self.mu_entry = tk.Entry(self)
        self.mu_entry.pack(pady=5)
        
        tk.Label(self, text="Varianza del tiempo de servicio (Var(S)):").pack(pady=5)
        self.var_s_entry = tk.Entry(self)
        self.var_s_entry.pack(pady=5)
        
        # Botón para calcular
        tk.Button(self, text="Calcular", command=self.calcular).pack(pady=20)
        
        # Área de resultados
        self.resultados = tk.Text(self, height=15, width=50, state="disabled")
        self.resultados.pack(pady=10)
        
        # Botón para cerrar
        tk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)

    def calcular(self):
        try:
            lam = float(self.lambda_entry.get())  # Tasa de llegadas
            mu = float(self.mu_entry.get())  # Tasa de servicio
            var_s = float(self.var_s_entry.get())  # Varianza del tiempo de servicio

            if lam >= mu:
                messagebox.showerror("Error", "λ debe ser menor que μ para que el sistema sea estable.")
                return

            rho = lam / mu
            lq = ((lam**2 * var_s**2) + rho**2) / (2 * (1 - rho))
            l = lq + rho
            wq = lq / lam if lam > 0 else 0
            w = wq + 1 / mu

            resultados_texto = (
                f"Resultados:\n"
                f"Utilización del servidor (ρ): {rho:.4f}\n"
                f"Número promedio en la cola (Lq): {lq:.4f}\n"
                f"Número promedio en el sistema (L): {l:.4f}\n"
                f"Tiempo promedio en la cola (Wq): {wq:.4f}\n"
                f"Tiempo promedio en el sistema (W): {w:.4f}\n"
            )

            self.resultados.config(state="normal")
            self.resultados.delete("1.0", tk.END)
            self.resultados.insert(tk.END, resultados_texto)
            self.resultados.config(state="disabled")

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")
