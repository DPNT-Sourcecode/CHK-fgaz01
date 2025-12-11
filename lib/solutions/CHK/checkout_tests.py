from checkout_solution import CheckoutSolution
import unittest

class TestCheckout(unittest.TestCase):
    supermarket = CheckoutSolution()

    def test_single_item_basket(self):
        self.assertEqual(self.supermarket.checkout("AAA"),130)

    def test_single_item_basket_2(self):
        self.assertEqual(self.supermarket.checkout("CC"),40)

    def test_multi_item_basket(self):
        self.assertEqual(self.supermarket.checkout("ABCDEABCDE"),280)

    def test_multi_Item_basket_2(self):
        self.assertEqual(self.supermarket.checkout("CCADDEEBBA"),280)

    def test_multi_item_basket_with_deals(self):
        self.assertEqual(self.supermarket.checkout("AAAAAEEBAAABB"),455)

    def test_multi_item_basket_with_deals_2(self):
        self.assertEqual(self.supermarket.checkout("ABCDECBAABCABBAAAEEAA"),665)

    def test_buy_one_get_one_free(self):
        self.assertEqual(self.supermarket.checkout("FFFFFF"),40)

    def test_buy_one_get_one_free_2(self):
        self.assertEqual(self.supermarket.checkout("FFABCDECBAABCABBAAAEEAAFF"),695)

    def test_multi_deals(self):
        self.assertEqual(self.supermarket.checkout("NNNM"),120)
    
    def test_multi_deals_2(self):
        self.assertEqual(self.supermarket.checkout("NNNNM"),160)

    def test_multi_deals_3(self):
        self.assertEqual(self.supermarket.checkout("NNNNNNMM"),240)

if __name__ == "__main__":
    unittest.main()