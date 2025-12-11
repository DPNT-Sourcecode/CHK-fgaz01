from checkout_solution import CheckoutSolution
import unittest

class TestCheckout(unittest.TestCase):
    supermarket = CheckoutSolution()

    # ----------------------------------------
    # Basic single-item or simple baskets
    # ----------------------------------------
    def test_single_item_A_offer(self):
        self.assertEqual(self.supermarket.checkout("AAA"), 130)

    def test_single_item_C_offer(self):
        self.assertEqual(self.supermarket.checkout("CC"), 40)

    # ----------------------------------------
    # Mixed baskets with multiple items and offers
    # ----------------------------------------
    def test_multi_item_basket(self):
        self.assertEqual(self.supermarket.checkout("ABCDEABCDE"), 280)

    def test_multi_item_basket_2(self):
        self.assertEqual(self.supermarket.checkout("CCADDEEBBA"), 280)

    def test_multi_item_with_deals(self):
        self.assertEqual(self.supermarket.checkout("AAAAAEEBAAABB"), 455)

    def test_multi_item_with_deals_2(self):
        self.assertEqual(self.supermarket.checkout("ABCDECBAABCABBAAAEEAA"), 665)

    # ----------------------------------------
    # Buy-one-get-one and special pair deals
    # ----------------------------------------
    def test_bogo_F(self):
        self.assertEqual(self.supermarket.checkout("FFFFFF"), 40)

    def test_bogo_F_with_mixed_basket(self):
        self.assertEqual(self.supermarket.checkout("FFABCDECBAABCABBAAAEEAAFF"), 695)

    # ----------------------------------------
    # Multi-item dependent deals (N → M free, etc.)
    # ----------------------------------------
    def test_multi_deals(self):
        self.assertEqual(self.supermarket.checkout("NNNM"), 120)

    def test_multi_deals_2(self):
        self.assertEqual(self.supermarket.checkout("NNNNM"), 160)

    def test_multi_deals_3(self):
        self.assertEqual(self.supermarket.checkout("NNNNNNMM"), 240)

    # ----------------------------------------
    # Group bundles (S, T, X, Y, Z mix-and-match)
    # ----------------------------------------
    def test_group_bundle_basic(self):
        self.assertEqual(self.supermarket.checkout("STX"), 45)

    def test_group_bundle_two_groups(self):
        self.assertEqual(self.supermarket.checkout("STXSTX"), 90)

    def test_group_bundle_mixed_priority(self):
        self.assertEqual(self.supermarket.checkout("SSTX"), 62)

    def test_group_bundle_with_other_items(self):
        self.assertEqual(self.supermarket.checkout("ABST"), 120)

    def test_group_bundle_SSS(self):
        self.assertEqual(self.supermarket.checkout("SSS"), 45)

    def test_group_bundle_SSSZ(self):
        self.assertEqual(self.supermarket.checkout("SSSZ"), 65)

    def test_group_bundle_ZZZ(self):
        self.assertEqual(self.supermarket.checkout("ZZZ"), 45)


if __name__ == "__main__":
    unittest.main()
