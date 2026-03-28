import csv
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from backend import Role, Watch, User, Admin, Catalogue, SessionManager

app = Flask(__name__)
app.secret_key = "watch-catalogue-secret-key"

# Backend setup
catalogue = Catalogue()
users = {
    "user": User(1, "user", "1234", Role.USER),
    "admin": Admin(2, "admin", "admin123"),
}


def load_watches_from_csv(filepath):
    """Load watches from the luxury watches CSV dataset."""
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            try:
                price = float(row.get("price", "0"))
            except ValueError:
                price = 0.0

            watch_id_value = row.get("watch_id")
            if watch_id_value is not None and watch_id_value.strip() != "":
                try:
                    watch_id = int(watch_id_value)
                except ValueError:
                    watch_id = i
            else:
                watch_id = i

            watch = Watch(
                watch_id=watch_id,
                name=row.get("name", "").strip(),
                brand=row.get("brand", "").strip(),
                price=price,
                material=row.get("material", "").strip(),
                reference=row.get("reference", "").strip(),
                condition=row.get("condition", "").strip(),
                image_url=row.get("image_url", "").strip(),
            )
            catalogue.add_watch(watch)


def save_watches_to_csv(filepath, watches):
    fieldnames = [
        "watch_id",
        "name",
        "brand",
        "price",
        "material",
        "reference",
        "condition",
        "image_url",
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for watch in watches:
            writer.writerow({
                "watch_id": watch.watch_id,
                "name": watch.name,
                "brand": watch.brand,
                "price": f"{watch.price}",
                "material": watch.material,
                "reference": watch.reference,
                "condition": watch.condition,
                "image_url": watch.image_url,
            })


# Load watches from CSV
csv_path = os.path.join(os.path.dirname(__file__), "watches.csv")
load_watches_from_csv(csv_path)


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("catalogue_page"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = users.get(username)
        if user is None:
            return render_template("login.html", error="User not found.")

        if user.login(username, password):
            session["username"] = username
            session["role"] = user.role.value
            return redirect(url_for("catalogue_page"))
        else:
            return render_template("login.html", error="Incorrect username or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    username = session.get("username")
    if username and username in users:
        users[username].logout()
    session.clear()
    return redirect(url_for("login"))


@app.route("/catalogue")
def catalogue_page():
    if "username" not in session:
        return redirect(url_for("login"))

    query = request.args.get("q", "").strip()
    brand = request.args.get("brand", "").strip()
    material = request.args.get("material", "").strip()
    condition = request.args.get("condition", "").strip()
    min_price = request.args.get("min_price", "").strip()
    max_price = request.args.get("max_price", "").strip()

    if query:
        watches = catalogue.search_watches(query)
    elif brand or material or condition or min_price or max_price:
        watches = catalogue.filter_watches(
            brand=brand or None,
            material=material or None,
            condition=condition or None,
            min_price=float(min_price) if min_price else None,
            max_price=float(max_price) if max_price else None,
        )
    else:
        watches = catalogue.get_all_watches()

    # Pagination
    page = request.args.get("page", 1, type=int)
    per_page = 24
    total = len(watches)
    total_pages = max(1, (total + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    paginated = watches[(page - 1) * per_page : page * per_page]

    # Collect unique values for filter dropdowns.
    all_watches = catalogue.get_all_watches()
    brands = sorted(set(w.brand for w in all_watches))
    materials = sorted(set(w.material for w in all_watches))
    conditions = sorted(set(w.condition for w in all_watches))

    is_admin = session.get("role") == "ADMIN"

    return render_template(
        "catalogue.html",
        watches=paginated,
        total=total,
        page=page,
        total_pages=total_pages,
        brands=brands,
        materials=materials,
        conditions=conditions,
        username=session["username"],
        is_admin=is_admin,
        query=query,
        sel_brand=brand,
        sel_material=material,
        sel_condition=condition,
        sel_min_price=min_price,
        sel_max_price=max_price,
    )


@app.route("/api/watch/<int:watch_id>")
def get_watch(watch_id):
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401
    watch = catalogue.get_watch(watch_id)
    if watch:
        return jsonify(watch.get_details())
    return jsonify({"error": "Watch not found"}), 404


@app.route("/api/watch", methods=["POST"])
def add_watch():
    if "username" not in session or session.get("role") != "ADMIN":
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    try:
        watch = Watch(
            watch_id=int(data["watch_id"]),
            name=data["name"],
            brand=data["brand"],
            price=float(data["price"]),
            material=data.get("material", ""),
            reference=data.get("reference", ""),
            condition=data.get("condition", ""),
            image_url=data.get("image_url", ""),
        )
        admin = users[session["username"]]
        admin.add_watch(watch, catalogue)
        save_watches_to_csv(csv_path, catalogue.get_all_watches())
        return jsonify({"success": True, "watch": watch.get_details()})
    except (ValueError, PermissionError) as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/watch/<int:watch_id>", methods=["PUT"])
def edit_watch(watch_id):
    if "username" not in session or session.get("role") != "ADMIN":
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    try:
        admin = users[session["username"]]
        kwargs = {}
        for field in ["name", "brand", "material", "reference",
                       "condition", "image_url"]:
            if field in data:
                kwargs[field] = data[field]
        if "price" in data:
            kwargs["price"] = float(data["price"])
        admin.edit_watch(watch_id, catalogue, **kwargs)
        save_watches_to_csv(csv_path, catalogue.get_all_watches())
        watch = catalogue.get_watch(watch_id)
        return jsonify({"success": True, "watch": watch.get_details()})
    except (ValueError, PermissionError) as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/watch/<int:watch_id>", methods=["DELETE"])
def delete_watch(watch_id):
    if "username" not in session or session.get("role") != "ADMIN":
        return jsonify({"error": "Admin access required"}), 403

    try:
        admin = users[session["username"]]
        admin.delete_watch(watch_id, catalogue)
        save_watches_to_csv(csv_path, catalogue.get_all_watches())
        return jsonify({"success": True})
    except (ValueError, PermissionError) as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
