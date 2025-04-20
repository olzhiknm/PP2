import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="your_db",
    user="your_user",
    password="your_password"
)
cur = conn.cursor()

def call_search():
    pattern = input()
    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def call_insert_or_update():
    name = input()
    phone = input()
    cur.callproc("insert_or_update_user", (name, phone))
    conn.commit()

def call_insert_many():
    cur.execute("DELETE FROM temp_users")
    n = int(input())
    for _ in range(n):
        name = input()
        phone = input()
        cur.execute("INSERT INTO temp_users (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.callproc("insert_many_users")
    conn.commit()

def call_paginate():
    limit = int(input())
    offset = int(input())
    cur.execute("SELECT * FROM paginate_users(%s, %s)", (limit, offset))
    for row in cur.fetchall():
        print(row)

def call_delete():
    value = input()
    cur.callproc("delete_user", (value,))
    conn.commit()

def main():
    while True:
        print("\n1. Поиск")
        print("2. Вставить/обновить")
        print("3. Вставить список")
        print("4. Пагинация")
        print("5. Удалить")
        print("6. Выход")
        choice = input()
        if choice == '1':
            call_search()
        elif choice == '2':
            call_insert_or_update()
        elif choice == '3':
            call_insert_many()
        elif choice == '4':
            call_paginate()
        elif choice == '5':
            call_delete()
        elif choice == '6':
            break
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
