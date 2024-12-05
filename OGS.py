import datetime

# User Class
class User:
    def __init__(self, username, password, address):
        self.username = username
        self.password = password
        self.address = address
        self.cart = []
        self.orders = []
        self.wishlist = []  # Initialize wishlist
        self.discount = 0  # Initialize discount

    def add_to_cart(self, item):
        self.cart.append(item)

    def checkout(self):
        if not self.cart:
            print("Your cart is empty. Add items to your cart first.")
            return
        order = Order(self.username, self.cart, self.address)
        self.orders.append(order)
        self.cart = []
        print(f"Order placed successfully! Delivery address: {self.address}")

    def apply_coupon(self, coupon_code):
        valid_coupons = {"DISCOUNT10": 10, "SALE20": 20}  # Example coupons
        if coupon_code in valid_coupons:
            self.discount = valid_coupons[coupon_code]
            print(f"Coupon applied! You get {self.discount}% off.")
        else:
            print("Invalid coupon code.")
    
    def calculate_total(self):
        total = sum([item.price for item in self.cart])
        total -= (total * self.discount / 100)
        return total
    
    def display_order_history(self):
        if not self.orders:
            print("No orders yet.")
            return
        for order in self.orders:
            order.display_order_details()
    
    def add_to_wishlist(self, product):
        self.wishlist.append(product)
        print(f"{product.name} added to your wishlist.")

    def view_wishlist(self):
        if not self.wishlist:
            print("Your wishlist is empty.")
            return
        print("\nYour Wishlist:")
        for product in self.wishlist:
            print(f"- {product.name} - ${product.price}")

# Product Class
class Product:
     def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

     def update_stock(self, quantity):
        self.stock -= quantity

     def add_review(self, review, rating):
        self.reviews.append({"review": review, "rating": rating})

     def display_reviews(self):
        if not self.reviews:
            print("No reviews yet.")
            return
        for review in self.reviews:
            print(f"Rating: {review['rating']} - Review: {review['review']}")

# Order Class
class Order:
    def __init__(self, username, cart, address):
        self.username = username
        self.cart = cart
        self.address = address
        self.order_date = datetime.datetime.now()
        self.delivery_date = self.order_date + datetime.timedelta(days=3)
        self.status = "Processing"

    def display_order_details(self):
        print(f"Order by {self.username}")
        for item in self.cart:
            print(f"Item: {item.name}, Price: {item.price}, Quantity: 1")
        print(f"Delivery Address: {self.address}")
        print(f"Order Date: {self.order_date}")
        print(f"Estimated Delivery: {self.delivery_date}")
        print(f"Order Status: {self.status}")
        print()

    def __init__(self, username, cart, address):
        self.username = username
        self.cart = cart
        self.address = address
        self.order_date = datetime.datetime.now()
        self.delivery_date = self.order_date + datetime.timedelta(days=3)
        self.status = "Processing"

    def cancel_order(self):
        if self.status == "Processing":
            self.status = "Cancelled"
            print("Your order has been cancelled.")
        else:
            print("Cannot cancel. The order is already shipped.")
    def update_status(self, status):
        self.status = status
        print(f"Order status updated to: {self.status}")
    
    def track_order(self):
        print(f"Order status: {self.status}")
        print(f"Estimated Delivery: {self.delivery_date}")

