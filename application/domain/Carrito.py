class Carrito:
    def __init__(self, owner):
        self.owner = owner, 
        self.productos = []
    
    def agregar(self, producto):
        for producto_lista in self.productos:
            if producto_lista.nombre == producto.nombre:
                # Si se encuentra, aumentar la cantidad en uno
                producto_lista.cantidad += 1
            else:
                self.productos.append(producto)
                
    def eliminar(self, producto):
        for producto_lista in self.productos:
            if producto_lista.nombre == producto.nombre:
                # Si se encuentra, aumentar la cantidad en uno
                self.productos.remove(producto_lista)
                
    def obtener_productos(self):
        return self.productos

    def obtener_owner(self):
        return self.owner
    
    def calcular_total(self):
        total = 0
        
        for producto in self.productos:
            total += producto.precio * producto.cantidad
            
        return total