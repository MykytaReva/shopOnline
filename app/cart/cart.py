class CookiesCart:
    '''
    Store cart items in cookies for anonymous users
    '''

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.session = self.request.session
        cart = self.session.get('cart', {})
        self.cart = cart

    def add(self, item):
        product_id = str(item.id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] += 1
        else:
            self.cart[product_id] = {'qty': 1}

        self.session['cart'] = self.cart
        self.save()

    def subtract(self, item):
        product_id = str(item.id)

        if product_id in self.cart:
            if self.cart[product_id]['qty'] > 1:
                self.cart[product_id]['qty'] -= 1
            else:
                del self.cart[product_id]
            self.session['cart'] = self.cart
            self.save()

    def delete(self, item):
        product_id = str(item.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session['cart'] = self.cart
            self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def save(self):
        self.session.modified = True
