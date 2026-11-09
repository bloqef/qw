import tkinter as tk
from pathlib import Path

inventory = []

safe_password = "6767"

images_folder = Path(__file__).resolve().parent / "images"

def show_image(filename):
    """Загружает картинку и показывает её в окне."""

    image_path = images_folder / filename

    try:
        picture = tk.PhotoImage(file=str(image_path))

        # Максимальная область для картинки: 1000 x 450.
        scale = 1

        while (
            picture.width() > 1000 * scale
            or picture.height() > 450 * scale
        ):
            scale += 1

        if scale > 1:
            picture = picture.subsample(scale, scale)

        image_label.config(
            image=picture,
            text=""
        )

        image_label.image = picture

    except tk.TclError:
        image_label.config(
            image="",
            text=(
                "Не удалось загрузить картинку:\n"
                + str(image_path)
                + "\n\nДобавь подходящий PNG-файл в папку images."
            )
        )

        image_label.image = None

def clear_buttons():
    """Удаляет кнопки предыдущей сцены."""

    for button in buttons_frame.winfo_children():
        button.destroy()

def add_button(text, action):
    """Добавляет кнопку с указанным действием."""

    button = tk.Button(
        buttons_frame,
        text=text,
        command=action,
        font=("Arial", 14),
        width=32,
        bg="#e8e8e8",
        fg="#202020",
        padx=8,
        pady=4
    )

    button.pack(pady=4)

def show_scene(text, image_name):
    """Обновляет текст, картинку и убирает старые кнопки."""

    clear_buttons()

    # Скрываем поле ввода кода, если оно было открыто.
    code_entry.pack_forget()

    story_label.config(text=text)

    show_image(image_name)

def update_inventory():
    """Показывает все предметы из списка inventory."""

    if len(inventory) == 0:
        inventory_label.config(text="Инвентарь: пусто")

    else:
        text = "Инвентарь:"

        for item in inventory:
            text = text + "\n- " + item

        inventory_label.config(text=text)

def add_item(item):
    """Добавляет предмет, если его ещё нет."""

    if item not in inventory:
        inventory.append(item)
        update_inventory()

def show_corridor():
    show_scene(
        "Ты заперт в доме.\n"
        "Найди код от сейфа, забери ключ и открой дверь.\n\n"
        "Ты стоишь в коридоре. Куда пойдёшь?",
        "corridor.png"
    )

    add_button("1. Гостиная", visit_living_room)
    add_button("2. Кухня", visit_kitchen)
    add_button("3. Спальня", visit_bedroom)
    add_button("4. Прихожая", visit_hall)
    add_button("5. Выйти из игры", window.destroy)

def visit_living_room():
    show_scene(
        "Ты в гостиной.\n\n"
        "На столе лежит старая записка:\n"
        "«Код спрятан там, где ты спишь».",
        "living_room.png"
    )

    add_button("Вернуться в коридор", show_corridor)

def visit_kitchen():
    show_scene(
        "Ты на кухне.\n\n"
        "На столе лежит журнал.\n"
        "В нём написано: «Ключ от входной двери хранится в сейфе».",
        "kitchen.png"
    )

    add_button("Вернуться в коридор", show_corridor)

def visit_bedroom():
    show_scene(
        "Ты в спальне.\n\n"
        "Здесь стоят кровать и шкаф.\n"
        "Может быть, стоит заглянуть под подушку?",
        "bedroom.png"
    )

    add_button("Осмотреть кровать", inspect_bed)
    add_button("Вернуться в коридор", show_corridor)


def inspect_bed():
    if "записка с кодом" not in inventory:
        add_item("записка с кодом")

        show_scene(
            "Под подушкой ты нашёл записку!\n\n"
            "Код от сейфа: " + safe_password + "\n\n"
            "Записка добавлена в инвентарь.",
            "bedroom.png"
        )

    else:
        show_scene(
            "Ты уже забрал записку.\n\n"
            "На ней написан код: " + safe_password,
            "bedroom.png"
        )

    add_button("Вернуться в спальню", visit_bedroom)
    add_button("Вернуться в коридор", show_corridor)

