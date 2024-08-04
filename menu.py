import tkinter as tk
from tkinter import Frame, messagebox, simpledialog
from grafica import GeneradorGrafica
import inventario
from producto import Producto
from carrito import Carrito
from inventario import Inventario
from u import generate_pdf
from usuario import Usuario
from pedido import Pedido
from file_manager import FileManager
import os

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Compras")
        self.geometry("700x300")
        self.inventario = inventario
        self.productos_window = None
        self.inventario = Inventario()
        self.carrito = Carrito()
        self.usuario = None
        self.register_window = None
        self.carrito_window = None
        self.usuarios = []  
        self.usuarios_window = None
        self.productos_window = None
        self.inventario_window = None

        self.usuarios = FileManager.load_from_json('Archivos Json/usuarios.json').get('usuarios', [])
        self.cargar_productos()

        self.create_widgets()
        self.update_admin_buttons()

    def cargar_productos(self):
        productos = FileManager.load_from_json('Archivos Json/productos.json').get('productos', [])
        for p in productos:
            self.inventario.agregar_producto(Producto(**p))

    def create_widgets(self):
        separator = tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=5, pady=10)

        admin_label = tk.Label(self, text="CAFE BOXHA")
        admin_label.pack(pady=10)

        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(pady=20)

        self.btn_login = tk.Button(self.menu_frame, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.btn_login.grid(row=0, column=0, padx=10)
        
        self.btn_register = tk.Button(self.menu_frame, text="Registrarse", command=self.registrarse)
        self.btn_register.grid(row=0, column=1, padx=10)
        
        self.btn_products = tk.Button(self.menu_frame, text="Ver Productos", command=self.ver_productos)
        self.btn_products.grid(row=0, column=2, padx=10)

        self.btn_cart = tk.Button(self.menu_frame, text="Ver Carrito", command=self.ver_carrito)
        self.btn_cart.grid(row=0, column=3, padx=10)

        self.btn_order = tk.Button(self.menu_frame, text="Realizar Pedido", command=self.realizar_pedido)
        self.btn_order.grid(row=0, column=4, padx=10)

        # Separador
        separator = tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=5, pady=10)

        admin_label = tk.Label(self, text="INTERFAZ DE ADMINISTRADOR")
        admin_label.pack(pady=10)

        self.admin_frame = tk.Frame(self)
        self.admin_frame.pack(pady=10)

        self.btn_users = tk.Button(self.admin_frame, text="Gestionar Usuarios", command=self.gestionar_usuarios)
        self.btn_users.grid(row=0, column=0, padx=10)

        self.btn_products_admin = tk.Button(self.admin_frame, text="Gestionar Productos", command=self.gestionar_productos)
        self.btn_products_admin.grid(row=0, column=1, padx=10)

        self.btn_Inventario = tk.Button(self.admin_frame, text="Actualizar Inventario", command=self.actualizar_inventario)
        self.btn_Inventario.grid(row=0, column=2, padx=10)
        
        self.btn_reports = tk.Button(self.admin_frame, text="Ver Reportes", command=self.ver_reportes)
        self.btn_reports.grid(row=0, column=3, padx=10)
        
        self.btn_grafica = tk.Button(self.admin_frame, text="Genera Grafica", command=self.ver_grafica)
        self.btn_grafica.grid(row=0, column=4, padx=10)
        
        self.inventario_path = 'C:/Users/alexp/Desktop/Cafe_Boxh/Archivos Json/productos.json'
        self.pedidos_path = 'C:/Users/alexp/Desktop/Cafe_Boxh/Archivos Json/pedidos.json'
        self.output_image_path = 'C:/Users/alexp/Desktop/Cafe_Boxh/Archivos Grafica/grafica_ventas.png'
    

        self.update_admin_buttons()
        
        separator = tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=5, pady=10)

    def update_admin_buttons(self):
        if self.usuario and self.usuario.rol == 'admin':
            self.btn_reports.config(state=tk.NORMAL)
            self.btn_products_admin.config(state=tk.NORMAL)
            self.btn_users.config(state=tk.NORMAL)
            self.btn_Inventario.config(state=tk.NORMAL)
            self.btn_grafica.config(state=tk.NORMAL)
        else:
            self.btn_reports.config(state=tk.DISABLED)
            self.btn_products_admin.config(state=tk.DISABLED)
            self.btn_users.config(state=tk.DISABLED)
            self.btn_Inventario.config(state=tk.DISABLED)
            self.btn_grafica.config(state=tk.DISABLED)
            
    def iniciar_sesion(self):
        login_window = tk.Toplevel(self)
        login_window.title("Iniciar Sesión")

        tk.Label(login_window, text="Ingrese su Correo:").grid(row=0, column=0)
        self.email_entry = tk.Entry(login_window)
        self.email_entry.grid(row=0, column=1)

        tk.Label(login_window, text="Ingrese su Contraseña:").grid(row=1, column=0)
        self.password_entry = tk.Entry(login_window, show='*')
        self.password_entry.grid(row=1, column=1)

        tk.Button(login_window, text="Iniciar Sesión", command=self.handle_login).grid(row=2, column=1, pady=10)
        

    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser completados.")
            return

        if not Usuario.validar_email(email):
            messagebox.showwarning("Advertencia", "Email inválido. Asegúrese de usar un formato válido.\ntexto@texto.texto")
            return

        if not Usuario.validar_password(password):
            messagebox.showwarning("Advertencia", "La contraseña debe tener al menos 6 caracteres.")
            return
        
        for u in self.usuarios:
            if u['email'] == email and u['password'] == password:
                self.usuario = Usuario(**u)
                messagebox.showinfo("Éxito", f"Bienvenido {self.usuario.nombre} ({self.usuario.rol})")
                self.update_admin_buttons()  
                return
        messagebox.showerror("Error", "Email o password incorrectos.")

    def registrarse(self):
        
        if self.register_window is not None and self.register_window.winfo_exists():
            self.register_window.destroy()
        
        self.register_window = tk.Toplevel(self)
        self.register_window.title("Registrarse")

        tk.Label(self.register_window, text="Ingrese su Nombre:").grid(row=0, column=0)
        self.reg_nombre_entry = tk.Entry(self.register_window)
        self.reg_nombre_entry.grid(row=0, column=1)

        tk.Label(self.register_window, text="Ingrese sus Apellidos:").grid(row=1, column=0)
        self.reg_apellido_entry = tk.Entry(self.register_window)
        self.reg_apellido_entry.grid(row=1, column=1)

        tk.Label(self.register_window, text="Ingrese su Email:").grid(row=2, column=0)
        self.reg_email_entry = tk.Entry(self.register_window)
        self.reg_email_entry.grid(row=2, column=1)

        tk.Label(self.register_window, text="Ingrese su Contraseña:").grid(row=3, column=0)
        self.reg_password_entry = tk.Entry(self.register_window, show='*')
        self.reg_password_entry.grid(row=3, column=1)

        tk.Button(self.register_window, text="Registrarse", command=self.handle_register).grid(row=4, column=1, pady=10)

    def handle_register(self):
        nombre = self.reg_nombre_entry.get().strip()
        apellido = self.reg_apellido_entry.get().strip()
        email = self.reg_email_entry.get().strip()
        password = self.reg_password_entry.get().strip()

        if not nombre or not apellido or not email or not password:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser completados.")
            return

        if not Usuario.validar_nombre(nombre):
            messagebox.showwarning("Advertencia", "Nombre inválido. Solo se permiten letras y espacios.")
            return

        if not Usuario.validar_apellido(apellido):
            messagebox.showwarning("Advertencia", "Apellido inválido. Solo se permiten letras y espacios.")
            return

        if not Usuario.validar_email(email):
            messagebox.showwarning("Advertencia", "Email inválido. Asegúrese de usar un formato válido.\ntexto@texto.texto")
            return

        if not Usuario.validar_password(password):
            messagebox.showwarning("Advertencia", "La contraseña debe tener al menos 6 caracteres.")
            return

        nuevo_usuario = Usuario(nombre, apellido, email, 'cliente', password)
        self.usuarios.append(nuevo_usuario.to_dict())

        FileManager.save_to_json({'usuarios': self.usuarios}, 'Archivos Json/usuarios.json')
        messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
        
        self.register_window.destroy()

    def ver_productos(self):
        
        if self.productos_window is not None and self.productos_window.winfo_exists():
            self.productos_window.destroy()
        
        self.productos_window = tk.Toplevel(self)
        self.productos_window.title("Productos Disponibles")
        
        messagebox.showinfo("Éxito", "Si la compra es mayor a 10 productos en un tipo de cafe.\n Se aplicará un descuento del 10%.")
        
        for idx, producto in enumerate(self.inventario.productos):
            tk.Label(self.productos_window, text=f"ID: {producto.id}").grid(row=idx, column=0)
            tk.Label(self.productos_window, text=f"Nombre: {producto.nombre}").grid(row=idx, column=1)
            tk.Label(self.productos_window, text=f"Precio: ${producto.precio}").grid(row=idx, column=2)
            tk.Button(self.productos_window, text="Agregar al Carrito", command=lambda p=producto: self.agregar_al_carrito(p)).grid(row=idx, column=3)   
            
    def agregar_al_carrito(self, producto):
        cantidad = simpledialog.askinteger("Cantidad", f"Ingrese la cantidad de {producto.nombre} que desea agregar:", minvalue=1)
            
        if cantidad is not None:
            if cantidad > 0 and cantidad <= producto.cantidad:
                if cantidad > 10:
                    messagebox.showinfo("Éxito","Descuento aplicado del 10 %.")
                self.carrito.agregar_producto(producto, cantidad)
                producto.cantidad -= cantidad  
                FileManager.save_to_json({'productos': [p.to_dict() for p in self.inventario.productos]}, 'Archivos Json/productos.json')
                messagebox.showinfo("Éxito", f"{cantidad} unidad(es) de {producto.nombre} agregadas al carrito.")
                messagebox.showinfo("Éxito", f"{cantidad} unidad(es) de {producto.nombre} agregadas al carrito.\n"
                                         f"ID: {producto.id}\n"
                                         f"Nombre: {producto.nombre}\n"
                                         f"Descripción: {producto.descripcion}\n"
                                         f"Precio: ${producto.precio}\n"
                                         f"Cantidad en carrito: {cantidad}\n"
                                         f"Total: ${producto.precio * cantidad}")
            else:
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser un número positivo mayor a cero.")
                else:
                    messagebox.showerror("Error", f"No hay suficiente stock. Solo hay {producto.cantidad} unidad(es) disponibles.")
        else:
            messagebox.showerror("Error", "Ingresa 1 al menos")
    
    def ver_carrito(self):
        
        if self.carrito_window is not None and self.carrito_window.winfo_exists():
            self.carrito_window.destroy()

        if not self.carrito.items:
            messagebox.showerror("Error", "El carrito está vacío.")
            return

        self.carrito_window = tk.Toplevel(self)
        self.carrito_window.title("Mi Carrito")

        for idx, item in enumerate(self.carrito.items):
            tk.Label(self.carrito_window, text=f"ID: {item.producto.id}").grid(row=idx, column=0)
            tk.Label(self.carrito_window, text=f"Nombre: {item.producto.nombre}").grid(row=idx, column=1)
            tk.Label(self.carrito_window, text=f"Cantidad: {item.cantidad}").grid(row=idx, column=2)
            tk.Label(self.carrito_window, text=f"Precio: ${item.producto.precio:.2f}").grid(row=idx, column=3)
            tk.Button(self.carrito_window, text="Eliminar", command=lambda p=item.producto.id: self.eliminar_del_carrito(p)).grid(row=idx, column=4)
            tk.Button(self.carrito_window, text="Reducir Cantidad", command=lambda p=item.producto.id: self.reducir_cantidad(p)).grid(row=idx, column=5)

        total, discount, original_total = self.carrito.total()

        original_total_label = tk.Label(self.carrito_window, text=f"Total Original: ${original_total:.2f}")
        original_total_label.grid(row=len(self.carrito.items), columnspan=6, pady=10)

        discount_label = tk.Label(self.carrito_window, text=f"Descuento: ${discount:.2f}")
        discount_label.grid(row=len(self.carrito.items) + 1, columnspan=6, pady=10)

        total_label = tk.Label(self.carrito_window, text=f"Total: ${total:.2f}")
        total_label.grid(row=len(self.carrito.items) + 2, columnspan=6, pady=10)

        tk.Button(self.carrito_window, text="Actualizar Carrito", command=self.ver_carrito).grid(row=len(self.carrito.items) + 3, columnspan=6, pady=10)
        tk.Button(self.carrito_window, text="Cancelar Pedido", command=self.cancelar_pedido).grid(row=len(self.carrito.items) + 4, columnspan=6, pady=10)
            
    def cancelar_pedido(self):
        if not self.carrito.items:
            messagebox.showerror("Error", "El carrito está vacío. No hay pedido para cancelar.")
            return

        for item in self.carrito.items:
            self.inventario.actualizar_inventario(item.producto.id, item.cantidad)
        self.carrito.items.clear()
        messagebox.showinfo("Pedido", "Pedido cancelado y productos devueltos al inventario.")
        self.ver_carrito()

    def reducir_cantidad(self, producto_id):
        cantidad = simpledialog.askinteger("Cantidad", f"Ingrese la cantidad a reducir:", minvalue=1)
        if cantidad:
            try:
                producto, cantidad_reducida = self.carrito.reducir_cantidad(producto_id, cantidad)
                self.inventario.actualizar_inventario(producto_id, cantidad_reducida)
                messagebox.showinfo("Éxito", f"Cantidad reducida en el carrito.")
                self.ver_carrito()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def realizar_pedido(self):
        if not self.carrito.items:
            messagebox.showerror("Error", "El carrito está vacío. No puede realizar un pedido.")
            return
        
        if not self.usuario:
            nombre = simpledialog.askstring("Nombre", "Ingrese su nombre:")
            email = simpledialog.askstring("Email", "Ingrese su correo:")
            if not nombre or not email:
                messagebox.showerror("Error", "Debe proporcionar nombre y email para realizar un pedido.")
                return
            self.usuario = Usuario(nombre, '', email, 'cliente', '')
    
        metodo_pago = simpledialog.askstring("Método de Pago", "Ingrese el método de pago (efectivo/tarjeta):")
        if metodo_pago not in ['efectivo', 'tarjeta']:
            messagebox.showerror("Error", "Método de pago inválido.")
            return

        nuevo_pedido = Pedido(self.usuario, self.carrito, metodo_pago)
        nuevo_pedido.confirmar_pedido()

        FileManager.save_to_json({'productos': [p.to_dict() for p in self.inventario.productos]}, 'Archivos Json/productos.json')

        pedidos = FileManager.load_from_json(self.pedidos_path).get('pedidos', [])
        pedidos.append(nuevo_pedido.to_dict())
        FileManager.save_to_json({'pedidos': pedidos}, self.pedidos_path)

        comprobante_path = os.path.join('C:\\Users\\alexp\\Desktop\\Cafe_Boxh\\Archivos Pagos', f'Comprobante_{nuevo_pedido.usuario.nombre}_{nuevo_pedido.total}.txt')
        with open(comprobante_path, 'w') as file:
            file.write(f"Comprobante de Pago\n")
            file.write(f"===================\n")
            file.write(f"Nombre: {nuevo_pedido.usuario.nombre}\n")
            file.write(f"Email: {nuevo_pedido.usuario.email}\n")
            file.write(f"Total: ${nuevo_pedido.total}\n")
            file.write(f"Método de Pago: {nuevo_pedido.metodo_pago}\n")
            file.write(f"Estado: {nuevo_pedido.estado}\n")
            file.write(f"\nProductos:\n")
            for item in nuevo_pedido.carrito.items:
                file.write(f" - {item.producto.nombre} x {item.cantidad} = ${item.producto.precio * item.cantidad}\n")

        messagebox.showinfo("Éxito", "Pedido realizado exitosamente.")
        self.carrito.vaciar_carrito()

    def gestionar_usuarios(self):
        
        if self.usuarios_window is not None and self.usuarios_window.winfo_exists():
            self.usuarios_window.destroy()

        self.usuarios_window = tk.Toplevel(self)
        self.usuarios_window.title("Gestión de Usuarios")

        for idx, user in enumerate(self.usuarios):
            tk.Label(self.usuarios_window, text=f"Nombre: {user['nombre']} {user['apellido']}").grid(row=idx, column=0)
            tk.Label(self.usuarios_window, text=f"Email: {user['email']}").grid(row=idx, column=1)
            tk.Button(self.usuarios_window, text="Eliminar", command=lambda u=user['email']: self.eliminar_usuario(u)).grid(row=idx, column=2)
            tk.Button(self.usuarios_window, text="Actualizar", command=lambda u=user: self.actualizar_usuario(u)).grid(row=idx, column=3)
        
        tk.Button(self.usuarios_window, text="Agregar Usuario", command=self.registrarse).grid(row=len(self.usuarios)+1, columnspan=6, pady=10)
    
        tk.Button(self.usuarios_window, text="Actualizar", command=self.gestionar_usuarios).grid(row=len(self.usuarios)+1, columnspan=1, pady=10)
   
    def eliminar_usuario(self, email):
        if messagebox.askyesno("Advertencia", "Esta seguro de Eliminar este usuario. ¿Desea cancelar?"):
            self.usuarios = [u for u in self.usuarios if u['email'] != email]
            FileManager.save_to_json({'usuarios': self.usuarios}, 'Archivos Json/usuarios.json')
            messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
            self.gestionar_usuarios()
        else:
            messagebox.showinfo("Cancelado", "Eliminación de usuario cancelada.")

    def actualizar_usuario(self, user):
        nombre = simpledialog.askstring("Nombre", "Ingrese el nuevo nombre:", initialvalue=user['nombre'])
        if nombre is None:
            messagebox.showinfo("Cancelado", "Actualización de usuario cancelada.")
            return
    
        apellido = simpledialog.askstring("Apellido", "Ingrese el nuevo apellido:", initialvalue=user['apellido'])
        if apellido is None:
            messagebox.showinfo("Cancelado", "Actualización de usuario cancelada.")
            return
    
        password = simpledialog.askstring("Password", "Ingrese el nuevo password:", initialvalue=user['password'])
        if password is None:
            messagebox.showinfo("Cancelado", "Actualización de usuario cancelada.")
            return
    
        rol = simpledialog.askstring("Rol", "Ingrese el nuevo rol (cliente/admin):", initialvalue=user['rol'])
        if rol is None:
            messagebox.showinfo("Cancelado", "Actualización de usuario cancelada.")
            return
    
        user.update({'nombre': nombre, 'apellido': apellido, 'password': password, 'rol': rol})
        FileManager.save_to_json({'usuarios': self.usuarios}, 'Archivos Json/usuarios.json')
        messagebox.showinfo("Éxito", "Usuario actualizado exitosamente.")
        self.gestionar_usuarios()


    def gestionar_productos(self):
        
        if self.productos_window is not None and self.productos_window.winfo_exists():
            self.productos_window.destroy()

        self.productos_window = tk.Toplevel(self)
        self.productos_window.title("Gestión de Productos")

        for idx, producto in enumerate(self.inventario.productos):
            tk.Label(self.productos_window, text=f"ID: {producto.id}").grid(row=idx, column=0)
            tk.Label(self.productos_window, text=f"Nombre: {producto.nombre}").grid(row=idx, column=1)
            tk.Label(self.productos_window, text=f"Precio: ${producto.precio}").grid(row=idx, column=2)
            tk.Label(self.productos_window, text=f"Cantidad: {producto.cantidad}").grid(row=idx, column=3)
            tk.Button(self.productos_window, text="Eliminar", command=lambda p=producto.id: self.eliminar_producto(p)).grid(row=idx, column=4)
            tk.Button(self.productos_window, text="Actualizar", command=lambda p=producto: self.actualizar_producto(p)).grid(row=idx, column=5)

        tk.Button(self.productos_window, text="Agregar nuevo café", command=self.agregar_producto).grid(row=len(self.inventario.productos)+1, columnspan=6, pady=10)

    def eliminar_producto(self, producto_id):
        if messagebox.askyesno("Advertencia", "¿Está seguro de eliminar este producto? ¿Desea continuar?"):
            
            if self.productos_window is not None and self.productos_window.winfo_exists():
                self.productos_window.destroy()

            self.inventario.eliminar_producto(producto_id)
            FileManager.save_to_json({'productos': [p.to_dict() for p in self.inventario.productos]}, 'Archivos Json/productos.json')
            messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")
            self.gestionar_productos()  
        else:
            messagebox.showinfo("Cancelado", "Eliminación de producto cancelada.")

    def agregar_producto(self):
        
        if self.productos_window is not None and self.productos_window.winfo_exists():
            self.productos_window.destroy()

        producto_id = None
        while producto_id is None:
            producto_id = simpledialog.askinteger("ID", "Ingrese el ID del producto:")
            if producto_id is None:
                if messagebox.askyesno("Advertencia", "El ID del producto no puede estar vacío. ¿Desea cancelar?"):
                    return

        nombre = None
        while not nombre:
            nombre = simpledialog.askstring("Nombre", "Ingrese el nombre del producto:")
            if not nombre:
                if messagebox.askyesno("Advertencia", "El nombre del producto no puede estar vacío. ¿Desea cancelar?"):
                    return

        descripcion = None
        while not descripcion:
            descripcion = simpledialog.askstring("Descripción", "Ingrese la descripción del producto:")
            if not descripcion:
                if messagebox.askyesno("Advertencia", "La descripción del producto no puede estar vacía. ¿Desea cancelar?"):
                    return

        precio = None
        while precio is None:
            precio = simpledialog.askfloat("Precio", "Ingrese el precio del producto:")
            if precio is None:
                if messagebox.askyesno("Advertencia", "El precio del producto no puede estar vacío. ¿Desea cancelar?"):
                    return

        cantidad = None
        while cantidad is None:
            cantidad = simpledialog.askinteger("Cantidad", "Ingrese la cantidad del producto:")
            if cantidad is None:
                if messagebox.askyesno("Advertencia", "La cantidad del producto no puede estar vacía. ¿Desea cancelar?"):
                    return

        nuevo_producto = Producto(producto_id, nombre, descripcion, precio, cantidad)
        self.inventario.agregar_producto(nuevo_producto)
        FileManager.save_to_json({'productos': [p.to_dict() for p in self.inventario.productos]}, 'Archivos Json/productos.json')
        messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
        self.gestionar_productos()  


    def actualizar_producto(self, producto):
        
        if self.productos_window is not None and self.productos_window.winfo_exists():
            self.productos_window.destroy()
            
        nombre = simpledialog.askstring("Nombre", "Ingrese el nuevo nombre:", initialvalue=producto.nombre)
        if nombre is None:
            messagebox.showinfo("Cancelado", "Actualización de producto cancelada.")
            return

        descripcion = simpledialog.askstring("Descripción", "Ingrese la nueva descripción:", initialvalue=producto.descripcion)
        if descripcion is None:
            messagebox.showinfo("Cancelado", "Actualización de producto cancelada.")
            return

        precio = simpledialog.askfloat("Precio", "Ingrese el nuevo precio:", initialvalue=producto.precio)
        if precio is None:
            messagebox.showinfo("Cancelado", "Actualización de producto cancelada.")
            return

        cantidad = simpledialog.askinteger("Cantidad", "Ingrese la nueva cantidad:", initialvalue=producto.cantidad)
        if cantidad is None:
            messagebox.showinfo("Cancelado", "Actualización de producto cancelada.")
            return

        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.cantidad = cantidad
        
        FileManager.save_to_json({'productos': [p.to_dict() for p in self.inventario.productos]}, 'Archivos Json/productos.json')
        messagebox.showinfo("Éxito", "Producto actualizado exitosamente.")
        
        self.gestionar_productos()


    def actualizar_inventario(self):
        
        if self.inventario_window is not None and self.inventario_window.winfo_exists():
            self.inventario_window.destroy()

        self.inventario_window = tk.Toplevel(self)
        self.inventario_window.title("Actualizar Inventario")

        for idx, producto in enumerate(self.inventario.productos):
            tk.Label(self.inventario_window, text=f"ID: {producto.id}").grid(row=idx, column=0)
            tk.Label(self.inventario_window, text=f"Nombre: {producto.nombre}").grid(row=idx, column=1)
            tk.Label(self.inventario_window, text=f"Cantidad Actual: {producto.cantidad}").grid(row=idx, column=2)
            tk.Button(self.inventario_window, text="Agregar Stock", command=lambda p=producto: self.agregar_stock(p)).grid(row=idx, column=3)
            tk.Button(self.inventario_window, text="Reducir Stock", command=lambda p=producto: self.reducir_stock(p)).grid(row=idx, column=4)

        tk.Button(self.inventario_window, text="Actualizar Inventario", command=self.actualizar_inventario).grid(row=len(self.inventario.productos), columnspan=5, pady=10)
        
    def agregar_stock(self, producto):
        cantidad = simpledialog.askinteger("Cantidad", f"Ingrese la cantidad a agregar para {producto.nombre}:")
        if cantidad is None:
            messagebox.showinfo("Cancelado", "Operación de agregar stock cancelada.")
            return
        if cantidad > 0:
            producto.cantidad += cantidad
            FileManager.save_to_json({'productos': [p.to_dict() for p in self.inventario.productos]}, 'Archivos Json/productos.json')
            messagebox.showinfo("Éxito", f"{cantidad} unidades agregadas al inventario de {producto.nombre}.")
            self.actualizar_inventario()
        else:
            messagebox.showerror("Error", "La cantidad debe ser mayor que cero.")

    def reducir_stock(self, producto):
        cantidad = simpledialog.askinteger("Cantidad", f"Ingrese la cantidad a reducir para {producto.nombre}:")
        if cantidad is None:
            messagebox.showinfo("Cancelado", "Operación de reducir stock cancelada.")
            return
        if cantidad > 0:
            if producto.cantidad >= cantidad:
                producto.cantidad -= cantidad
                FileManager.save_to_json({'productos': [p.to_dict() for p in self.inventario.productos]}, 'Archivos Json/productos.json')
                messagebox.showinfo("Éxito", f"{cantidad} unidades reducidas del inventario de {producto.nombre}.")
                self.actualizar_inventario()
            else:
                messagebox.showerror("Error", "No hay suficiente stock para reducir esa cantidad.")
        else:
            messagebox.showerror("Error", "La cantidad debe ser mayor que cero.")


    def ver_reportes(self):

        path_pdf = 'C:\\Users\\alexp\\Desktop\\Cafe_Boxh\\Archivos PDF\\inventario.pdf'
        self.inventario.generar_pdf(path_pdf)

        messagebox.showinfo("Reporte Generado", f"El reporte de inventario se ha generado y guardado en {path_pdf}")

        json_file_path = 'C:\\Users\\alexp\\Desktop\\Cafe_Boxh\\Archivos Json\\pedidos.json'
        path_pdf = 'C:\\Users\\alexp\\Desktop\\Cafe_Boxh\\Archivos Pdf\\pedidos.pdf'

        generate_pdf(json_file_path, path_pdf)

        messagebox.showinfo("Reporte Generado", f"El reporte de pedidos se ha generado y guardado en {path_pdf}")

    def ver_grafica(self):
        generador = GeneradorGrafica(self.inventario_path, self.pedidos_path, self.output_image_path)
        generador.generar_grafica()
        messagebox.showinfo("Gráfica Generada", f"La gráfica de ventas se ha generado y guardado en {self.output_image_path}")
        
    def on_closing(self):
        if self.carrito.items:
            for item in self.carrito.items:
                self.inventario.actualizar_inventario(item.producto.id, item.cantidad)
            messagebox.showinfo("Carrito", "Productos devueltos al inventario.")
        self.root.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
