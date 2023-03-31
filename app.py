from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# CREATE THE FLASK APP
app = Flask(__name__)

# ADD THE DATABASE CONNECTION TO THE FLASK APP
db_cred = {
    'user': 'username',    # DATABASE USER
    'pass': 'password',    # DATABASE PASSWORD
    'host': '127.0.0.1',   # DATABASE HOSTNAME
    'name': 'vulnerable'   # DATABASE NAME
}
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://\
{db_cred['user']}:{db_cred['pass']}@{db_cred['host']}/\
{db_cred['name']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db  = SQLAlchemy(app)

with app.app_context():
    with db.engine.connect() as conn:
        # CLEAN
        conn.execute(text("DROP TABLE IF EXISTS users;"))

        # CREATE A users TABLE USING RAW SQL QUERY
        conn.execute(
            text(
            '''
            CREATE TABLE users (
                email VARCHAR(50),
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                passwd VARCHAR(50)
            );
            '''
            )
        )

        # INSERT TEMP VALUES IN THE users TABLE USING RAW SQL QUERY
        conn.execute(
            text(
            '''
            INSERT INTO users (`email`, `first_name`, `last_name`, `passwd`) VALUES
            ("john.doe@zmail.com", "John", "Doe", "john@123");
            '''
            )
        )
        conn.execute(
            text(
            '''
            INSERT INTO users (`email`, `first_name`, `last_name`, `passwd`) VALUES
            ("liam.olivia@wmail.com", "Liam", "Olivia", "lolivia$345");
            '''
            )
        )
        conn.commit()

@app.route("/sqli/login", methods= ["GET","POST"])
def sqli_login():
    if "email" in request.form and "password" in request.form:
        email = request.form.get("email")
        passwd = request.form.get("password")

        with db.engine.connect() as conn:
            rs = conn.execute(text("SELECT * from users WHERE email='"+email+"' AND passwd='"+passwd+"'")).all()

            if len(rs) != 0:
                return "Login OK"
            else:
                return "Login failed"
    else:
        return "Login failed"

# RUN THE APP
if __name__ == '__main__':
    app.run()
