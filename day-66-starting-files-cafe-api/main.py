from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        dictionary = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return dictionary


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    all_cafes = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafes=all_cafes)


@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    all_cafes = db.session.execute(db.select(Cafe).where(Cafe.location == query_location)).scalars().all()
    if all_cafes:
        all_cafes = [cafe.to_dict() for cafe in all_cafes]
        return jsonify(cafes=all_cafes), 200
    return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 400


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    name = request.form["name"]
    map_url = request.form["map_url"]
    img_url = request.form["img_url"]
    location = request.form["loc"]
    seats = request.form["seats"]
    has_toilet = bool(request.form["toilet"])
    has_wifi = bool(request.form["wifi"])
    has_sockets = bool(request.form["sockets"])
    can_take_calls = bool(request.form["calls"])
    coffee_price = request.form["coffee_price"]
    new_cafe = Cafe(name=name, map_url=map_url, img_url=img_url, location=location, seats=seats,
                    has_toilet=has_toilet, has_wifi=has_wifi, has_sockets=has_sockets,
                    can_take_calls=can_take_calls, coffee_price=coffee_price)
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key != "TopSecretAPIKey":
        return jsonify({"error": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe."}), 200
    return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


if __name__ == '__main__':
    app.run(debug=True)
