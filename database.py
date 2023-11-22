import sqlite3 as sql


async def sql_connector():
    con = sql.connect("shazam.db")
    cur = con.cursor()
    return con, cur


async def create_tables():
    con, cur = await sql_connector()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY,
                username VARCHAR(100)
        )""")

async def add_user(user_id: int, username: str):
    con, cur = await sql_connector()
    user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()

    if not user:
        cur.execute("INSERT INTO users VALUES (?, ?)", (user_id, username))
        con.commit()
    

async def get_all_users():
    con, cur = await sql_connector()
    
    users = cur.execute("SELECT * FROM users").fetchall()
    return len(users)

async def get_all_users_id():
    con, cur = await sql_connector()
    
    users = cur.execute("SELECT user_id FROM users").fetchall()
    return users


async def get_all_users():
    con, cur = await sql_connector()
    
    users = cur.execute("SELECT * FROM users").fetchone()
    return len(users)


async def get_all_id():
    con, cur = await sql_connector()
    
    users = cur.execute("SELECT user_id FROM users").fetchall()
    return users
