# SDK de Mercado Pago
import mercadopago
from flask import session, Flask, flash, render_template, request, redirect, url_for

class PagosController:
    def __init__(self, app):
        self.app = app
        # Agrega access token de aplicacion de mercado pago
        self.sdk = mercadopago.SDK("TEST-2662247305576876-112118-aef012964bf37797f2668f83221e4db7-418530695")
        self.register_routes()
    
    def register_routes(self):
        self.app.add_url_rule('/checkout', 'checkout', self.checkout, methods=['POST'])
    
    def checkout(self):    
        items = []
        print(f'Sesion cart: {session["cart"]}')
        for product in session["cart"]:
            items.append({
                "title": product["name"],
                "description": product["descripcion"],
                "unit_price": float(product["price"].replace('$','').replace(',', '')),
                "currency_id": "ARS",
                "quantity": product["quantity"],
            })
        print(f"Items: {items}")

        preference_data = {
            "items": items,
            "payer": {
                "name": "João",
                "surname": "Silva",
                "email": "user@email.com",
                "phone": {
                    "area_code": "11",
                    "number": "4444-4444"
                },
                "identification": {
                    "type": "CPF",
                    "number": "19119119100"
                },
                "address": {
                    "street_name": "Street",
                    "street_number": 123,
                    "zip_code": "06233200"
                }
            },
            "back_urls": {
                "success": "http://localhost:5000/",
                "failure": "http://localhost:5000/",
                "pending": "http://localhost:5000/productos"
            },
            "auto_return": "approved",
            "payment_methods": {
            "excluded_payment_methods": [],
            "excluded_payment_types": [],
            "installments": 3
            }
        }

        reference_response = self.sdk.preference().create(preference_data)
        preference_id = reference_response['response']['id']

        session["preferenceId"] = preference_id
        # Puedes redirigir a otra página después de procesar los datos
        return render_template('mercadoPago.html')