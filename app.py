from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.url_map.strict_slashes = False
app.debug = True

app.secret_key = "sri"

#Just something you would have (basically creating an engine to go and edit your DB and each session so that multiple users can access)
engine = create_engine("postgresql://postgres:atharva13@127.0.0.1:5432/practice")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        flights = db.execute("SELECT * FROM flights").fetchall()
        return render_template("index.html", flights=flights)
    else:
        flight_id = request.form.get("flight_id")
        name = request.form.get("name")
        db.execute("INSERT INTO passengers(name, flight_id) VALUES (:name, :flight_id)", {"name": name, "flight_id": flight_id})
        db.commit()
        return render_template("success.html")

@app.route("/admin", methods = ['GET', 'POST'])
def admin():
    if request.method == 'GET':
        flights = db.execute("SELECT * FROM flights").fetchall()
        return render_template("admin.html", flights=flights)
    else:
        origin = request.form.get("origin")
        destination = request.form.get("destination")
        duration = request.form.get("duration")
        db.execute("INSERT INTO flights(origin, destination, duration) VALUES (:origin, :destination, :duration)",
                   {"origin": origin, "destination": destination, "duration": duration})
        db.commit()
        return redirect("/admin")

@app.route("/details", methods = ['GET'])
def details():
    flight_id = request.args.get("idd")
    find_flight = db.execute("SELECT origin, destination, duration FROM flights WHERE id=:flight_id", {"flight_id": flight_id}).fetchall()
    flights = db.execute("SELECT * FROM flights").fetchall()
    passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
                            {"flight_id": flight_id}).fetchall()
    return render_template("details.html", flights=flights, passengers=passengers, flight_id=flight_id, find_flight=find_flight)


if __name__ == "__main__":
    app.run("")