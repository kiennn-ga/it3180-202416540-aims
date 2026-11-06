import unittest

from aims.cart import Cart
from aims.dvd import DigitalVideoDisc


class CartTest(unittest.TestCase):
    def test_add_dvd_until_full(self):
        cart = Cart()
        for index in range(20):
            with self.subTest(dvd_number=index + 1):
                self.assertTrue(
                    cart.add_dvd(DigitalVideoDisc(f"DVD {index + 1}"))
                )
        self.assertEqual(len(cart.items), 20)

        extra_dvd = DigitalVideoDisc("DVD 21")
        with self.subTest(check="reject the 21st DVD"):
            self.assertFalse(cart.add_dvd(extra_dvd))
        with self.subTest(check="preserve cart contents"):
            self.assertEqual(len(cart.items), 20)
            self.assertNotIn(extra_dvd, cart.items)


if __name__ == "__main__":
    unittest.main()
