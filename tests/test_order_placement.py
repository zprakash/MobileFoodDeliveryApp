import unittest
from unittest import mock  # Import the mock module for simulating payment failures in tests.

from Order_Placement import OrderPlacement, Cart, UserProfile, RestaurantMenu, PaymentMethod

class TestOrderPlacement(unittest.TestCase):
    """
    Unit tests for the OrderPlacement class.
    """
    def setUp(self):
        """
        Sets up the test environment by creating instances of necessary classes.
        """
        self.restaurant_menu = RestaurantMenu(available_items=["Burger", "Pizza", "Salad"])
        self.user_profile = UserProfile(delivery_address="123 Main St")
        self.cart = Cart()
        self.order = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)

    def test_validate_order_empty_cart(self):
        """
        Test case for validating an order with an empty cart.
        """
        result = self.order.validate_order()
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Cart is empty")

    def test_validate_order_item_not_available(self):
        """
        Test case for validating an order with an unavailable item.
        """
        self.cart.add_item("Pasta", 15.99, 1)
        result = self.order.validate_order()
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Pasta is not available")

    def test_validate_order_success(self):
        """
        Test case for successfully validating an order.
        """
        self.cart.add_item("Burger", 8.99, 2)
        result = self.order.validate_order()
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order is valid")

    def test_confirm_order_success(self):
        """
        Test case for confirming an order with successful payment.
        """
        self.cart.add_item("Pizza", 12.99, 1)
        payment_method = PaymentMethod()
        result = self.order.confirm_order(payment_method)
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order confirmed")
        self.assertEqual(result["order_id"], "ORD123456")

    def test_confirm_order_failed_payment(self):
        """
        Test case for confirming an order with failed payment.
        """
        self.cart.add_item("Pizza", 12.99, 1)
        payment_method = PaymentMethod()

        # Use unittest.mock.patch to simulate failed payment processing.
        with mock.patch.object(payment_method, 'process_payment', return_value=False):
            result = self.order.confirm_order(payment_method)
            self.assertFalse(result["success"])
            self.assertEqual(result["message"], "Payment failed")

if __name__ == "__main__":
    unittest.main()
