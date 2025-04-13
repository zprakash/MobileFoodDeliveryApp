import unittest
from unittest import mock  # Import the mock module to simulate payment gateway responses.
from Payment_Processing import PaymentProcessing 

# Unit tests for PaymentProcessing class
class TestPaymentProcessing(unittest.TestCase):
    """
    Unit tests for the PaymentProcessing class to ensure payment validation and processing work correctly.
    """
    def setUp(self):
        """
        Sets up the test environment by creating an instance of PaymentProcessing.
        """
        self.payment_processing = PaymentProcessing()

    def test_validate_payment_method_success(self):
        """
        Test case for successful validation of a valid payment method ('credit_card') with valid details.
        """
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        result = self.payment_processing.validate_payment_method("credit_card", payment_details)
        self.assertTrue(result)

    def test_validate_payment_method_invalid_gateway(self):
        """
        Test case for validation failure due to an unsupported payment method ('bitcoin').
        """
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        with self.assertRaises(ValueError) as context:
            self.payment_processing.validate_payment_method("bitcoin", payment_details)
        self.assertEqual(str(context.exception), "Invalid payment method")

    def test_validate_credit_card_invalid_details(self):
        """
        Test case for validation failure due to invalid credit card details (invalid card number and CVV).
        """
        payment_details = {"card_number": "1234", "expiry_date": "12/25", "cvv": "12"}  # Invalid card number and CVV.
        result = self.payment_processing.validate_credit_card(payment_details)
        self.assertFalse(result)

    def test_process_payment_success(self):
        """
        Test case for successful payment processing using the 'credit_card' method with valid details.
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}

        # Use mock to simulate a successful payment response from the gateway.
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}):
            result = self.payment_processing.process_payment(order, "credit_card", payment_details)
            self.assertEqual(result, "Payment successful, Order confirmed")

    def test_process_payment_failure(self):
        """
        Test case for payment failure due to a declined credit card.
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1111222233334444", "expiry_date": "12/25", "cvv": "123"}  # Simulate a declined card.

        # Use mock to simulate a failed payment response from the gateway.
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "failure"}):
            result = self.payment_processing.process_payment(order, "credit_card", payment_details)
            self.assertEqual(result, "Payment failed, please try again")

    def test_process_payment_invalid_method(self):
        """
        Test case for payment processing failure due to an invalid payment method ('bitcoin').
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}

        # No need for mocking, the method will raise an error directly.
        result = self.payment_processing.process_payment(order, "bitcoin", payment_details)
        self.assertIn("Error: Invalid payment method", result)

    def test_validate_payment_method_missing_details(self):
        """
        Test case for validation failure due to missing credit card details (e.g., missing CVV).
        """
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25"}  # Missing 'cvv'
        with self.assertRaises(ValueError) as context:
            self.payment_processing.validate_payment_method("credit_card", payment_details)
        self.assertEqual(str(context.exception), "Invalid credit card details")

    def test_process_payment_paypal_success(self):
        """
        Test case for successful payment processing using the 'paypal' method.
        """
        order = {"total_amount": 50.00}
        payment_details = {"email": "user@example.com"}  # Simulated PayPal details

        # Use mock to simulate a successful PayPal payment response.
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}):
            result = self.payment_processing.process_payment(order, "paypal", payment_details)
            self.assertEqual(result, "Payment successful, Order confirmed")


if __name__ == "__main__":
    unittest.main()  # Run the unit tests.
