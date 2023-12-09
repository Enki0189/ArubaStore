class Cajero:
    def __init__(self, medios_pago):
        self.medios_pago = medios_pago
    
    def pagar(self, carrito, medio_pago):
        return medio_pago.pagar(carrito.calcular_total())
    
    def obtener_medios_pago(self):
        return self.medios_pago