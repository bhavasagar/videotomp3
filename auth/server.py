import datetime
import jwt, os
from flask import Flask, request
from flask_mysqldb import MySQL


app = Flask(__name__)
mysql = MySQL(app)


app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


@app.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Credentials not found", 400
    
    cursor = mysql.connection.cursor()
    ret = cursor.execute(f"SELECT * FROM User WHERE email={auth.username}")
    if ret > 0:
        user_row = cursor.fetchone()
        email = user_row[0]
        password = user_row[1]

        if email != auth.username or password != auth.password:
            return "Invalid credentials", 401
        
        return createJWT(auth.username, os.environ.get('JWT_SECRET'), True)
    return "User doesn't exisits", 400

@app.post("/validate")
def validate():
    encoded_jwt = request.headers["Authorization"]
    
    if not encoded_jwt:
        return "Missing Credentials", 400
    
    if "Bearer" not in encoded_jwt:
        return "Invalid Token", 400
    
    token = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("secret"), algorithm=["HS256"]
        )
    except:
        return "Not authorized", 400
    
    return decoded, 200
    
def createJWT(username, secret, admin):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(tz=datetime.timezone.utc),
            "admin": admin
        },
        secret=secret,
        algorithm="HS256"
    )
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)