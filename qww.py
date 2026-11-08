import tkinter as tk

inventory = []

safe_password = "6767"

def clear_buttons():
    """Удаляет кнопки предыдущей комнаты."""

    for button in buttons_frame.winfo_children():
        button.destroy()


def add_button(text, action):
    """Создаёт кнопку и связывает её с функцией."""

    button = tk.Button(
        buttons_frame,
        text=text,
        command=action,
        font=("Arial", 12),
        width=28
    )
    button.pack(pady=4)


def show_scene(text):
    """Меняет текст сцены и убирает старые элементы."""

    story_label.config(text=text)

    clear_buttons()

    code_entry.pack_forget()


def update_inventory():
    """Обновляет текст инвентаря в окне."""

    if len(inventory) == 0:
        inventory_label.config(text="Инвентарь: пусто")

    else:
        text = "Инвентарь:"

        for item in inventory:
            text = text + "\n- " + item

        inventory_label.config(text=text)

def show_corridor():
    show_scene(
        "Ты заперт в доме.\n"
        "Найди код от сейфа, забери ключ и открой дверь.\n\n"
        "Ты стоишь в коридоре. Куда пойдёшь?"
    )

    add_button("1. Гостиная", visit_living_room)
    add_button("2. Кухня", visit_kitchen)
    add_button("3. Спальня", visit_bedroom)
    add_button("4. Прихожая", visit_hall)
    add_button("5. Выйти из игры", window.destroy)


def visit_living_room():
    show_scene(
        "Ты в гостиной.\n\n"
        "На столе выцарапана подсказка:\n"
        "«Код спрятан там, где ты спишь»."
    )

    add_button("Вернуться в коридор", show_corridor)

def visit_kitchen():
    show_scene(
        "Ты на кухне.\n\n"
        "На столе лежит старый журнал.\n"
        "В нём написано: «Запасной ключ хранится в сейфе»."
    )

    add_button("Вернуться в коридор", show_corridor)

def visit_bedroom():
    show_scene(
        "Ты в спальне.\n\n"
        "Здесь стоят кровать и шкаф.\n"
        "Может быть, стоит заглянуть под подушку?"
    )

    add_button("Осмотреть кровать", inspect_bed)
    add_button("Вернуться в коридор", show_corridor)

def inspect_bed():
    if "записка с кодом" not in inventory:
        inventory.append("записка с кодом")

        show_scene(
            "Под подушкой ты нашёл записку!\n\n"
            "На ней написан код: " + safe_password + "\n\n"
            "Записка добавлена в инвентарь."
        )

        update_inventory()

    else:
        show_scene(
            "Ты уже забрал записку.\n\n"
            "Код от сейфа: " + safe_password
        )

    add_button("Вернуться в спальню", visit_bedroom)
    add_button("Вернуться в коридор", show_corridor)

def visit_hall():
    show_scene(
        "Ты в прихожей.\n\n"
        "Перед тобой запертая дверь.\n"
        "Рядом стоит сейф с кодовым замком."
    )

    add_button("Открыть сейф", show_safe)
    add_button("Открыть дверь", open_door)
    add_button("Вернуться в коридор", show_corridor)

def show_safe():
    # Если ключ уже взят, вводить код повторно не нужно.
    if "ключ" in inventory:
        show_scene(
            "Сейф уже открыт и пуст.\n"
            "Ключ находится в твоём инвентаре."
        )

        add_button("Вернуться в прихожую", visit_hall)

    else:
        text = "Введи код от сейфа."

        if "записка с кодом" in inventory:
            text = text + "\nКод на твоей записке: " + safe_password
        else:
            text = text + "\nПодсказка спрятана в одной из комнат."

        show_scene(text)

        # Убираем ранее введённый пароль.
        code_entry.delete(0, tk.END)

        # Показываем поле ввода.
        code_entry.pack(pady=8)
        code_entry.focus_set()

        add_button("Проверить код", check_code)
        add_button("Вернуться в прихожую", visit_hall)


def check_code():
    # Получаем текст из поля ввода.
    code = code_entry.get().strip()

    if code == safe_password:
        if "ключ" not in inventory:
            inventory.append("ключ")

        update_inventory()

        show_scene(
            "Код верный! Сейф открылся.\n\n"
            "Ты забрал ключ.\n"
            "Теперь можно открыть выходную дверь!"
        )

        add_button("Вернуться в прихожую", visit_hall)

    else:
        story_label.config(
            text="Неверный код.\n"
                 "Попробуй ещё раз или поищи подсказку."
        )

        code_entry.delete(0, tk.END)
        code_entry.focus_set()

def open_door():
    if "ключ" in inventory:
        show_scene(
            "Ты вставил ключ и повернул его.\n\n"
            "Дверь открылась!\n"
            "Ты выбрался из дома. Победа!"
        )

        add_button("Играть снова", restart_game)
        add_button("Закрыть игру", window.destroy)

    else:
        show_scene(
            "Дверь заперта!\n\n"
            "Нужно найти ключ.\n"
            "Возможно, он лежит в сейфе."
        )

        add_button("Вернуться в прихожую", visit_hall)


def restart_game():
    # Удаляем все предметы из существующего списка.
    inventory.clear()

    update_inventory()
    show_corridor()

window = tk.Tk()
window.title("Побег из дома")
window.geometry("600x620")

title_label = tk.Label(
    window,
    text="ПОБЕГ ИЗ ДОМА",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=15)

story_label = tk.Label(
    window,
    text="",
    font=("Arial", 13),
    wraplength=540,
    justify="center"
)
story_label.pack(pady=10)

# Отдельное место для поля ввода пароля.
input_frame = tk.Frame(window)
input_frame.pack()

code_entry = tk.Entry(
    input_frame,
    font=("Arial", 14),
    justify="center",
    width=15
)

# Отдельное место для кнопок комнат.
buttons_frame = tk.Frame(window)
buttons_frame.pack(pady=10)

inventory_label = tk.Label(
    window,
    text="Инвентарь: пусто",
    font=("Arial", 12),
    justify="left",
    anchor="w"
)
inventory_label.pack(
    side="bottom",
    fill="x",
    padx=20,
    pady=15
)


show_corridor()
window.mainloop()