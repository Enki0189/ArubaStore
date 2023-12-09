class Deposito:
    def __init__(self, productos_dao):
        self.productos_dao = productos_dao
    
    def agregar_nuevo_producto(self, producto):
        self.productos_dao.insertar_producto(producto)
    
    def baja_producto(self, producto):
        return self.productos_dao.eliminar_producto(producto)
    
    def actualizar_stock(self, producto, accion):
        producto_db = self.productos_dao.buscar_producto_por_nombre(producto.nombre)
        
        if not producto_db or producto_db == None:
            # Si no se encuentra el producto se retorna falso
            return False
        
        if(accion == 'quitar'):
            stock_actualizado = producto_db.stock - producto.cantidad
            if(stock_actualizado < 0):
                #Esto significa que se pidio mas cantidad de la que hay en stock. No se realiza pedido
                return False
        else: 
            if accion == 'agregar':
                stock_actualizado = producto_db.stock + producto.cantidad
            else:
                # accion desconocida
                return False   
        
        #En este punto solo se llega si se quiso reducir stock y el stock restante no es negativo
        #o se llego porque se quiso aumentar el stock.
        producto_db.actualizar_stock(stock_actualizado)
        self.productos_dao.editar_producto(producto_db)
        return True   
            
    
    def obtener_productos(self):
        return self.productos_dao.obtener_productos()
    