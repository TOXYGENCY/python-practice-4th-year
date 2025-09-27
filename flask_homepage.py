from flask import Flask, render_template

app = Flask(__name__)

items_list = [
    "item 1",
    "item 2.0",
    "item pro max"
]
is_active = True

users_data = {
    1: {
        "name": "Ivan",
        "surname": "Petrov",
        "email": "email@mail.ru",
        "phone": "+79451236789"
    },
    2: {
        "name": "Petr",
        "surname": "Ivanov",
        "email": "email@mail.ru",
        "phone": "+79451236789"
    },
    3: {
        "name": "sidor",
        "surname": "sidorov",
        "email": "email@mail.ru",
        "phone": "+79451236789"
    },
    4: {
        "name": "Jon",
        "surname": "Doeh",
        "email": "email@mail.ru",
        "phone": "+79451236789"
    }
}

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/users/<int:user_id>")
def users(user_id):
    return render_template("user.html", user=users_data[user_id])

@app.route("/items")
def items():
    return render_template("items.html", name="Petrov", items = items_list, is_active = is_active)


@app.route("/name/<name>")
def name(name):
    return name

@app.route("/age/<int:age>")
def age(age):
    return f"{age}"

if __name__ == "__main__":
    app.run(debug=True)