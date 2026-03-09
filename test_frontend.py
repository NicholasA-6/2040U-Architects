import tkinter as tk
from tkinter import ttk, messagebox
from enum import Enum


# ---------------------------
# Backend classes
# ---------------------------

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
        return (
            f"ID: {self.watch_id}\n"
            f"Name: {self.name}\n"
            f"Brand: {self.brand}\n"
            f"Movement: {self.movement_type}\n"
            f"Display: {self.display_type}\n"
            f"Price: ${self.price}\n"
            f"Case Shape: {self.case_shape}\n"
            f"Certifications: {self.certifications}\n"
            f"Image URL: {self.image_url}"
        )

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

    def login(self, username, password):
        if self.username == username and self.password_hash == password:
            self.logged_in = True
            return True
        return False

    def logout(self):
        self.logged_in = False

    def is_logged_in(self):
        return self.logged_in


# Admin can do extra actions like adding watches.
class Admin(User):
    def __init__(self, user_id, username, password_hash):
        super().__init__(user_id, username, password_hash, Role.ADMIN)

    def add_watch(self, watch, catalogue):
        if not self.logged_in:
            raise PermissionError("Admin must be logged in before adding a watch.")
        catalogue.add_watch(watch)


# Stores all watches.
class Catalogue:
    def __init__(self):
        self.watches = []

    def add_watch(self, watch):
        for existing_watch in self.watches:
            if existing_watch.watch_id == watch.watch_id:
                raise ValueError(f"Watch with ID {watch.watch_id} already exists.")
        self.watches.append(watch)

    def get_all_watches(self):
        return self.watches


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


# ---------------------------
# Frontend
# ---------------------------

