import tkinter as tk
from tkinter import simpledialog, messagebox

class Pedido:
    def __init__(self, usuario, carrito, metodo_pago):
        self.usuario = usuario
        self.carrito = carrito
        self.total = carrito.total()
        self.metodo_pago = metodo_pago
        self.estado = "Pendiente"

    def confirmar_pedido(self):
        if self.metodo_pago == 'efectivo':
            messagebox.showinfo("Pago Procesado", "Pago en efectivo confirmado.")
            messagebox.showinfo("Comprobante en Efectivo", "Comprobante generado")
        elif self.metodo_pago == 'tarjeta':
            tarjeta_valida = False
            while not tarjeta_valida:
                numero_tarjeta = simpledialog.askstring("Pago con Tarjeta", "Ingrese el número de tarjeta (16 dígitos):")
                cvv = simpledialog.askstring("Pago con Tarjeta", "Ingrese el CVV (3 dígitos):", show='*')
                if numero_tarjeta and cvv:
                    if len(numero_tarjeta) == 16 and numero_tarjeta.isdigit() and len(cvv) == 3 and cvv.isdigit():
                        tarjeta_valida = True
                        messagebox.showinfo("Pago Procesado", "Pago con tarjeta confirmado.")
                        messagebox.showinfo("Comprobate por Tarjeta", "Comprobante generado")
                    else:
                        messagebox.showerror("Error", "Número de tarjeta o CVV inválido. Inténtelo de nuevo.")
                else:
                    messagebox.showerror("Error", "Debe ingresar tanto el número de tarjeta como el CVV.")
        self.estado = "Confirmado"

    def __str__(self):
        return f"Pedido de {self.usuario.nombre} - Total: ${self.total} - Estado: {self.estado}"

    def to_dict(self):
        return {
            'usuario': self.usuario.to_dict(),
            'carrito': self.carrito.to_dict(),
            'total': self.total,
            'metodo_pago': self.metodo_pago,
            'estado': self.estado
        }