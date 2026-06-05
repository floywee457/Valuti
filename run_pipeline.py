import subprocess
import sys
from datetime import datetime


def run_step(name, script):
    print(f"\n{'='*50}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {name}")
    print(f"{'='*50}")

    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True,
        encoding = "utf-8"
    )

    if result.stdout:
        print(result.stdout.strip())

    if result.returncode != 0:
        print(f"ОШИБКА:")
        print(result.stderr)
        return False
    else:
        return True


if __name__ == "__main__":
    print(f"ПАЙПЛАЙН ЗАПУЩЕН: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if run_step("1. Сбор данных", "collect.py"):
        if run_step("2. Трансформация", "transform.py"):
            run_step("3. Экспорт", "export.py")

    print(f"\nПАЙПЛАЙН ЗАВЕРШЁН: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")