# Grocery Store Class
class GroceryStore:
    def __init__(self):
        self.products = []
        self.users = {}
        self.logged_in_user = None
        self.admin = "admin_username"  # Set admin username

    def add_product(self, product):
        self.products.append(product)

    def register_user(self, username, password, address):
        if username in self.users:
            print(f"Username {username} already exists.")
            return
        user = User(username, password, address)
        self.users[username] = user
        print(f"User {username} registered successfully.")

    def login_user(self, username, password):
        if username not in self.users:
            print(f"User {username} not found.")
            return False
        user = self.users[username]
        if user.password == password:
            self.logged_in_user = user
            print(f"Welcome {username}!")
            return True
        else:
            print("Invalid password.")
            return False

    def display_products(self):
        if not self.products:
            print("No products available.")
            return
        print("\nAvailable Products:")
        for idx, product in enumerate(self.products, 1):
            print(f"{idx}. {product.name} - ${product.price} (Stock: {product.stock})")
    
    def search_product(self, search_query):
        print(f"Searching for: {search_query}")  # Debugging
        print(f"Available products: {[product.name for product in self.products]}")  # Debugging

        found = False
        for product in self.products:
            if search_query.lower() in product.name.lower():  # Match query in product names
                print(f"Product: {product.name}, Price: ${product.price}, Stock: {product.stock}")
                found = True
        if not found:
            print("No products found matching your search.")



    def add_to_cart(self, product_index, quantity):
        if not self.logged_in_user:
            print("Please log in to add items to your cart.")
            return
        product = self.products[product_index - 1]
        if product.stock >= quantity:
            product.update_stock(quantity)
            self.logged_in_user.add_to_cart(product)
            print(f"{product.name} added to your cart.")
        else:
            print(f"Not enough stock for {product.name}. Only {product.stock} available.")

    def view_cart(self):
        if not self.logged_in_user:
            print("Please log in to view your cart.")
            return
        if not self.logged_in_user.cart:
            print("Your cart is empty.")
            return
        print("\nYour Cart:")
        for item in self.logged_in_user.cart:
            print(f"- {item.name} - ${item.price}")

    def checkout(self):
        if not self.logged_in_user:
            print("Please log in to checkout.")
            return
        self.logged_in_user.checkout()

    def view_orders(self):
        if not self.logged_in_user:
            print("Please log in to view your orders.")
            return
        if not self.logged_in_user.orders:
            print("You have no orders yet.")
            return
        for order in self.logged_in_user.orders:
            order.display_order_details()

    def add_product_by_admin(self, name, price, stock):
        if self.logged_in_user and self.logged_in_user.username == self.admin:
            product = Product(name, price, stock)
            self.products.append(product)
            print(f"Product {name} added by admin.")
        else:
            print("You must be an admin to add products.")

    def remove_product_by_admin(self, product_name):
        if self.logged_in_user and self.logged_in_user.username == self.admin:
            product_to_remove = next((p for p in self.products if p.name == product_name), None)
            if product_to_remove:
                self.products.remove(product_to_remove)
                print(f"Product {product_name} removed by admin.")
            else:
                print("Product not found.")
        else:
            print("You must be an admin to remove products.")

    def check_inventory(self):
        for product in self.products:
            if product.stock < 10:
                print(f"Low stock alert: {product.name} - only {product.stock} left.")

