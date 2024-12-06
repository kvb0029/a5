
import unittest
from io import StringIO
import sys

from OGS import GroceryStore, Product
class TestGroceryStore(unittest.TestCase):

    def setUp(self):
        # Create a new GroceryStore instance for testing
        self.store = GroceryStore()
        # Add some initial products
        self.store.add_product(Product("Apple", 1.0, 100))
        self.store.add_product(Product("Banana", 0.5, 50))
        self.store.register_user("admin_username", "admin123", "Admin Address")  # Admin setup

    def capture_output(self, func, *args):
        """Helper method to capture printed output."""
        captured_output = StringIO()
        sys.stdout = captured_output
        func(*args)
        sys.stdout = sys.__stdout__
        return captured_output.getvalue()
    def setUp(self):
        # Create a new GroceryStore instance for testing
        self.store = GroceryStore()
        # Add some initial products
        self.store.add_product(Product("Apple", 1.0, 100))
        self.store.add_product(Product("Banana", 0.5, 50))
        self.store.register_user("admin_username", "admin123", "Admin Address")  # Admin setup

    def capture_output(self, func, *args):
        """Helper method to capture printed output."""
        captured_output = StringIO()
        sys.stdout = captured_output
        func(*args)
        sys.stdout = sys.__stdout__
        return captured_output.getvalue()

    # Test cases for user registration
    def test_register_user(self):
        output = self.capture_output(self.store.register_user, "user1", "pass123", "123 Street")
        self.assertIn("User user1 registered successfully.", output)
        output = self.capture_output(self.store.register_user, "user1", "pass123", "123 Street")
        self.assertIn("Username user1 already exists.", output)

    # Test cases for user login
    def test_login_user(self):
        self.store.register_user("user1", "pass123", "123 Street")
        output = self.capture_output(self.store.login_user, "user1", "pass123")
        self.assertIn("Welcome user1!", output)
        output = self.capture_output(self.store.login_user, "user1", "wrongpass")
        self.assertIn("Invalid password.", output)
        output = self.capture_output(self.store.login_user, "unknown", "pass123")
        self.assertIn("User unknown not found.", output)

    # Test cases for viewing products
    def test_view_products(self):
        output = self.capture_output(self.store.display_products)
        self.assertIn("Apple - $1.0", output)
        self.assertIn("Banana - $0.5", output)

    # Test cases for searching products
    def test_search_product(self):
        output = self.capture_output(self.store.search_product, "Apple")
        self.assertIn("Product: Apple, Price: $1.0, Stock: 100", output)
        output = self.capture_output(self.store.search_product, "Mango")
        self.assertIn("No products found matching your search.", output)

    # Test cases for adding to cart
    def test_add_to_cart(self):
        self.store.register_user("user1", "pass123", "123 Street")
        self.store.login_user("user1", "pass123")
        output = self.capture_output(self.store.add_to_cart, 1, 2)  # Add 2 Apples
        self.assertIn("Apple added to your cart.", output)
        output = self.capture_output(self.store.add_to_cart, 1, 101)  # Exceed stock
        self.assertIn("Not enough stock for Apple. Only 98 available.", output)

    # Test cases for applying coupon
    def test_apply_coupon(self):
        self.store.register_user("user1", "pass123", "123 Street")
        self.store.login_user("user1", "pass123")
        output = self.capture_output(self.store.logged_in_user.apply_coupon, "DISCOUNT10")
        self.assertIn("Coupon applied! You get 10% off.", output)
        output = self.capture_output(self.store.logged_in_user.apply_coupon, "INVALID")
        self.assertIn("Invalid coupon code.", output)

    # Test cases for admin functionalities
    def test_admin_add_product(self):
        self.store.login_user("admin_username", "admin123")
        output = self.capture_output(self.store.add_product_by_admin, "Mango", 2.5, 50)
        self.assertIn("Product Mango added by admin.", output)
        output = self.capture_output(self.store.add_product_by_admin, "Pineapple", 3.0, 30)
        self.assertIn("Product Pineapple added by admin.", output)

    def test_admin_remove_product(self):
        self.store.login_user("admin_username", "admin123")
        output = self.capture_output(self.store.remove_product_by_admin, "Apple")
        self.assertIn("Product Apple removed by admin.", output)
        output = self.capture_output(self.store.remove_product_by_admin, "NonExistent")
        self.assertIn("Product not found.", output)

    def test_admin_check_inventory(self):
        self.store.login_user("admin_username", "admin123")
        self.store.products.append(Product("LowStockItem", 5.0, 5))  # Add low stock product
        output = self.capture_output(self.store.check_inventory)
        self.assertIn("Low stock alert: LowStockItem - only 5 left.", output)


if __name__ == "__main__":
    unittest.main()
