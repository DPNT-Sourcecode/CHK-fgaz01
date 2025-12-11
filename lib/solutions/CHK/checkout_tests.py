from checkout_solution import CheckoutSolution
import unittest

class TestCheckout(unittest.TestCase):
    supermarket = CheckoutSolution()

    def test_singleItemBasket(self):
        self.assertEqual(self.supermarket.checkout("AAA"),130)

    def test_singleItemBasket2(self):
        self.assertEqual(self.supermarket.checkout("CC"),40)

    def test_multiItemBasket(self):
        self.assertEqual(self.supermarket.checkout("ABCDEABCDE"),280)

    def test_multiItemBasket2(self):
        self.assertEqual(self.supermarket.checkout("CCADDEEBBA"),280)

    def test_multiItemBasketWithDeals(self):
        self.assertEqual(self.supermarket.checkout("AAAAAEEBAAABB"),455)

    def test_multiItemBasketWithDeals2(self):
        self.assertEqual(self.supermarket.checkout("ABCDECBAABCABBAAAEEAA"),665)

    def test_buyOneGetOneFree(self):
        self.assertEqual(self.supermarket.checkout("CCADDEEBBA"),280)

     def test_multiItemBasket2(self):
        self.assertEqual(self.supermarket.checkout("CCADDEEBBA"),280)
