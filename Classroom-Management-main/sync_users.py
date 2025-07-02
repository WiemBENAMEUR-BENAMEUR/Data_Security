import mysql.connector
from lib.helper import user_data_path  # path to your user.txt file

def sync_users_from_db():
    # Connect to MySQL inside Docker
    conn = mysql.connector.connect(
        host="db",  # docker service name for mysql
        user="admin",
        password="password",
        database="classroom"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, register_time, role FROM users")
    users = cursor.fetchall()

    # Read existing users from user.txt into a set for quick lookup
    existing_users = set()
    try:
        with open(user_data_path, "r", encoding="utf-8") as f:
            for line in f:
                # Assuming id is the first field before ";;;"
                existing_users.add(line.split(";;;")[0])
    except FileNotFoundError:
        # If file doesn't exist yet, that's fine
        pass

    with open(user_data_path, "a", encoding="utf-8") as f:  # Open in append mode
        new_count = 0
        for row in users:
            user_id = str(row[0])
            if user_id not in existing_users:
                line = ";;;".join(str(col) for col in row) + "\n"
                f.write(line)
                new_count += 1

    print(f"✅ Synced users from DB to user.txt, added {new_count} new users")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    sync_users_from_db()
