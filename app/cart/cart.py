from shop.models import Item


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

    def get_items(self):
        cart_items = []
        for item_id, item_data in self.cart.items():
            item = Item.objects.get(pk=item_id)
            qty = item_data.get('qty')
            cart_items.append({
                'item': item,
                'quantity': qty,
            })
        cart_items = sorted(cart_items, key=lambda x: x['item'].created_at)
        return cart_items

    def get_total_price(self):
        total_price = sum(
            [it['quantity']*it['item'].price for it in self.get_items()]
            )
        return total_price
