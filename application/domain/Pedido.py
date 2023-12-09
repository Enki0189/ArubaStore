class Pedido:
    def __init__(self, id, fecha, estado, cliente, productos, medio_pago):
        self.id = id
        self.fecha = fecha
        self.estado = estado
        self.cliente = cliente
        self.productos = productos
        self.medio_pago = medio_pago
    
    def actualizar(self, estado):
        self.estado = estado