#optimizacion_modelo.py
import tkinter as tk
from tkinter import messagebox
from sympy import symbols, diff, lambdify

class OptimizacionNoRestringidaVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Optimización No Restringida")
        self.geometry("600x400")

        self.method = tk.StringVar(value="Bisección")

        tk.Label(self, text="Seleccione el Método:").pack(pady=10)
        tk.Radiobutton(self, text="Método de Bisección", variable=self.method, value="Bisección").pack()
        tk.Radiobutton(self, text="Método de Newton", variable=self.method, value="Newton").pack()

        tk.Label(self, text="Ingrese la función a optimizar (en términos de x):").pack(pady=10)
        self.funcion_entry = tk.Entry(self, width=50)
        self.funcion_entry.pack()

        self.param_frame = tk.Frame(self)
        self.param_frame.pack(pady=10)

        tk.Label(self.param_frame, text="Tolerancia:").grid(row=0, column=0, padx=5, pady=5)
        self.tolerancia_entry = tk.Entry(self.param_frame)
        self.tolerancia_entry.grid(row=0, column=1, padx=5, pady=5)

        self.biseccion_frame = tk.Frame(self)
        tk.Label(self.biseccion_frame, text="Límite inferior (a):").grid(row=0, column=0, padx=5, pady=5)
        self.biseccion_a_entry = tk.Entry(self.biseccion_frame)
        self.biseccion_a_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.biseccion_frame, text="Límite superior (b):").grid(row=1, column=0, padx=5, pady=5)
        self.biseccion_b_entry = tk.Entry(self.biseccion_frame)
        self.biseccion_b_entry.grid(row=1, column=1, padx=5, pady=5)

        self.newton_frame = tk.Frame(self)
        tk.Label(self.newton_frame, text="Punto inicial (x0):").grid(row=0, column=0, padx=5, pady=5)
        self.newton_x0_entry = tk.Entry(self.newton_frame)
        self.newton_x0_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self, text="Resolver", command=self.resolver).pack(pady=20)

        self.result_label = tk.Label(self, text="", fg="blue")
        self.result_label.pack(pady=10)

        self.method.trace_add("write", self.toggle_method_frames)
        self.toggle_method_frames()

    def toggle_method_frames(self, *args):
        self.biseccion_frame.pack_forget()
        self.newton_frame.pack_forget()

        if self.method.get() == "Bisección":
            self.biseccion_frame.pack(pady=10)
        elif self.method.get() == "Newton":
            self.newton_frame.pack(pady=10)

    def resolver(self):
        try:
            funcion_str = self.funcion_entry.get()
            x = symbols('x')
            funcion = eval(funcion_str)
            derivada = diff(funcion, x)

            tolerancia = float(self.tolerancia_entry.get())

            if self.method.get() == "Bisección":
                a = float(self.biseccion_a_entry.get())
                b = float(self.biseccion_b_entry.get())
                resultado = self.biseccion_method(funcion, derivada, a, b, tolerancia)
            else:
                x0 = float(self.newton_x0_entry.get())
                resultado = self.newton_method(funcion, derivada, x0, tolerancia)

            self.result_label.config(text=f"Resultado: x* ≈ {resultado:.6f}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def biseccion_method(self, f_expr, df_expr, a, b, tolerance):
        f_prime = lambdify(symbols('x'), df_expr)

        while abs(b - a) > 2 * tolerance:
            midpoint = (a + b) / 2
            if f_prime(midpoint) > 0:
                a = midpoint
            else:
                b = midpoint

        return (a + b) / 2

    def newton_method(self, f_expr, df_expr, x0, tolerance, max_iterations=100):
        f_prime = lambdify(symbols('x'), df_expr)
        f_double_prime = lambdify(symbols('x'), diff(df_expr, symbols('x')))

        x_current = x0
        for _ in range(max_iterations):
            first_derivative = f_prime(x_current)
            second_derivative = f_double_prime(x_current)

            if abs(second_derivative) < 1e-10:
                raise ValueError("La segunda derivada es cercana a cero. Método no converge.")

            x_next = x_current - first_derivative / second_derivative

            if abs(x_next - x_current) < tolerance:
                return x_next

            x_current = x_next

        raise ValueError("El método de Newton no convergió después del número máximo de iteraciones.")

