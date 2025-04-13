
import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    database="your_db",
    user="your_user",
    password="your_password"
)
cur = conn.cursor()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            phone VARCHAR(20)
        )
    """)
    conn.commit()

def insert_from_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", 
                        (row['first_name'], row['phone']))
    conn.commit()

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()

def update_user():
    choice = input("Update by (1) name or (2) phone? ")
    if choice == '1':
        old_name = input("Old name: ")
        new_name = input("New name: ")
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
    elif choice == '2':
        old_phone = input("Old phone: ")
        new_phone = input("New phone: ")
        cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", (new_phone, old_phone))
    conn.commit()

def query_data():
    print("1. Все данные")
    print("2. По имени")
    print("3. По номеру")
    choice = input("Выбор: ")
    if choice == '1':
        cur.execute("SELECT * FROM phonebook")
    elif choice == '2':
        name = input("Имя: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
    elif choice == '3':
        phone = input("Телефон: ")
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
    for row in cur.fetchall():
        print(row)

def delete_data():
    choice = input("Удалить по (1) имени или (2) телефону? ")
    if choice == '1':
        name = input("Имя: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    elif choice == '2':
        phone = input("Телефон: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()

def main():
    create_table()
    while True:
        print("\n1. Вставить из CSV")
        print("2. Ввести вручную")
        print("3. Обновить")
        print("4. Запрос")
        print("5. Удалить")
        print("6. Выйти")
        choice = input("Выбор: ")
        if choice == '1':
            insert_from_csv("data.csv")
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_user()
        elif choice == '4':
            query_data()
        elif choice == '5':
            delete_data()
        elif choice == '6':
            break
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
