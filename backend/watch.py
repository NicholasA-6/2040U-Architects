#this class is for specifying the details that are in a watch
class Watch:
    def __init__(self, watch_id, name, brand, display_type, price, case_shape, certifications, image_url):
        self.watch_id = watch_id
        self.name = name
        self.brand = brand
        self.display_type = display_type
        self.price = price
        self.case_shape = case_shape
        self.certifications = certifications
        self.image_url = image_url

        def get_details(self):
            return (
                f"Watch ID: {self.watch_id}\n"
                f"Name: {self.name}\n"
                f"Brand: {self.brand}\n"
                f"Display Type: {self.display_type}\n"
                f"Price: {self.price}\n"
                f"Certifications: {self.certifications}\n"
                f"Image URL: {self.image_url}\n"
            )
        
        #needed for editing details of the wathces
        def update_details(self, watch_id, name, brand, display_type, price, case_shape, certifications, image_url):
            self.name = name
            self.brand = brand
            self.display_type = display_type
            self.price = price
            self.case_shape = case_shape
            self.certifications = certifications
            self.image_url = image_url
        
        def __str__(self):
            return f"{self.watch_id} - {self.name} ({self.brand}) - ${self.price}"