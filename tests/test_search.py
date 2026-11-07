import unittest

from aims.dvd import DigitalVideoDisc
from aims.search import search_by_title


class TitleSearchTest(unittest.TestCase):
    def test_search_ignores_case_and_preserves_order(self):
        lion_king = DigitalVideoDisc("The Lion King")
        lion = DigitalVideoDisc("LION")
        aladdin = DigitalVideoDisc("Aladdin")
        items = [lion_king, aladdin, lion]
        for keyword in ("lion", "LION", "LiOn"):
            with self.subTest(keyword=keyword):
                self.assertEqual(
                    search_by_title(items, keyword), [lion_king, lion]
                )
        self.assertEqual(items, [lion_king, aladdin, lion])

    def test_search_returns_no_matches(self):
        self.assertEqual(
            search_by_title([DigitalVideoDisc("Aladdin")], "lion"), []
        )

    def test_search_empty_list(self):
        self.assertEqual(search_by_title([], "lion"), [])


if __name__ == "__main__":
    unittest.main()
