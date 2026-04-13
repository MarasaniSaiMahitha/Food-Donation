import pymysql

try:
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='Mahitha@22',
        port=3306
    )
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS adv_food_db")
    connection.commit()
    print("Database adv_food_db created successfully.")
except Exception as e:
    print(f"Error creating database: {e}")
finally:
    if 'connection' in locals() and connection.open:
        connection.close()
