from producto import Producto
from file_manager import FileManager
import json
from fpdf import FPDF

class Inventario:
    def __init__(self):
        self.productos = []

    def cargar_inventario(self):
        path_json = 'C:\\Users\\alexp\\Desktop\\Cafe_Boxh\\Archivos Json\\productos.json'
        try:
            with open(path_json, 'r') as f:
                data = json.load(f)
                if 'productos' in data:
                    return [Producto(**p) for p in data['productos']]
                else:
                    print("Error: La clave 'productos' no está en el archivo JSON.")
                    return []
        except FileNotFoundError:
            print(f"Error: El archivo {path_json} no se encontró.")
            return []
        except json.JSONDecodeError:
            print(f"Error: El archivo {path_json} no es un JSON válido.")
            return []

    def guardar_inventario(self):
        path = 'C:\\Users\\alexp\\Desktop\\Cafe_Boxh\\Archivos Json\\inventario.json'
        with open(path, 'w') as f:
            json.dump({'productos': [p.to_dict() for p in self.productos]}, f, indent=4)     
    
    def actualizar_inventario(self, producto_id, cantidad):
        for producto in self.productos:
            if producto.id == producto_id:
                producto.cantidad += cantidad
                break

    def quitar_del_inventario(self, producto_id, cantidad):
        for producto in self.productos:
            if producto.id == producto_id:
                if producto.cantidad >= cantidad:
                    producto.cantidad -= cantidad
                    return True
                else:
                    return False
        return False

    def __str__(self):
        return '\n'.join([f"ID: {p.id}, Nombre: {p.nombre}, Descripción: {p.descripcion}, Precio: {p.precio}, Cantidad: {p.cantidad}" for p in self.productos])
    
    def agregar_producto(self, producto):
        self.productos.append(producto)

    def obtener_producto(self, id_producto):
        for producto in self.productos:
            if producto.id == id_producto:
                return producto
        return None
    
    def eliminar_producto(self, producto_id):
        self.productos = [p for p in self.productos if p.id != producto_id]

    def modificar_producto(self, producto_modificado):
        for idx, producto in enumerate(self.productos):
            if producto.id == producto_modificado.id:
                self.productos[idx] = producto_modificado
                break

    def generar_pdf(self, path_pdf):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Inventario de Productos", ln=True, align='C')

        pdf.cell(20, 10, txt="ID", border=1)
        pdf.cell(50, 10, txt="Nombre", border=1)
        pdf.cell(80, 10, txt="Descripción", border=1)
        pdf.cell(20, 10, txt="Precio", border=1)
        pdf.cell(20, 10, txt="Cantidad", border=1)
        pdf.ln()

        for producto in self.productos:
            descripcion = producto.descripcion
            descripcion_lines = [descripcion[i:i+36] for i in range(0, len(descripcion), 36)]

            pdf.cell(20, 10, txt=str(producto.id), border=1)
            pdf.cell(50, 10, txt=producto.nombre, border=1)
            

            pdf.cell(80, 10, txt=descripcion_lines[0], border=1)
            pdf.cell(20, 10, txt=str(producto.precio), border=1)
            pdf.cell(20, 10, txt=str(producto.cantidad), border=1)
            pdf.ln()

 
            for line in descripcion_lines[1:]:
                pdf.cell(20, 10, txt="", border=0)  
                pdf.cell(50, 10, txt="", border=0)  
                pdf.cell(80, 10, txt=line, border=1)
                pdf.cell(20, 10, txt="", border=0)  
                pdf.cell(20, 10, txt="", border=0)  
                pdf.ln()

        pdf.output(path_pdf)


inventario = Inventario()
inventario.cargar_inventario()
print(inventario)  
inventario.generar_pdf('C:\\Users\\alexp\\Desktop\\Cafe_Boxh\\Archivos PDF\\inventario.pdf')

