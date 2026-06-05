import csv
import psycopg2
from datetime import datetime

connecting = {
    'host': 'localhost',
    'port': 5432,
    'database': 'Valute_info',
    'user': 'postgres',
    'password': '12345'
}

def export():
    conn = psycopg2.connect(**connecting)
    cur = conn.cursor()

    cur.execute("""
        SELECT date, code, name, avg_value, max_value, min_value, count_measurements
        FROM valuti_stats
        ORDER BY date DESC, code
    """)
    rows = cur.fetchall()

    if not rows:
        print("Нет данных для экспорта")
        conn.close()
        return

    filename = f"currency_report_{datetime.now().strftime('%Y-%m-%d')}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Дата", "Код", "Валюта", "Средний", "Макс", "Мин", "Замеров"])
        writer.writerows(rows)

    cur.close()
    conn.close()

    print(f"Экспортировано {len(rows)} строк в {filename}")


if __name__ == "__main__":
    export()