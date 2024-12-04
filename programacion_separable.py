import tkinter as tk
from tkinter import messagebox
from scipy.optimize import minimize

class ProgramacionSeparableVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Optimización de Función Objetivo")
        self.geometry("700x600")

        self.variables_frame = tk.Frame(self)
        self.variables_frame.pack(pady=10)

        
        tk.Label(self.variables_frame, text="Función Objetivo :").grid(row=0, column=0, padx=5, pady=5)
        self.obj_func_entry = tk.Entry(self.variables_frame)
        self.obj_func_entry.insert(0, "x1 + x2**4")  
        self.obj_func_entry.grid(row=0, column=1, padx=5, pady=5)

      
        tk.Label(self.variables_frame, text="Restricción :").grid(row=1, column=0, padx=5, pady=5)
        self.restriccion_entry = tk.Entry(self.variables_frame)
        self.restriccion_entry.insert(0, "3*x1 + 2*x2**2-9")  
        self.restriccion_entry.grid(row=1, column=1, padx=5, pady=5)

        
        tk.Button(self, text="Resolver", command=self.resolver).pack(pady=20)

    def resolver(self):
        try:   
            obj_func_str = self.obj_func_entry.get()
            restriccion_str = self.restriccion_entry.get()

            def objetivo(vars):
                x1, x2 = vars
                return -(eval(obj_func_str))  


            def restriccion1(vars):
                x1, x2 = vars
                return 0 - eval(restriccion_str)

            restricciones = [{'type': 'ineq', 'fun': restriccion1}]
            limites = [(0, None), (0, None)] 

            punto_inicial = [0.0, 2.0] 
          
            resultado = minimize(objetivo, punto_inicial, bounds=limites, constraints=restricciones, method='SLSQP')

     
            x1, x2 = resultado.x
            z = -(x1 + x2**4) 

            resultado_texto = f"x1 = {x1:.4f}\nx2 = {x2:.4f}\nZ = {z:.4f}"
            messagebox.showinfo("Resultado", resultado_texto)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


