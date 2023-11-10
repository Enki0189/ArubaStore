class Producto:
    def __init__(self, id, nombre, descripcion, precio, stock, imagen):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen

    def transformar_a_json(self) :
        price_value = self.precio 
        formatted_price = "${:,.2f}".format(float(price_value))
       
        return {
            "id" : self.id,
            "name" : self.nombre,
            "descripcion" : self.descripcion,
            "imagen": self.imagen,
            "price": formatted_price
        }