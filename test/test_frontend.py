import copy
import pytest
from flask import Flask
import shutil
from WatchCatalogue import app
from WatchCatalogue.backend import *

# Creates an instance of the Flask app for testing
@pytest.fixture()
def app_create():
    app_created = app.app_start()
    yield app_created

# Creates a test client for the Flask app for testing
@pytest.fixture()
def client(app_create):
    return app_create.test_client()

# Tests starting the app
def test_start_app():
    app_instance = app.app_start()
    assert type(app_instance) == Flask

# Generates a test response from the client
def test_request_example():
    app_instance = app.app_start()
    client = app_instance.test_client()
    response = client.get("")
    print(response)

# Tests loading the watch data from the database
def test_load_watches_from_csv():
    shutil.copyfile(app.csv_path, "./test/testwatches.csv")
    catalogue = Catalogue()
    app.load_watches_from_csv("./test/testwatches.csv", catalogue)
    with open("./test/testwatches.csv", 'r') as file:
        for watch in catalogue.watches:
            for i, line in enumerate(file):
                if i != 0:
                    data = line.split(",")
                    if data[0] == watch.watch_id:
                        assert data[1] == watch.name
                        assert data[2] == watch.brand
                        assert data[3] == watch.price
                        assert data[4] == watch.material
                        assert data[5] == watch.reference
                        assert data[6] == watch.condition
                        assert data[7] == watch.image_url

# Tests saving the watches to the database
def test_save_watches_to_csv():
    shutil.copyfile(app.csv_path, "./test/testwatches.csv")
    catalogue = Catalogue()
    app.load_watches_from_csv("./test/testwatches.csv", catalogue)
    watch = Watch("10", "Test Watch", "Fancy Brand", "$500", "Gold", "1232389021", "New", "")
    catalogue.watches.append(watch)
    app.save_watches_to_csv('./test/testwatches.csv', catalogue.watches)
    with open("./test/testwatches.csv", 'r') as file:
        for i, line in enumerate(file):
            if i == len(catalogue.watches):
                data = line.split("[,\n]")
                if data[0] == watch.watch_id:
                    assert data[1] == watch.name
                    assert data[2] == watch.brand
                    assert data[3] == watch.price
                    assert data[4] == watch.material
                    assert data[5] == watch.reference
                    assert data[6] == watch.condition
                    assert data[7] == watch.image_url

# Tests loading the users from the database
def test_load_users_from_csv():
    shutil.copyfile(app.users_csv_path, "./test/testusers.csv")
    loaded_users = app.load_users_from_csv("./test/testusers.csv")
    with open("./test/testusers.csv", 'r') as file:
        for user in loaded_users:
            for i, line in enumerate(file):
                if i != 0:
                    data = line.split(",")
                    if data[1] == user:
                        assert True

# Tests initializing the users on program start
def test_initialize_users():
    shutil.copyfile(app.users_csv_path, "./test/testusers.csv")
    users = app.initialize_users("./test/testusers.csv")
    with open("./test/testusers.csv", 'r') as file:
        for user in users:
            for i, line in enumerate(file):
                if i != 0:
                    data = line.split(",")
                    if data[1] == user:
                        assert True

# Tests initializing users when no users exist in database
def test_initialize_users_blank():
    shutil.copyfile("./test/blank.csv", "./test/testusers.csv")
    users = app.initialize_users("./test/testusers.csv")
    with open("./test/testusers.csv", 'r') as file:
        for user in users:
            for i, line in enumerate(file):
                if i != 0:
                    data = line.split(",")
                    if data[1] == user:
                        assert True

# Tests similar watches functionality
def test_get_similar_watches_number():
    shutil.copyfile(app.csv_path, "./test/testwatches.csv")
    catalogue = Catalogue()
    app.load_watches_from_csv("./test/testwatches.csv", catalogue)
    watch = catalogue.watches[0]
    similar_watches = app.get_similar_watches(watch, catalogue.watches, 5)
    assert len(similar_watches) == 5

# Tests similar watches are rated by similarity properly
def test_get_similar_watches_similarity():
    shutil.copyfile(app.csv_path, "./test/testwatches.csv")
    catalogue = Catalogue()
    app.load_watches_from_csv("./test/testwatches.csv", catalogue)
    watch = catalogue.watches[0]
    watch2 = copy.deepcopy(watch)
    watch3 = copy.deepcopy(watch)
    watch2.watch_id = len(catalogue.watches) + 1
    watch3.watch_id = len(catalogue.watches) + 2
    catalogue.watches.append(watch3)
    catalogue.watches.append(watch2)
    similar_watches = app.get_similar_watches(watch, catalogue.watches, 5)
    assert watch2 in similar_watches
    assert watch3 in similar_watches

# Tests watches with same data are perfectly similar
def test_get_similar_watches_priority():
    shutil.copyfile(app.csv_path, "./test/testwatches.csv")
    catalogue = Catalogue()
    app.load_watches_from_csv("./test/testwatches.csv", catalogue)
    watch = catalogue.watches[0]
    watch2 = copy.deepcopy(watch)
    watch3 = copy.deepcopy(watch)
    watch4 = copy.deepcopy(watch)
    watch5 = copy.deepcopy(watch)
    watch6 = copy.deepcopy(watch)
    watch2.watch_id = len(catalogue.watches) + 1
    watch3.watch_id = len(catalogue.watches) + 2
    watch4.watch_id = len(catalogue.watches) + 3
    watch5.watch_id = len(catalogue.watches) + 4
    watch6.watch_id = len(catalogue.watches) + 5
    watch5.brand = "Testing Brand"
    watch6.brand = "Testing Brand"
    catalogue.watches.append(watch3)
    catalogue.watches.append(watch2)
    catalogue.watches.append(watch4)
    catalogue.watches.append(watch5)
    catalogue.watches.append(watch6)
    similar_watches = app.get_similar_watches(watch, catalogue.watches, 5)
    assert watch2 in similar_watches
    assert watch3 in similar_watches
    assert watch4 in similar_watches
    assert watch5 not in similar_watches
    assert watch6 not in similar_watches