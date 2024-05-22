from flask import Flask, request, render_template
from repositories.UserRepository import UserRepository
from services.UserService import UserService
from models.User import User, Base
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine('sqlite:///database/database.db', echo=True)
user_repository: UserRepository = UserRepository(engine=engine, base=Base)
user_service: UserService = UserService(user_repository=user_repository)


@app.route('/')
def index():
    users_list = user_service.get_all_users()
    return render_template("index.html", users=users_list)


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    phone = request.form['phone']

    error_message = None

    try:
        user_service.add_user(User(name, surname, email, phone))
    except ValueError as e:
        error_message = str(e)

    users_list = user_service.get_all_users()
    return render_template("index.html", users=users_list, error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
