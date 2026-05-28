import sqlite3
import faker
import random
from security import secure_generate_password, secure_hash_password

N_USERS = 256


def init_database(db: sqlite3.Cursor):
    db.executescript(
        """
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        is_flagworthy BOOL DEFAULT FALSE,
        password VARCHAR(255) NOT NULL
    );
    """
    )
    f = faker.Faker("it_IT")
    users = [
        {
            "username": "test",
            "name": "test1",
            "is_flagworthy": False,  # Lol, no  
            "password": secure_hash_password("this_is_test_password"),
        }
    ]
    for _ in range(N_USERS):
        name = f.name()
        username = name.lower().replace(" ", "_")
        password = secure_generate_password()
        users.append(
            {
                "username": username,
                "name": name,
                "is_flagworthy": False,
                "password": secure_hash_password(password),
            }
        )
    random.shuffle(users)
    users[0]["is_flagworthy"] = True
    random.shuffle(users)
    for u in users:
        db.execute(
            """
            INSERT INTO users (username, name, is_flagworthy, password) VALUES (?,?,?,?)""",
            [u["username"], u["name"], u["is_flagworthy"], u["password"]],
        )
    db.connection.commit()