# Main Function
def main():
    store = GroceryStore()
    
    # Adding some initial products
    store.add_product(Product("Apple", 1.0, 100))
    store.add_product(Product("Banana", 0.5, 50))
    store.add_product(Product("Carrot", 1.2, 30))
    store.add_product(Product("Broccoli", 2.5, 20))
    store.add_product(Product("Orange", 0.8, 60))
    store.add_product(Product("Potato", 0.4, 200))
    store.add_product(Product("Tomato", 1.0, 150))
    store.add_product(Product("Cucumber", 0.9, 40))
    store.add_product(Product("Milk (1L)", 1.5, 80))
    store.add_product(Product("Eggs (12-pack)", 3.0, 50))
    store.add_product(Product("Bread (Loaf)", 2.0, 100))
    store.add_product(Product("Butter (500g)", 3.5, 25))
    store.add_product(Product("Rice (1kg)", 2.8, 100))
    store.add_product(Product("Pasta (500g)", 2.0, 75))
    store.add_product(Product("Chicken (1kg)", 6.0, 40))
    store.add_product(Product("Beef (1kg)", 8.0, 30))
    store.add_product(Product("Fish (1kg)", 7.5, 20))
    store.add_product(Product("Coke (2L)", 2.5, 90))

    while True:
        print("\n=== Online Grocery Delivery System ===")
        print("1. Register")
        print("2. Login")
        print("3. View Products")
        print("4. Search Product")
        print("5. Add to Cart")
        print("6. View Cart")
        print("7. Apply Discount Coupon")
        print("8. Checkout")
        print("9. View Orders")
        print("10. Cancel Order")
        print("11. Track Order")
        print("12. View Wishlist")
        print("13. Add to Wishlist")
        print("14. Admin: Add Product")
        print("15. Admin: Remove Product")
        print("16. Check Inventory (Admin)")
        print("17. Logout")
        print("18. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":  # Register
            username = input("Enter username: ")
            password = input("Enter password: ")
            address = input("Enter your address: ")
            store.register_user(username, password, address)

        elif choice == "2":  # Login
            username = input("Enter username: ")
            password = input("Enter password: ")
            if store.login_user(username, password):
                continue

        elif choice == "3":  # View Products
            store.display_products()

        elif choice == "4":  # Search Product
            search_query = input("Enter product name to search: ")
            store.search_product(search_query)

        elif choice == "5":  # Add to Cart
            product_index = int(input("Enter product index to add to cart: "))
            quantity = int(input("Enter quantity: "))
            store.add_to_cart(product_index, quantity)

        elif choice == "6":  # View Cart
            store.view_cart()

        elif choice == "7":  # Apply Discount Coupon
            if store.logged_in_user:
                coupon_code = input("Enter coupon code: ")
                store.logged_in_user.apply_coupon(coupon_code)
            else:
                print("Please log in to apply a coupon.")

        elif choice == "8":  # Checkout
            store.checkout()

        elif choice == "9":  # View Orders
            store.view_orders()

        elif choice == "10":  # Cancel Order
            if store.logged_in_user:
                if store.logged_in_user.orders:
                    order_id = int(input("Enter order index to cancel: ")) - 1
                    if 0 <= order_id < len(store.logged_in_user.orders):
                        store.logged_in_user.orders[order_id].cancel_order()
                    else:
                        print("Invalid order index.")
                else:
                    print("You have no orders to cancel.")
            else:
                print("Please log in to cancel an order.")

        elif choice == "11":  # Track Order
            if store.logged_in_user:
                if store.logged_in_user.orders:
                    order_id = int(input("Enter order index to track: ")) - 1
                    if 0 <= order_id < len(store.logged_in_user.orders):
                        store.logged_in_user.orders[order_id].track_order()
                    else:
                        print("Invalid order index.")
                else:
                    print("You have no orders to track.")
            else:
                print("Please log in to track an order.")

        elif choice == "12":  # View Wishlist
            if store.logged_in_user:
                store.logged_in_user.view_wishlist()
            else:
                print("Please log in to view your wishlist.")

        elif choice == "13":  # Add to Wishlist
            if store.logged_in_user:
                product_index = int(input("Enter product index to add to wishlist: "))
                if 0 < product_index <= len(store.products):
                    product = store.products[product_index - 1]
                    store.logged_in_user.add_to_wishlist(product)
                else:
                    print("Invalid product index.")
            else:
                print("Please log in to add items to your wishlist.")

        elif choice == "14":  # Admin: Add Product
            if store.logged_in_user and store.logged_in_user.username == store.admin:
                name = input("Enter product name: ")
                price = float(input("Enter product price: "))
                stock = int(input("Enter product stock: "))
                store.add_product_by_admin(name, price, stock)
            else:
                print("You must be an admin to add products.")

        elif choice == "15":  # Admin: Remove Product
            if store.logged_in_user and store.logged_in_user.username == store.admin:
                product_name = input("Enter product name to remove: ")
                store.remove_product_by_admin(product_name)
            else:
                print("You must be an admin to remove products.")

        elif choice == "16":  # Admin: Check Inventory
            if store.logged_in_user and store.logged_in_user.username == store.admin:
                store.check_inventory()
            else:
                print("You must be an admin to check inventory.")

        elif choice == "17":  # Logout
            store.logged_in_user = None
            print("Logged out successfully.")

        elif choice == "18":  # Exit
            print("Thank you for using the Online Grocery Delivery System!")
            break

        else:
            print("Invalid choice. Please try again.")



