import tkinter as tk
from tkinter import messagebox
from math import factorial

class ModeloFuentesFinitas:
    def __init__(self, lambda_, mu, k):
        self.lambda_ = lambda_
        self.mu = mu
        self.k = k
        self.rho = lambda_ / mu
    
    def calcular_probabilidad_ocupacion(self):
        # Calcular la sumatoria en el denominador
        denominador = sum([(factorial(self.k) / (factorial(i) * factorial(self.k - i))) * (self.lambda_ / self.mu) ** i for i in range(self.k + 1)])
        
        # Calcular la probabilidad P_j para cada j
        probabilidad = [((factorial(self.k) / (factorial(i) * factorial(self.k - i))) * (self.lambda_ / self.mu) ** i) / denominador for i in range(self.k + 1)]
        
        return probabilidad
    
    def calcular_longitud_promedio(self):
        # Calcular P_k (probabilidad de que todos los servidores estén ocupados)
        probabilidad_ocupacion = self.calcular_probabilidad_ocupacion()[-1]
        
        # Calcular longitud promedio
        L = self.lambda_ / self.mu * (1 / (1 - probabilidad_ocupacion))
        
        return L

    def calcular_longitud_promedio_cola(self):
        # Calcular la probabilidad de que todos los servidores estén ocupados P(k)
        probabilidad_ocupacion = self.calcular_probabilidad_ocupacion()[-1]
        
        # Calcular longitud promedio de la cola (Lq)
        Lq = ((self.lambda_ ** 2) * probabilidad_ocupacion + self.rho ** 2) / (2 * (1 - self.rho))
        
        return Lq

    def calcular_tiempo_promedio_cola(self):
        Lq = self.calcular_longitud_promedio_cola()
        # Calcular tiempo promedio de espera en la cola (Wq)
        Wq = Lq / self.lambda_
        return Wq

    def calcular_tiempo_promedio_sistema(self):
        Wq = self.calcular_tiempo_promedio_cola()
        # Calcular tiempo promedio en el sistema (W)
        W = Wq + (1 / self.mu)
        return W

    def calcular_probabilidad_de_ocupacion_total(self):
        # Calcular P_k (probabilidad de que todos los servidores estén ocupados)
        probabilidad_ocupacion = self.calcular_probabilidad_ocupacion()[-1]
        return probabilidad_ocupacion

class FuentesFinitasVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Modelo Fuentes Finitas")
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
            lambda_ = float(self.lambda_entry.get())  # λ
            mu = float(self.mu_entry.get())  # μ
            k = int(self.k_entry.get())  # k (número de servidores)
            
            if lambda_ <= 0 or mu <= 0 or k <= 0:
                messagebox.showerror("Error", "Todos los valores deben ser positivos.")
                return
            
            modelo = ModeloFuentesFinitas(lambda_, mu, k)
            
            # Calcular probabilidades P(0) a P(k)
            probabilidades = modelo.calcular_probabilidad_ocupacion()
            
            # Calcular longitud promedio
            longitud_promedio = modelo.calcular_longitud_promedio()
            
            # Calcular longitud promedio de la cola
            longitud_promedio_cola = modelo.calcular_longitud_promedio_cola()
            
            # Calcular tiempo promedio en la cola
            tiempo_promedio_cola = modelo.calcular_tiempo_promedio_cola()
            
            # Calcular tiempo promedio en el sistema
            tiempo_promedio_sistema = modelo.calcular_tiempo_promedio_sistema()
            
            # Calcular la probabilidad de ocupación total (P(k))
            probabilidad_ocupacion_total = modelo.calcular_probabilidad_de_ocupacion_total()
            
            # Mostrar resultados en el área de texto
            resultados_texto = "Probabilidades de ocupación P(0) a P(k):\n"
            for i, p in enumerate(probabilidades):
                resultados_texto += f"P({i}) = {p:.4f}\n"
            
            resultados_texto += f"\nLongitud promedio del sistema L: {longitud_promedio:.4f}\n"
            resultados_texto += f"Longitud promedio de la cola Lq: {longitud_promedio_cola:.4f}\n"
            resultados_texto += f"Tiempo promedio en la cola Wq: {tiempo_promedio_cola:.4f}\n"
            resultados_texto += f"Tiempo promedio en el sistema W: {tiempo_promedio_sistema:.4f}\n"
            resultados_texto += f"Probabilidad de que todos los servidores estén ocupados P(k): {probabilidad_ocupacion_total:.4f}"
            
            self.resultados.config(state="normal")
            self.resultados.delete("1.0", tk.END)
            self.resultados.insert(tk.END, resultados_texto)
            self.resultados.config(state="disabled")
        
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos.")
