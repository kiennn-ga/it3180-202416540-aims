import unittest

from aims.cart import Cart
from aims.dvd import DigitalVideoDisc


class CartSortTest(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        self.star_wars = DigitalVideoDisc("Star Wars", cost=24.95)
        self.aladdin = DigitalVideoDisc("Aladdin", cost=18.99)
        self.lion_king = DigitalVideoDisc("The Lion King", cost=19.95)
        for dvd in (self.star_wars, self.lion_king, self.aladdin):
            self.cart.add_dvd(dvd)

    def test_sort_by_title(self):
        self.cart.sort_by_title()
        self.assertEqual(
            self.cart.items, [self.aladdin, self.star_wars, self.lion_king]
        )
        self.assertAlmostEqual(self.cart.total_cost(), 63.89)

    def test_sort_by_cost(self):
        self.cart.sort_by_cost()
        self.assertEqual(
            self.cart.items, [self.aladdin, self.lion_king, self.star_wars]
        )
        self.assertAlmostEqual(self.cart.total_cost(), 63.89)

    def test_sort_empty_cart(self):
        cart = Cart()
        cart.sort_by_title()
        cart.sort_by_cost()
        self.assertEqual(cart.items, [])

    def test_sort_preserves_equal_cost_order(self):
        self.star_wars.cost = self.lion_king.cost
        self.cart.sort_by_cost()
        self.assertEqual(
            self.cart.items, [self.aladdin, self.star_wars, self.lion_king]
        )


if __name__ == "__main__":
    unittest.main()
