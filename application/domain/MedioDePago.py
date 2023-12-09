from abc import ABC, abstractmethod

class MedioDePago(ABC):
    
    @abstractmethod
    def pagar(self, monto):
        pass
    
    @abstractmethod
    def obtener_descripcion(self):
        pass

class MercadoPago(MedioDePago):
    
    def __init__(self):
        self.descripcion = 'Mercado pago'
    
    def pagar(self, monto):
        return None
    
    def obtener_descripcion(self):
        return self.descripcion

class Tarjeta(MedioDePago):
    
    def __init__(self):
        self.descripcion = 'Tarjeta'
    
    def pagar(self, monto):
        return None
    
    def obtener_descripcion(self):
        return self.descripcion

class Efectivo(MedioDePago):
    
    def __init__(self):
        self.descripcion = 'Efectivo'
    
    def pagar(self, monto):
        return None
    
    def obtener_descripcion(self):
        return self.descripcion