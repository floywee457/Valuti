import psycopg2
from datetime import datetime

connecting = {
    'host': 'localhost',
    'port': 5432,
    'database': 'Valute_info',
    'user': 'postgres',
    'password': '12345'
}

def transform():
    conn = psycopg2.connect(**connecting)
    cur = conn.cursor()

    # Создаём таблицу для статистики если её нет
    cur.execute("""
        CREATE TABLE IF NOT EXISTS valuti_stats (
            id SERIAL PRIMARY KEY,
            date DATE,
            code VARCHAR(10),
            name VARCHAR(200),
            avg_value NUMERIC(10, 4),
            max_value NUMERIC(10, 4),
            min_value NUMERIC(10, 4),
            count_measurements INTEGER,
            calculated_at TIMESTAMP
        )
    """)

    # Берём все дни
    cur.execute("SELECT DISTINCT date(date) FROM valuti ORDER BY date")
    days = [row[0] for row in cur.fetchall()]

    if not days:
        print("Нет данных")
        conn.close()
        return

    now = datetime.now()

    for day in days:
        cur.execute("DELETE FROM valuti_stats WHERE date = %s", (day,))

        cur.execute("""
            INSERT INTO valuti_stats (date, code, name, avg_value, max_value, min_value, count_measurements, calculated_at)
            SELECT
                date(date),
                code,
                name,
                ROUND(AVG(value), 4),
                MAX(value),
                MIN(value),
                COUNT(*),
                %s
            FROM valuti
            WHERE date(date) = %s
            GROUP BY date(date), code, name
        """, (now, day))

    conn.commit()
    cur.close()
    conn.close()

    print(f"Трансформация завершена")


if __name__ == "__main__":
    transform()