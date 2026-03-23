from app import catalogue, add_watch
from backend import *
import random

class TestWatch:
    def test_watch_creation(self):
        Watch(None, None, None, None, None, None, None, None)

    def test_watch_init(self):
        i = random_bytes(8, 4)
        watch = Watch(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
        assert watch.watch_id == i[0]
        assert watch.name == i[1]
        assert watch.brand == i[2]
        assert watch.price == i[3]
        assert watch.material == i[4]
        assert watch.reference == i[5]
        assert watch.condition == i[6]
        assert watch.image_url == i[7]

    def test_watch_get_details(self):
        i = random_bytes(8, 4)
        watch = Watch(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
        assert watch.get_details() == {
            "watch_id": i[0],
            "name": i[1],
            "brand": i[2],
            "price": i[3],
            "material": i[4],
            "reference": i[5],
            "condition": i[6],
            "image_url": i[7],
        }

    def test_watch_string(self):
        i = random_bytes(8, 4)
        watch = Watch(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
        assert str(watch) == f"{i[0]} - {i[1]} ({i[2]}) - ${i[3]}"

    def test_watch_large_data(self):
        i = random_bytes(8, 999999)
        watch = Watch(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])

class TestUser:
    def test_user_creation(self):
        User(None, None, None, None)

    def test_user_init(self):
        i = random_bytes(3, 8)
        user = User(i[0], i[1], i[2])
        assert user.user_id == i[0]
        assert user.username == i[1]
        assert user.password_hash == i[2]

    def test_user_login_logout(self):
        i = random_bytes(3, 8)
        user = User(i[0], i[1], i[2])
        assert user.login(i[1], i[2])
        assert user.logged_in is True
        user.logout()
        assert user.logged_in is False
        assert user.login(i[1] + b"1", i[2]) is False

class TestCatalogue:
    def test_catalogue_creation(self):
        Catalogue()

    def test_catalogue_init(self):
        catalogue = Catalogue()
        assert len(catalogue.watches) == 0

class TestAdmin:
    def test_admin_creation(self):
        Admin(None, None, None)

    def test_admin_init(self):
        i = random_bytes(3, 8)
        admin = Admin(i[0], i[1], i[2])
        assert admin.user_id == i[0]
        assert admin.username == i[1]
        assert admin.password_hash == i[2]

    def test_admin_add_watch(self):
        catalogue = Catalogue()
        i = random_bytes(8, 4)
        watch = Watch(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
        j = random_bytes(3, 8)
        admin = Admin(j[0], j[1], j[2])
        try:
            admin.add_watch(watch, catalogue)
            raise Exception
        except PermissionError:
            pass
        admin.login(j[1], j[2])
        try:
            admin.add_watch(watch, catalogue)
        except PermissionError:
            raise Exception



def random_bytes(entries, n):
    i = []
    for x in range(0, entries):
        i.append(random.randbytes(n))
    return i