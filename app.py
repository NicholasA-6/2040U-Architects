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

# Pre-load sample watches so the catalogue is not empty on first visit.
sample_watches = [
    Watch(1, "Submariner Date", "Rolex", "Automatic", "Analog",
          9150.00, "Round", "COSC Certified", ""),
    Watch(2, "Speedmaster Moonwatch", "Omega", "Manual-winding", "Analog",
          6350.00, "Round", "METAS Certified", ""),
    Watch(3, "Royal Oak", "Audemars Piguet", "Automatic", "Analog",
          24500.00, "Octagonal", "None", ""),
    Watch(4, "Nautilus", "Patek Philippe", "Automatic", "Analog",
          35000.00, "Rounded Octagonal", "Patek Philippe Seal", ""),
    Watch(5, "Santos de Cartier", "Cartier", "Automatic", "Analog",
          7250.00, "Square", "None", ""),
    Watch(6, "Big Pilot", "IWC", "Automatic", "Analog",
          13500.00, "Round", "None", ""),
    Watch(7, "Luminor Marina", "Panerai", "Automatic", "Analog",
          8900.00, "Cushion", "None", ""),
    Watch(8, "Reverso Classic", "Jaeger-LeCoultre", "Manual-winding", "Analog",
          6800.00, "Rectangular", "None", ""),
]

for w in sample_watches:
    catalogue.add_watch(w)


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
    movement = request.args.get("movement", "").strip()
    case_shape = request.args.get("case_shape", "").strip()
    min_price = request.args.get("min_price", "").strip()
    max_price = request.args.get("max_price", "").strip()

    if query:
        watches = catalogue.search_watches(query)
    elif brand or movement or case_shape or min_price or max_price:
        watches = catalogue.filter_watches(
            brand=brand or None,
            movement_type=movement or None,
            case_shape=case_shape or None,
            min_price=float(min_price) if min_price else None,
            max_price=float(max_price) if max_price else None,
        )
    else:
        watches = catalogue.get_all_watches()

    # Collect unique values for filter dropdowns.
    all_watches = catalogue.get_all_watches()
    brands = sorted(set(w.brand for w in all_watches))
    movements = sorted(set(w.movement_type for w in all_watches))
    case_shapes = sorted(set(w.case_shape for w in all_watches))

    is_admin = session.get("role") == "ADMIN"

    return render_template(
        "catalogue.html",
        watches=watches,
        brands=brands,
        movements=movements,
        case_shapes=case_shapes,
        username=session["username"],
        is_admin=is_admin,
        query=query,
        sel_brand=brand,
        sel_movement=movement,
        sel_case_shape=case_shape,
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
            movement_type=data["movement_type"],
            display_type=data["display_type"],
            price=float(data["price"]),
            case_shape=data["case_shape"],
            certifications=data.get("certifications", ""),
            image_url=data.get("image_url", ""),
        )
        admin = users[session["username"]]
        admin.add_watch(watch, catalogue)
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
        for field in ["name", "brand", "movement_type", "display_type",
                       "case_shape", "certifications", "image_url"]:
            if field in data:
                kwargs[field] = data[field]
        if "price" in data:
            kwargs["price"] = float(data["price"])
        admin.edit_watch(watch_id, catalogue, **kwargs)
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
        return jsonify({"success": True})
    except (ValueError, PermissionError) as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
