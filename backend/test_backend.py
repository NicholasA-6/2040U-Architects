import random
from typing import NamedTuple
import backend.user
import backend.watch
import backend.admin
import backend.role
import backend.catalogue

# class WatchData(NamedTuple):
#     watch_id: int
#     name:

def test_user(user = None):
    if user is None:
        data = {
            "user_id": random.randint(0, 99999999),
            "username": random.randint(0, 9999),
            "password_hash": random.randint(0, 9999),
            "role": backend.role.Role.USER
        }
        testing_user = backend.user.User(data.get("user_id"), data.get("username"), data.get("password_hash"), data.get("role"))
    else:
        data = {
            "user_id": user.user_id,
            "username": user.username,
            "password_hash": user.password_hash,
            "role": user.role
        }
        testing_user = user
    assert testing_user.login(data.get("username"), data.get("password_hash"))
    assert testing_user.is_loggedin()
    testing_user.logout()
    assert not testing_user.is_loggedin()
    for i in range(0, 50):
        num = random.randbytes(100)
        if i != data.get("username") and i != data.get("password_hash"):
            assert not testing_user.login(num, num) and not testing_user.is_loggedin()

def test_admin():
    data = {
        "user_id": random.randint(0, 99999999),
        "username": random.randint(0, 9999),
        "password_hash": random.randint(0, 9999),
        "role": backend.role.Role.USER
    }
    watchdata = WatchData
    testing_admin = backend.admin.Admin(data.get("user_id"),
                                        data.get("username"),
                                        data.get("password_hash"),
                                        data.get("role"))
    test_user(testing_admin)
    catalogue = backend.catalogue.Catalogue()
    watch = backend.watch.Watch(watchdata.watch_id, watchdata.name, watchdata.brand,
                                watchdata.display_type,
                                watchdata.price,
                                watchdata.case_shape,
                                watchdata.certification,
                                watchdata.image_url)
    assert testing_admin.login(data.get("username"), data.get("password_hash"))
    try:
        testing_admin.add_watch(watch, catalogue)
        assert True
    except PermissionError:
        assert False
    testing_admin.logout()
    watch.watch_id += 1
    try:
        testing_admin.add_watch(watch, catalogue)
        assert False
    except PermissionError:
        assert True

def test_catalogue():
    catalogue = backend.catalogue.Catalogue()

    for i in range(0, 50):
        watchdata = WatchData
        watch = backend.watch.Watch(i, watchdata.name, watchdata.brand,
                                    watchdata.display_type,
                                    watchdata.price,
                                    watchdata.case_shape,
                                    watchdata.certification,
                                    watchdata.image_url)
        catalogue.add_watch(watch)
    watches = catalogue.get_all_watches()
    assert len(watches) == 50
    watch = watches[49]
    try:
        catalogue.add_watch(watch)
        assert False
    except ValueError:
        assert True

# def test_watch():
#     watchdata = WatchData
#     watch = backend.watch.Watch(watchdata.watch_id, watchdata.name, watchdata.brand,
#                                 watchdata.display_type,
#                                 watchdata.price,
#                                 watchdata.case_shape,
#                                 watchdata.certification,
#                                 watchdata.image_url)
#     watch.update

class WatchData:
    watch_id = random.randint(0, 99999999)
    name = random.randint(0, 9999)
    brand = random.randint(0, 9999)
    display_type = random.randint(0, 3)
    price = random.randint(0, 9999)
    case_shape = random.randint(0, 9999)
    certification = random.randint(0, 9999)
    image_url = random.randbytes(100)
