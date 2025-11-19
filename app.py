from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Linked List Classes
class ItemNode:
    def __init__(self, name, qty, unit_price):
        self.name = name
        self.qty = qty
        self.unit_price = unit_price
        self.subtotal = qty * unit_price
        self.next = None

class ItemList:
    def __init__(self):
        self.head = None

    def append(self, name, qty, unit_price):
        if name.strip() == "" or qty <= 0 or unit_price < 0:
            return  
        new_node = ItemNode(name, qty, unit_price)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def traverse(self):
        current = self.head
        while current:
            yield current
            current = current.next

    def calculate_total(self):
        return sum(node.subtotal for node in self.traverse())


# Flask Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', 'Guest').strip() or "Guest"
        items = ItemList()

        names = request.form.getlist('item_name')
        qtys = request.form.getlist('qty')
        prices = request.form.getlist('unit_price')

        
        for name, qty, price in zip(names, qtys, prices):
            try:
                qty = int(qty) if qty else 0
                price = float(price) if price else 0.0
            except ValueError:
                qty, price = 0, 0.0
            items.append(name, qty, price)

        
        
        tax_input = request.form.get('tax', '').strip()
        discount_input = request.form.get('discount', '').strip()

        try:
            tax_percent = float(tax_input) if tax_input else 0.0
        except ValueError:
            tax_percent = 0.0

        try:
            discount_percent = float(discount_input) if discount_input else 0.0
        except ValueError:
            discount_percent = 0.0

        subtotal = items.calculate_total()
        tax_amount = subtotal * (tax_percent / 100)
        discount_amount = subtotal * (discount_percent / 100)
        grand_total = subtotal + tax_amount - discount_amount

        return render_template(
            'receipt.html',
            customer=customer_name,
            items=items.traverse(),
            subtotal=subtotal,
            tax=tax_amount,
            discount=discount_amount,
            grand_total=grand_total,
            tax_percent=tax_percent,
            discount_percent=discount_percent,
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
