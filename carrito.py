from item_carrito import ItemCarrito

class Carrito:
    def __init__(self):
        self.items = []

    def agregar_producto(self, producto, cantidad):
        for item in self.items:
            if item.producto.id == producto.id:
                item.cantidad += cantidad
                return
        self.items.append(ItemCarrito(producto, cantidad))
    
    def eliminar_producto(self, producto_id):
        for item in self.items:
            if item.producto.id == producto_id:
                self.items.remove(item)
                return item.producto, item.cantidad
        return None, 0

    def reducir_cantidad(self, producto_id, cantidad):
        for item in self.items:
            if item.producto.id == producto_id:
                if item.cantidad >= cantidad:
                    item.cantidad -= cantidad
                    if item.cantidad == 0:
                        self.items.remove(item)
                    return item.producto, cantidad
                else:
                    raise ValueError("Cantidad a reducir es mayor que la cantidad en el carrito.")
        raise ValueError("Producto no encontrado en el carrito.")

    def vaciar_carrito(self):
        self.items = []
    
    def total(self):
        total_items = sum(item.cantidad for item in self.items)
        total_cost = sum(item.producto.precio * item.cantidad for item in self.items)
        discount = 0

        if total_items > 10:
            discount = total_cost * 0.10 
            total_cost *= 0.90 

        return total_cost, discount, total_cost + discount
    
    def ver_carrito(self):
        for item in self.items:
            print(f"ID: {item.producto.id} - Nombre: {item.producto.nombre} - Cantidad: {item.cantidad} - Precio: ${item.producto.precio:.2f}")
        total = sum(item.producto.precio * item.cantidad for item in self.items)
        print(f"Total: ${total:.2f}")

    def to_dict(self):
        return {
            'items': [item.to_dict() for item in self.items]
        }
