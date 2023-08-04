from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='------',
    database='Scraping'
)


class User(BaseModel):
    id: int
    username: str
    email: str

# CRUD operations
@app.post("/users/", response_model=User)
async def create_user(user: User):
    user_data = jsonable_encoder(user)
    cursor = db_connection.cursor()
    insert_query = "INSERT INTO user (id, username, email) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (user_data['id'], user_data['username'], user_data['email']))
    db_connection.commit()
    return user_data

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    cursor = db_connection.cursor()
    select_query = "SELECT * FROM user WHERE id = %s"
    cursor.execute(select_query, (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        return User(id=user_data[0], username=user_data[1], email=user_data[2])
    else:
        return JSONResponse(content={"message": "User not found"}, status_code=404)

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    user_data = jsonable_encoder(user)
    cursor = db_connection.cursor()
    update_query = "UPDATE user SET username = %s, email = %s WHERE id = %s"
    cursor.execute(update_query, (user_data['username'], user_data['email'], user_id))
    db_connection.commit()
    return user_data

@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    cursor = db_connection.cursor()
    select_query = "SELECT * FROM user WHERE id = %s"
    cursor.execute(select_query, (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        delete_query = "DELETE FROM user WHERE id = %s"
        cursor.execute(delete_query, (user_id,))
        db_connection.commit()
        return User(id=user_data[0], username=user_data[1], email=user_data[2])
    else:
        return JSONResponse(content={"message": "User not found"}, status_code=404)
