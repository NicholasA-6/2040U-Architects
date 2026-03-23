from enum import Enum


# Keeps the user roles clear and easy to check.
class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"


# Represents one watch in the catalogue.
class Watch:
    def __init__(self, watch_id, name, brand, movement_type, display_type,
                 price, case_shape, certifications, image_url):
        self.watch_id = watch_id
        self.name = name
        self.brand = brand
        self.movement_type = movement_type
        self.display_type = display_type
        self.price = price
        self.case_shape = case_shape
        self.certifications = certifications
        self.image_url = image_url

    def get_details(self):
        return {
            "watch_id": self.watch_id,
            "name": self.name,
            "brand": self.brand,
            "movement_type": self.movement_type,
            "display_type": self.display_type,
            "price": self.price,
            "case_shape": self.case_shape,
            "certifications": self.certifications,
            "image_url": self.image_url,
        }

    def __str__(self):
        return f"{self.watch_id} - {self.name} ({self.brand}) - ${self.price}"


# Base user class.
class User:
    def __init__(self, user_id, username, password_hash, role=Role.USER):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.logged_in = False
        self.wishlist = []

    def login(self, username, password):
        if self.username == username and self.password_hash == password:
            self.logged_in = True
            return True
        return False

    def logout(self):
        self.logged_in = False

    def is_logged_in(self):
        return self.logged_in
    
    def add_to_wishlist(self, watch):
        if watch not in self.wishlist:
            self.wishlist.append(watch)

    def remove_from_wishlist(self, watch_id):
        for watch in self.wishlist:
            if watch.watch_id == watch_id:
                self.wishlist.remove(watch)
                return True
        return False

    def get_wishlist(self):
        return self.wishlist

    def is_in_wishlist(self, watch_id):
        for watch in self.wishlist:
            if watch.watch_id == watch_id:
                return True
        return False


# Admin can do extra actions like adding watches.
class Admin(User):
    def __init__(self, user_id, username, password_hash):
        super().__init__(user_id, username, password_hash, Role.ADMIN)

    def add_watch(self, watch, catalogue):
        if not self.logged_in:
            raise PermissionError("Admin must be logged in before adding a watch.")
        catalogue.add_watch(watch)

    def edit_watch(self, watch_id, catalogue, **kwargs):
        if not self.logged_in:
            raise PermissionError("Admin must be logged in before editing a watch.")
        catalogue.edit_watch(watch_id, **kwargs)

    def delete_watch(self, watch_id, catalogue):
        if not self.logged_in:
            raise PermissionError("Admin must be logged in before deleting a watch.")
        catalogue.delete_watch(watch_id)


# Stores all watches.
class Catalogue:
    def __init__(self):
        self.watches = []

    def add_watch(self, watch):
        for existing_watch in self.watches:
            if existing_watch.watch_id == watch.watch_id:
                raise ValueError(f"Watch with ID {watch.watch_id} already exists.")
        self.watches.append(watch)

    def edit_watch(self, watch_id, **kwargs):
        for watch in self.watches:
            if watch.watch_id == watch_id:
                for key, value in kwargs.items():
                    if hasattr(watch, key):
                        setattr(watch, key, value)
                return watch
        raise ValueError(f"Watch with ID {watch_id} not found.")

    def delete_watch(self, watch_id):
        for i, watch in enumerate(self.watches):
            if watch.watch_id == watch_id:
                return self.watches.pop(i)
        raise ValueError(f"Watch with ID {watch_id} not found.")

    def get_watch(self, watch_id):
        for watch in self.watches:
            if watch.watch_id == watch_id:
                return watch
        return None

    def get_all_watches(self):
        return self.watches

    def search_watches(self, query):
        query = query.lower()
        return [w for w in self.watches if
                query in w.name.lower() or
                query in w.brand.lower() or
                query in w.certifications.lower()]

    def filter_watches(self, brand=None, min_price=None, max_price=None,
                       movement_type=None, case_shape=None):
        results = self.watches
        if brand:
            results = [w for w in results if w.brand.lower() == brand.lower()]
        if min_price is not None:
            results = [w for w in results if w.price >= min_price]
        if max_price is not None:
            results = [w for w in results if w.price <= max_price]
        if movement_type:
            results = [w for w in results if w.movement_type.lower() == movement_type.lower()]
        if case_shape:
            results = [w for w in results if w.case_shape.lower() == case_shape.lower()]
        return results


# Tracks who is currently logged in.
class SessionManager:
    def __init__(self):
        self.current_user = None

    def login(self, user, username, password):
        success = user.login(username, password)
        if success:
            self.current_user = user
        return success

    def logout(self):
        if self.current_user is not None:
            self.current_user.logout()
            self.current_user = None

    def get_current_user(self):
        return self.current_user

    def is_admin_logged_in(self):
        return (
            self.current_user is not None
            and self.current_user.is_logged_in()
            and self.current_user.role == Role.ADMIN
        )