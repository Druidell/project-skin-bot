import mss
import numpy as np
from PIL import Image
import keyboard
import time
import os
import hashlib
import winsound
import pyautogui
import random
from win10toast import ToastNotifier
from hash_db import HASH_DB

# ===============================
# НАСТРОЙКИ
# ===============================

# Области скриншота (ПОМЕНЯЙ ПОД СЕБЯ)
LEFT_AREA = {"top": 284, "left": 273, "width":699, "height": 453}
RIGHT_AREA = {"top": 284, "left": 996, "width": 699, "height": 453}

# ОБЛАСТИ КНОПОК (x1, y1, x2, y2)
LOWER_BUTTON_AREA = (1012, 764, 1143, 827)   # "Нижний"
HIGHER_BUTTON_AREA = (1350, 766, 1450, 830) # "Выше"

# ЗАДЕРЖКИ (в секундах)
CLICK_DELAY_MIN = 0.05   # 5 мс
CLICK_DELAY_MAX = 0.25   # 25 мс

# ===============================
# СЛУЖЕБНОЕ
# ===============================

BASE_DIR = os.path.dirname(__file__)
UNKNOWN_DIR = os.path.join(BASE_DIR, "unknown")
os.makedirs(UNKNOWN_DIR, exist_ok=True)

toaster = ToastNotifier()

# pyautogui максимально быстро
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0

# ===============================
# ЗВУКИ
# ===============================

def sound_success():
    winsound.Beep(1200, 180)

def sound_error():
    winsound.Beep(400, 500)

# ===============================
# СКРИНШОТ
# ===============================

def grab_area(area):
    with mss.mss() as sct:
        img = np.array(sct.grab(area))
        return Image.fromarray(img)

# ===============================
# HASH (ПИКСЕЛЬ В ПИКСЕЛЬ)
# ===============================

def get_hash(img):
    return hashlib.sha256(img.tobytes()).hexdigest()

# ===============================
# РАНДОМНЫЙ КЛИК ПО ОБЛАСТИ
# ===============================

def random_click(area):
    x1, y1, x2, y2 = area

    x = random.randint(x1, x2)
    y = random.randint(y1, y2)

    delay = random.uniform(CLICK_DELAY_MIN, CLICK_DELAY_MAX)
    time.sleep(delay)

    pyautogui.click(x, y)

# ===============================
# АВТОКЛИК
# ===============================

def click_site(result):
    if result == "LOWER":
        random_click(LOWER_BUTTON_AREA)
    else:
        random_click(HIGHER_BUTTON_AREA)

# ===============================
# НЕУДАЧА
# ===============================

def handle_fail(img, side, hash_value, known=None):
    img.save(os.path.join(UNKNOWN_DIR, f"{side}_{hash_value}.png"))
    sound_error()

    text = f"{side} НЕ НАЙДЕН\nHash:\n{hash_value}"

    if known:
        text += (
            f"\n\nДРУГОЙ НАЙДЕН:\n"
            f"Hash:\n{known['hash']}\n"
            f"Цена: {known['price']} ₽"
        )

    toaster.show_toast("Неудача", text, duration=1, threaded=True)
    print("\nНЕУДАЧА")
    print(text)
    print("\nЖди следующий F8\n")

# ===============================
# УСПЕХ
# ===============================

def handle_success(lh, lp, rh, rp):
    result = "HIGHER" if rp > lp else "LOWER"
    sound_success()

    text = (
        f"РЕЗУЛЬТАТ:\n"
        f"{'✅ ВЫШЕ' if result == 'HIGHER' else '❌ НИЖНИЙ'}\n\n"
        f"ЛЕВЫЙ:\nHash:\n{lh}\nЦена: {lp} ₽\n\n"
        f"ПРАВЫЙ:\nHash:\n{rh}\nЦена: {rp} ₽\n\n"
    )

    toaster.show_toast("Успех", text, duration=1, threaded=True)
    print("\nУСПЕХ")
    print(text)

    click_site(result)
    print("Автоклик выполнен\n")

# ===============================
# ОСНОВНОЙ ЦИКЛ
# ===============================

def main():
    print("▶ Программа запущена")
    print("▶ Нажимай F8 для анализа\n")

    while True:
        keyboard.wait("F8")

        left_img = grab_area(LEFT_AREA)
        right_img = grab_area(RIGHT_AREA)

        left_hash = get_hash(left_img)
        right_hash = get_hash(right_img)

        left_ok = left_hash in HASH_DB
        right_ok = right_hash in HASH_DB

        if left_ok and right_ok:
            handle_success(
                left_hash, HASH_DB[left_hash],
                right_hash, HASH_DB[right_hash]
            )
            continue

        if left_ok and not right_ok:
            handle_fail(
                right_img, "RIGHT", right_hash,
                {"hash": left_hash, "price": HASH_DB[left_hash]}
            )
            continue

        if right_ok and not left_ok:
            handle_fail(
                left_img, "LEFT", left_hash,
                {"hash": right_hash, "price": HASH_DB[right_hash]}
            )
            continue

        handle_fail(left_img, "LEFT", left_hash)

# ===============================
if __name__ == "__main__":
    main()