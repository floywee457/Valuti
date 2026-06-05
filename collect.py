import requests
import psycopg2

connecting = {
    'host': 'localhost',
    'port': 5432,
    'database': 'Valute_info',
    'user': 'postgres',
    'password': '12345'
}

def script():
    conn = psycopg2.connect(**connecting)
    cur = conn.cursor()

    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    data = response.json()

    for key, val in data['Valute'].items():
        cur.execute("""
        INSERT INTO valuti(code,name,value,date) VALUES(%s,%s,%s,%s)
        """, (key, val['Name'], val['Value'], data['Timestamp'].replace("T", " ").replace('+03:00', ' ')))

    conn.commit()
    cur.close()
    conn.close()

    print(f"Собрано {len(data['Valute'])} валют")


if __name__ == "__main__":
    script()