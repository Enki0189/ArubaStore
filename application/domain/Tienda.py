from application.domain.Pedido import Pedido
from datetime import date


class Tienda:
    
    def __init__(self, cajero, deposito):
        self.pedidos = []
        self.cajero = cajero
        self.deposito = deposito
    
    def realizar_compra(self, carrito, medio_pago): 
        productos_reservados = []
        productos_carrito = carrito.obtener_productos()
        
        reserva_stock_exitosa = self.reservar_stock(productos_reservados, productos_carrito)
        
        if reserva_stock_exitosa:
            compra_exitosa = self.cajero.pagar(carrito, medio_pago)
            if compra_exitosa:
                pedido = self.crear_pedido(carrito, medio_pago)
                carrito.vaciar()
                return pedido
        else:
            self.restaurar_stock(productos_reservados)
        
        return None 
    
    def reservar_stock(self, productos_reservados, productos_carrito):
        for producto in productos_carrito:
            esta_reservado_stock = self.deposito.actualizar_stock(producto, 'quitar')
            if esta_reservado_stock: 
                productos_reservados.append(producto)
            else:
                return False
        return True
    
    def restaurar_stock(self, productos_reservados):
        for producto in productos_reservados:
            self.deposito.actualizar_stock(producto, 'agregar')
            
    def crear_pedido(self, carrito, medio_pago):
        return Pedido(None, date.today(), 'CREADO', carrito.obtener_owner(), carrito.obtener_productos(), medio_pago)