import unittest

from aims.dvd import DigitalVideoDisc
from aims.search import search_by_category


class CategorySearchTest(unittest.TestCase):
    def test_returns_all_matching_dvds_in_original_order(self):
        lion_king = DigitalVideoDisc("The Lion King", category="Animation")
        star_wars = DigitalVideoDisc("Star Wars", category="Science Fiction")
        aladdin = DigitalVideoDisc("Aladdin", category="Animation")
        items = [lion_king, star_wars, aladdin]
        self.assertEqual(
            search_by_category(items, "Animation"), [lion_king, aladdin]
        )
        self.assertEqual(items, [lion_king, star_wars, aladdin])

    def test_no_matching_category(self):
        items = [DigitalVideoDisc("Aladdin", category="Animation")]
        self.assertEqual(search_by_category(items, "Drama"), [])

    def test_empty_list(self):
        self.assertEqual(search_by_category([], "Animation"), [])


if __name__ == "__main__":
    unittest.main()
