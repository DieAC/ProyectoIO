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
        denominador = sum([(factorial(self.k) / (factorial(self.k - i))) * (self.lambda_ / self.mu) ** i for i in range(self.k + 1)])
        
        probabilidad = [(((factorial(self.k) / (factorial(self.k - i))) * (self.lambda_ / self.mu) ** i) / denominador) for i in range(self.k + 1)]
        
        return probabilidad
    
    def calcular_longitud_promedio(self):
        probabilidad_ocupacion = self.calcular_probabilidad_ocupacion()[0]
        Lq = self.calcular_longitud_promedio_cola()
        L = Lq + (1 - probabilidad_ocupacion)
        
        return L

    def calcular_longitud_promedio_cola(self):
        probabilidad_ocupacion = self.calcular_probabilidad_ocupacion()[0]
        
        Lq = self.k - (((self.lambda_ + self.mu) / self.lambda_) * (1 - probabilidad_ocupacion))
        
        return Lq

    def calcular_tiempo_promedio_cola(self):
        Lq = self.calcular_longitud_promedio_cola()
        L = self.calcular_longitud_promedio()
        Wq = Lq / ((self.k - L) * self.lambda_)
        return Wq

    def calcular_tiempo_promedio_sistema(self):
        Wq = self.calcular_tiempo_promedio_cola()
        W = Wq + (1 / self.mu)
        return W

    def calcular_probabilidad_de_ocupacion_total(self):
        probabilidad_ocupacion = self.calcular_probabilidad_ocupacion()[-1]
        return probabilidad_ocupacion
    
    def calcular_probabilidad_de_ocupacion_nula(self):
        probabilidad_desocupacion = self.calcular_probabilidad_ocupacion()[0]
        return probabilidad_desocupacion

class FuentesFinitasVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Modelo Fuentes Finitas")
        self.geometry("400x500")
        
        tk.Label(self, text="Tasa de llegada (λ):").pack(pady=5)
        self.lambda_entry = tk.Entry(self)
        self.lambda_entry.pack(pady=5)
        
        tk.Label(self, text="Tasa de servicio promedio (μ):").pack(pady=5)
        self.mu_entry = tk.Entry(self)
        self.mu_entry.pack(pady=5)
        
        tk.Label(self, text="Población finita (N):").pack(pady=5)
        self.k_entry = tk.Entry(self)
        self.k_entry.pack(pady=5)
        
        tk.Button(self, text="Calcular", command=self.calcular).pack(pady=20)
        
        self.resultados = tk.Text(self, height=15, width=50, state="disabled")
        self.resultados.pack(pady=10)
        
        tk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)

    def calcular(self):
        try:
            lambda_ = float(self.lambda_entry.get()) 
            mu = float(self.mu_entry.get()) 
            k = int(self.k_entry.get())  
            
            if lambda_ <= 0 or mu <= 0 or k <= 0:
                messagebox.showerror("Error", "Todos los valores deben ser positivos.")
                return
            
            modelo = ModeloFuentesFinitas(lambda_, mu, k)
            
            probabilidades = modelo.calcular_probabilidad_ocupacion()
            
            longitud_promedio = modelo.calcular_longitud_promedio()
            
            longitud_promedio_cola = modelo.calcular_longitud_promedio_cola()
            
            tiempo_promedio_cola = modelo.calcular_tiempo_promedio_cola()
            
            tiempo_promedio_sistema = modelo.calcular_tiempo_promedio_sistema()
            
            probabilidad_ocupacion_total = modelo.calcular_probabilidad_de_ocupacion_total()
            

            probabilidad_ocupacion_nula = modelo.calcular_probabilidad_de_ocupacion_nula()

            resultados_texto = "Probabilidades de ocupación P(0) a P(k):\n"
            for i, p in enumerate(probabilidades):
                resultados_texto += f"P({i}) = {p:.4f}\n"
            
            resultados_texto += f"\nLongitud promedio del sistema L: {longitud_promedio:.4f}\n"
            resultados_texto += f"Longitud promedio de la cola Lq: {longitud_promedio_cola:.4f}\n"
            resultados_texto += f"Tiempo promedio en la cola Wq: {tiempo_promedio_cola:.4f}\n"
            resultados_texto += f"Tiempo promedio en el sistema W: {tiempo_promedio_sistema:.4f}\n"
            resultados_texto += f"Probabilidad de que todos los servidores estén desocupados P(0): {probabilidad_ocupacion_nula:.4f}\n"
            resultados_texto += f"Probabilidad de que todos los servidores estén ocupados P(k): {probabilidad_ocupacion_total:.4f}"
            
            self.resultados.config(state="normal")
            self.resultados.delete("1.0", tk.END)
            self.resultados.insert(tk.END, resultados_texto)
            self.resultados.config(state="disabled")
        
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos.")