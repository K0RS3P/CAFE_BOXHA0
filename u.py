import json
from fpdf import FPDF

def generate_pdf(json_file_path, pdf_file_path):

    with open(json_file_path, 'r') as file:
        data = json.load(file)


    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Pedidos', 0, 1, 'C')

        def chapter_title(self, num, title):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, f'Pedido {num}', 0, 1, 'L')
            self.ln(5)

        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)
            self.ln()

        def add_order(self, order, num):
            self.add_page()
            self.chapter_title(num, f"Usuario: {order['usuario']['nombre']} {order['usuario']['apellido']}")
            
            body = f"""
            Email: {order['usuario']['email']}
            Rol: {order['usuario']['rol']}
            Total: ${order['total']}
            Método de Pago: {order['metodo_pago']}
            Estado: {order['estado']}
            
            Detalles del Carrito:
            """
            
            for item in order['carrito']['items']:
                product = item['producto']
                body += f"""
                Producto ID: {product['id']}
                Nombre: {product['nombre']}
                Descripción: {product['descripcion']}
                Precio: ${product['precio']}
                Cantidad: {item['cantidad']}
                """
            
            self.chapter_body(body)

    pdf = PDF()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    for i, order in enumerate(data['pedidos'], 1):
        pdf.add_order(order, i)

    pdf.output(pdf_file_path)

    print(f'PDF generado en: {pdf_file_path}')
