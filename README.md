# project-skin-bot

1) Установить Python
Скачать: https://www.python.org/downloads/

Установить библиотеки
pip install mss pillow numpy keyboard win10toast pyautogui

2) Запуск:
python main.py

Результат:
Картинка сохраняется в unknown/

Если хотя бы одного hash нет:
уведомление + звук ошибки

Если оба hash есть:
уведомление + звук успешного выполнения 

3) Важные условия 
Автоклик в случайную точку кнопки
Случайная задержка
Разрешение экрана всегда одинаковое
Масштаб окна 100%
Области скриншота настроены точно
CLICK_DELAY_MIN < CLICK_DELAY_MAX

4) Смена задержки
Например:
Быстро:
CLICK_DELAY_MIN = 0.05
CLICK_DELAY_MAX = 0.12

Медленнее:
CLICK_DELAY_MIN = 0.15
CLICK_DELAY_MAX = 0.35