class WatchApp:
    # Colors used across the app for a consistent look.
    BG_COLOR = "#f0f2f5"
    HEADER_BG = "#2c3e50"
    HEADER_FG = "#ffffff"
    ACCENT_COLOR = "#2980b9"
    ACCENT_HOVER = "#3498db"
    FONT = "Segoe UI"

    def __init__(self, root):
        self.root = root
        self.root.title("Watch Catalog Test Frontend")
        self.root.geometry("900x700")
        self.root.configure(bg=self.BG_COLOR)

        # Set up ttk styles so buttons and entries look cleaner.
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("TLabel", font=(self.FONT, 10), background=self.BG_COLOR)
        self.style.configure("Header.TLabel", font=(self.FONT, 18, "bold"), background=self.BG_COLOR)
        self.style.configure("SubHeader.TLabel", font=(self.FONT, 13, "bold"), background=self.BG_COLOR)
        self.style.configure("Info.TLabel", font=(self.FONT, 14, "bold"), background=self.BG_COLOR)

        self.style.configure(
            "Accent.TButton",
            font=(self.FONT, 10, "bold"),
            background=self.ACCENT_COLOR,
            foreground="#ffffff",
            padding=(12, 6)
        )
        self.style.map(
            "Accent.TButton",
            background=[("active", self.ACCENT_HOVER)]
        )

        self.style.configure("TButton", font=(self.FONT, 10), padding=(8, 4))
        self.style.configure("TEntry", padding=(4, 4))
        self.style.configure("TLabelframe", background=self.BG_COLOR, font=(self.FONT, 10, "bold"))
        self.style.configure("TLabelframe.Label", background=self.BG_COLOR, font=(self.FONT, 10, "bold"))

        # Basic backend setup
        self.catalogue = Catalogue()
        self.session_manager = SessionManager()

        # Sample users for testing
        self.normal_user = User(1, "user", "1234", Role.USER)
        self.admin_user = Admin(2, "admin", "admin123")

        # Main container
        self.main_frame = tk.Frame(self.root, padx=15, pady=15, bg=self.BG_COLOR)
        self.main_frame.pack(fill="both", expand=True)

        self.build_login_ui()

    # Clears the current screen before drawing a new one.
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ---------------------------
    # Login screen
    # ---------------------------
    def build_login_ui(self):
        self.clear_frame()

        ttk.Label(
            self.main_frame,
            text="Watch Catalog System - Login",
            style="Header.TLabel"
        ).pack(pady=(30, 10))

        login_box = tk.Frame(self.main_frame, bd=2, relief="groove",
                             padx=20, pady=20, bg=self.BG_COLOR)
        login_box.pack(pady=20)

        ttk.Label(login_box, text="Username:").grid(row=0, column=0, sticky="w", pady=8, padx=5)
        self.username_entry = ttk.Entry(login_box, width=28)
        self.username_entry.grid(row=0, column=1, pady=8, padx=5)

        ttk.Label(login_box, text="Password:").grid(row=1, column=0, sticky="w", pady=8, padx=5)
        self.password_entry = ttk.Entry(login_box, width=28, show="*")
        self.password_entry.grid(row=1, column=1, pady=8, padx=5)

        ttk.Button(
            login_box,
            text="Login",
            style="Accent.TButton",
            command=self.handle_login
        ).grid(row=2, column=0, columnspan=2, pady=15)

        # These labels make testing easier so you do not forget the sample accounts.
        ttk.Label(
            self.main_frame,
            text="Test accounts:\nUser -> username: user | password: 1234\nAdmin -> username: admin | password: admin123",
            justify="left"
        ).pack(pady=15)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # We only have two sample users for testing.
        selected_user = None
        if username == self.normal_user.username:
            selected_user = self.normal_user
        elif username == self.admin_user.username:
            selected_user = self.admin_user

        if selected_user is None:
            messagebox.showerror("Login Failed", "User not found.")
            return

        success = self.session_manager.login(selected_user, username, password)

        if success:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.build_dashboard_ui()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    # ---------------------------
    # Main dashboard
    # ---------------------------
    def build_dashboard_ui(self):
        self.clear_frame()

        current_user = self.session_manager.get_current_user()

        header_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        header_frame.pack(fill="x", pady=(5, 15))

        ttk.Label(
            header_frame,
            text=f"Logged in as: {current_user.username} ({current_user.role.value})",
            style="Info.TLabel"
        ).pack(side="left")

        ttk.Button(
            header_frame,
            text="Logout",
            command=self.handle_logout
        ).pack(side="right")

        # Left side for watch list
        left_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        left_frame.pack(side="left", fill="both", expand=True, padx=(5, 15), pady=10)

        ttk.Label(left_frame, text="Catalogue Watches", style="SubHeader.TLabel").pack(anchor="w")

        # Listbox with a scrollbar so longer lists are easy to browse.
        list_container = tk.Frame(left_frame, bg=self.BG_COLOR)
        list_container.pack(fill="both", expand=True, pady=8)

        scrollbar = ttk.Scrollbar(list_container, orient="vertical")
        self.watch_listbox = tk.Listbox(
            list_container, width=50, height=25,
            font=(self.FONT, 10),
            selectbackground=self.ACCENT_COLOR,
            selectforeground="#ffffff",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.watch_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.watch_listbox.pack(side="left", fill="both", expand=True)
        self.watch_listbox.bind("<<ListboxSelect>>", self.show_watch_details)

        # Right side for details and admin actions, wrapped in a scrollable canvas.
        right_outer = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        right_outer.pack(side="right", fill="both", expand=True, padx=(15, 5), pady=10)

        right_canvas = tk.Canvas(right_outer, bg=self.BG_COLOR, highlightthickness=0)
        right_scrollbar = ttk.Scrollbar(right_outer, orient="vertical", command=right_canvas.yview)
        right_frame = tk.Frame(right_canvas, bg=self.BG_COLOR)

        right_frame.bind(
            "<Configure>",
            lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all"))
        )
        right_canvas.create_window((0, 0), window=right_frame, anchor="nw")
        right_canvas.configure(yscrollcommand=right_scrollbar.set)

        right_canvas.pack(side="left", fill="both", expand=True)
        right_scrollbar.pack(side="right", fill="y")

        # Allow mousewheel scrolling on the right panel.
        def on_mousewheel(event):
            right_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        right_canvas.bind_all("<MouseWheel>", on_mousewheel)

        ttk.Label(right_frame, text="Watch Details", style="SubHeader.TLabel").pack(anchor="w")

        self.details_text = tk.Text(
            right_frame, width=45, height=12,
            font=(self.FONT, 10), state="normal",
            padx=8, pady=8
        )
        self.details_text.pack(pady=8)
        self.details_text.insert("1.0", "Select a watch from the list to view details.")
        self.details_text.config(state="disabled")

        # Only admins should see the add watch section.
        if self.session_manager.is_admin_logged_in():
            self.build_add_watch_form(right_frame)
        else:
            ttk.Label(
                right_frame,
                text="You are logged in as a normal user.\nYou can view watches, but you cannot add them.",
                justify="left"
            ).pack(pady=25, anchor="w")

        self.refresh_watch_list()

    # ---------------------------
    # Add watch section
    # ---------------------------
    def build_add_watch_form(self, parent):
        form_frame = ttk.LabelFrame(parent, text="Add Watch (Admin Only)", padding=(15, 10))
        form_frame.pack(fill="x", pady=15)

        labels = [
            "Watch ID", "Name", "Brand", "Movement Type",
            "Display Type", "Price", "Case Shape",
            "Certifications", "Image URL"
        ]

        self.form_entries = {}

        for i, label_text in enumerate(labels):
            ttk.Label(form_frame, text=label_text + ":").grid(row=i, column=0, sticky="w", pady=4)
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=4, padx=8)
            self.form_entries[label_text] = entry

        ttk.Button(
            form_frame,
            text="Add Watch",
            style="Accent.TButton",
            command=self.handle_add_watch
        ).grid(row=len(labels), column=0, columnspan=2, pady=12)

    def handle_add_watch(self):
        try:
            watch_id = int(self.form_entries["Watch ID"].get().strip())
            name = self.form_entries["Name"].get().strip()
            brand = self.form_entries["Brand"].get().strip()
            movement_type = self.form_entries["Movement Type"].get().strip()
            display_type = self.form_entries["Display Type"].get().strip()
            price = float(self.form_entries["Price"].get().strip())
            case_shape = self.form_entries["Case Shape"].get().strip()
            certifications = self.form_entries["Certifications"].get().strip()
            image_url = self.form_entries["Image URL"].get().strip()

            # Basic check so empty important fields do not go in by accident.
            if not name or not brand:
                messagebox.showerror("Input Error", "Name and brand cannot be empty.")
                return

            watch = Watch(
                watch_id=watch_id,
                name=name,
                brand=brand,
                movement_type=movement_type,
                display_type=display_type,
                price=price,
                case_shape=case_shape,
                certifications=certifications,
                image_url=image_url
            )

            admin = self.session_manager.get_current_user()
            admin.add_watch(watch, self.catalogue)

            messagebox.showinfo("Success", "Watch added successfully.")
            self.refresh_watch_list()

            # Clears the form after adding a watch.
            for entry in self.form_entries.values():
                entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Input Error", f"Please check your input.\n\n{e}")
        except PermissionError as e:
            messagebox.showerror("Permission Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------
    # Watch display
    # ---------------------------
    def refresh_watch_list(self):
        self.watch_listbox.delete(0, tk.END)

        watches = self.catalogue.get_all_watches()

        if not watches:
            self.watch_listbox.insert(tk.END, "  No watches yet. Add one to get started.")
        else:
            for watch in watches:
                self.watch_listbox.insert(tk.END, str(watch))

    def show_watch_details(self, event):
        selected_index = self.watch_listbox.curselection()

        if not selected_index:
            return

        watch = self.catalogue.get_all_watches()[selected_index[0]]

        self.details_text.config(state="normal")
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert("1.0", watch.get_details())
        self.details_text.config(state="disabled")

    # ---------------------------
    # Logout
    # ---------------------------
    def handle_logout(self):
        self.session_manager.logout()
        messagebox.showinfo("Logged Out", "You have been logged out.")
        self.build_login_ui()


# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = WatchApp(root)
    root.mainloop()