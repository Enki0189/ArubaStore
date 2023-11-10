class Pedido:
    def __init__(self, id, fecha, estado, tipoDeMedioDePago, usuario, productos):
        self.id = id
        self.fecha = fecha
        self.estado = estado
        self.tipoDeMedioDePago = tipoDeMedioDePago
        self.usuario = usuario
        self.productos