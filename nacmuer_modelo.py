import tkinter as tk
from tkinter import messagebox

class NacimientoMuerteVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Modelo de Nacimiento y Muerte")
        self.geometry("400x400")

        tk.Label(self, text="Tasa de nacimiento (λ):").pack(pady=5)
        self.lambda_entry = tk.Entry(self)
        self.lambda_entry.pack(pady=5)

        tk.Label(self, text="Tasa de muerte (μ):").pack(pady=5)
        self.mu_entry = tk.Entry(self)
        self.mu_entry.pack(pady=5)

        tk.Label(self, text="Número de clientes en el sistema (n):").pack(pady=5)
        self.n_entry = tk.Entry(self)
        self.n_entry.pack(pady=5)

        tk.Label(self, text="Número de servidores (s):").pack(pady=5)
        self.s_entry = tk.Entry(self)
        self.s_entry.pack(pady=5)

        tk.Button(self, text="Calcular", command=self.calcular).pack(pady=20)

        self.resultados = tk.Text(self, height=10, width=50, state="disabled")
        self.resultados.pack(pady=10)

        tk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)

    def calcular(self):
        try:
            lam = float(self.lambda_entry.get()) 
            mu = float(self.mu_entry.get()) 
            n = int(self.n_entry.get())
            s = int(self.s_entry.get())  

            if lam >= mu:
                messagebox.showerror("Error", "λ debe ser menor que μ para que el sistema sea estable.")
                return

            rho = lam / mu

            sumatoria = sum(rho**i for i in range(n + 1))
            p0 = 1 / sumatoria
            probabilidades = [p0]
            p = 1 - p0
            
            for i in range(1, n + 1):
                pn = p0 * (rho ** i)
                probabilidades.append(pn)

            L = sum(i * probabilidades[i] for i in range(n + 1))

            Lq = sum((i - s) * probabilidades[i] for i in range(s + 1, n + 1))

            Wq = Lq / lam if lam > 0 else 0

            W = L / lam if lam > 0 else 0

            resultados_texto = (
                f"Resultados:\n"
                f"Probabilidad de que no haya unidades en el sistema (ρ0): {p0:.4f}\n"
                f"Utilización del sistema (ρ): {p:.4f}\n"
                f"Longitud promedio de la cola (Lq): {Lq:.4f}\n"
                f"Longitud promedio del sistema (L): {L:.4f}\n"
                f"Tiempo promedio en la cola (Wq): {Wq:.4f}\n"
                f"Tiempo promedio en el sistema (W): {W:.4f}\n\n"
                f"Probabilidades:\n"
            )
            for i, pn in enumerate(probabilidades):
                resultados_texto += f"P({i}): {pn:.4f}\n"

            self.resultados.config(state="normal")
            self.resultados.delete("1.0", tk.END)
            self.resultados.insert(tk.END, resultados_texto)
            self.resultados.config(state="disabled")

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")