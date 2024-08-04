
        
class ItemCarrito:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

    def to_dict(self):
        return {
            'producto': self.producto.to_dict(),
            'cantidad': self.cantidad
        }
