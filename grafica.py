import json
import matplotlib.pyplot as plt
from collections import defaultdict
from tkinter import messagebox

class GeneradorGrafica:
    def __init__(self, inventario_path, pedidos_path, output_image_path):
        self.inventario_path = inventario_path
        self.pedidos_path = pedidos_path
        self.output_image_path = output_image_path

    def generar_grafica(self):

        try:
            with open(self.pedidos_path, 'r', encoding='utf-8') as file:
                pedidos_data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", f"El archivo {self.pedidos_path} no se encontró.")
            return
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"El archivo {self.pedidos_path} no es un JSON válido.")
            return


        try:
            with open(self.inventario_path, 'r', encoding='utf-8') as file:
                inventario_data = json.load(file)
                inventario_productos = inventario_data.get('productos', [])
        except FileNotFoundError:
            messagebox.showerror("Error", f"El archivo {self.inventario_path} no se encontró.")
            return
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"El archivo {self.inventario_path} no es un JSON válido.")
            return


        ventas = defaultdict(int)

        for pedido in pedidos_data['pedidos']:
            for item in pedido['carrito']['items']:
                producto_nombre = item['producto']['nombre']
                cantidad_vendida = item['cantidad']
                ventas[producto_nombre] += cantidad_vendida

        productos = [p['nombre'] for p in inventario_productos]
        cantidades_vendidas = [ventas[p] if p in ventas else 0 for p in productos]
        cantidades_no_vendidas = [p['cantidad'] for p in inventario_productos]

        x = range(len(productos))

        plt.figure(figsize=(14, 8))
        plt.bar(x, cantidades_vendidas, width=0.4, label='Vendidos', color='skyblue', align='center')
        plt.bar(x, cantidades_no_vendidas, width=0.4, label='No Vendidos', color='lightcoral', align='edge')

        plt.xlabel('Productos')
        plt.ylabel('Cantidad')
        plt.title('Cantidad Vendida y No Vendida de Cada Producto en el Día')
        plt.xticks(x, productos, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()

        plt.savefig(self.output_image_path)

        plt.show()