def visit_hall():
    show_scene(
        "Ты в прихожей.\n\n"
        "Перед тобой запертая входная дверь.\n"
        "Рядом стоит сейф с кодовым замком.",
        "hall.png"
    )

    add_button("Открыть сейф", show_safe)
    add_button("Открыть дверь", open_door)
    add_button("Вернуться в коридор", show_corridor)

def show_safe():
    if "ключ" in inventory:
        show_scene(
            "Сейф уже открыт и пуст.\n\n"
            "Ключ находится в твоём инвентаре.",
            "safe.png"
        )

        add_button("Вернуться в прихожую", visit_hall)

    else:
        text = "Введи код от сейфа."

        if "записка с кодом" in inventory:
            text = (
                text
                + "\n\nНа найденной записке написано: "
                + safe_password
            )
        else:
            text = (
                text
                + "\n\nПодсказка спрятана в одной из комнат."
            )

        show_scene(text, "safe.png")

        # Очищаем и показываем поле ввода.
        code_entry.delete(0, tk.END)
        code_entry.pack(pady=8)
        code_entry.focus_set()

        add_button("Проверить код", check_code)
        add_button("Вернуться в прихожую", visit_hall)


def check_code():
    # Получаем текст из поля и убираем пробелы по краям.
    code = code_entry.get().strip()

    if code == safe_password:
        add_item("ключ")

        show_scene(
            "Код верный! Сейф открылся.\n\n"
            "Внутри лежит ключ. Ты забрал его.\n"
            "Теперь можно открыть входную дверь!",
            "safe.png"
        )

        add_button("Вернуться в прихожую", visit_hall)

    else:
        story_label.config(
            text=(
                "Неверный код.\n\n"
                "Попробуй ещё раз или поищи записку в спальне."
            )
        )

        code_entry.delete(0, tk.END)
        code_entry.focus_set()

def open_door():
    if "ключ" in inventory:
        show_scene(
            "Ты вставил ключ и повернул его.\n\n"
            "Дверь открылась!\n"
            "Ты выбрался из дома. Победа!",
            "victory.png"
        )

        add_button("Играть снова", restart_game)
        add_button("Закрыть игру", window.destroy)

    else:
        show_scene(
            "Дверь заперта!\n\n"
            "У тебя пока нет ключа.\n"
            "Попробуй открыть сейф.",
            "hall.png"
        )

        add_button("Вернуться в прихожую", visit_hall)


def restart_game():
    """Очищает инвентарь и возвращает в начало."""

    inventory.clear()

    update_inventory()
    show_corridor()

window = tk.Tk()

window.title("Побег из дома")

# Размер окна: ширина 1920, высота 1080 пикселей.
window.geometry("1920x1080")

window.configure(bg="#20242b")

title_label = tk.Label(
    window,
    text="ПОБЕГ ИЗ ДОМА",
    font=("Arial", 26, "bold"),
    bg="#20242b",
    fg="white"
)
title_label.pack(pady=12)

inventory_label = tk.Label(
    window,
    text="Инвентарь: пусто",
    font=("Arial", 14),
    justify="left",
    anchor="w",
    bg="#303640",
    fg="white",
    padx=20,
    pady=10
)
inventory_label.pack(side="bottom", fill="x")

image_frame = tk.Frame(
    window,
    width=1000,
    height=450,
    bg="#15181d"
)
image_frame.pack(pady=5)
image_frame.pack_propagate(False)

image_label = tk.Label(
    image_frame,
    text="",
    font=("Arial", 14),
    wraplength=900,
    bg="#15181d",
    fg="white"
)
image_label.pack(fill="both", expand=True)

story_label = tk.Label(
    window,
    text="",
    font=("Arial", 16),
    wraplength=1200,
    justify="center",
    bg="#20242b",
    fg="white"
)
story_label.pack(pady=12)

input_frame = tk.Frame(window, bg="#20242b")
input_frame.pack()

code_entry = tk.Entry(
    input_frame,
    font=("Arial", 20),
    justify="center",
    width=16
)

buttons_frame = tk.Frame(window, bg="#20242b")
buttons_frame.pack(pady=8)

update_inventory()
show_corridor()

window.mainloop()