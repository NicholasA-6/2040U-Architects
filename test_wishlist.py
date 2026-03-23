import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend import User
from backend import Role
from backend import Watch


class TestWishlistRed(unittest.TestCase):
    def test_user_can_add_watch_to_wishlist(self):
        user = User(1, "user", "1234", Role.USER)
        watch = Watch(
    101,
    "Seiko 5 Sports",
    "Seiko",
    "Automatic",
    "Analog",
    399.99,
    "Round",
    "Water Resistant",
    "url"
)

        user.add_to_wishlist(watch)

        self.assertIn(watch, user.get_wishlist())


if __name__ == "__main__":
    unittest.main()