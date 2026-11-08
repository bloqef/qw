import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

safe_password = "6767"

found_password = "нет"
has_key = "нет"
door_open = "нет"

rooms = ["1)гостиная", "2)кухня", "3)спальня", "4)прихожая", "5)выйти из игры"]

def show_rooms():
    """Показывает доступные комнаты."""

    print("\nТы можешь пойти в:")
    for room in rooms:
        print("-", room)


def visit_living_room():
    """Гостиная: здесь можно найти записку с подсказкой."""

    print("\nТы в гостиной. На столе лежит старая записка.")
    print("На ней написано: «Код спрятан там, где ты спишь».")


def visit_kitchen():
    """Кухня: можно осмотреть холодильник и найти нож."""

    print("\nТы на кухне. Пахнет пылью и старой едой.")


def visit_bedroom():
    """Спальня: здесь спрятан код от сейфа."""

    global found_password 

    print("\nТы в спальне. Стоит кровать и шкаф.")

    choice = input("Осмотреть кровать? (да/нет): ").lower().strip()

    if choice == "да":
        if found_password == "нет":
            print("Под подушкой ты нашёл бумажку с кодом: 6767")
            found_password = "да"
        else:
            print("Ты уже нашёл код:", safe_password)
    else:
        print("Ты ничего не осмотрел.")


def visit_hall():
    """Прихожая: здесь сейф и выходная дверь."""

    global has_key
    global door_open

    print("\nТы в прихожей. Здесь стоит сейф и входная дверь.")

    choice = input("Что делать? 1)сейф/2)дверь/3)назад: ").lower().strip()

    if choice == "1":
        open_safe()

    elif choice == "2":
        if has_key == "да":
            print("Ты вставил ключ, повернул его...")
            door_open = "да"
        else:
            print("Дверь заперта. Нужен ключ.")

    else:
        print("Ты возвращаешься в коридор.")


def open_safe():
    """Открывает сейф, если введён правильный код."""

    global has_key

    if found_password == "нет":
        print("Ты не знаешь код. Возможно, он спрятан в другой комнате.")

    code = input("Введи код от сейфа: ").strip()

    if code == safe_password:
        print("Сейф открылся!")

        if has_key == "нет":
            has_key = "да"
    else:
        print("Неверный код. Сейф остался закрыт.")


def play():

    while door_open == "нет":
        clear_screen()
        print("\nТы стоишь в коридоре.")
        show_rooms()

        choice = input("Куда пойти? ").lower().strip()

        if choice == "1":
            visit_living_room()

        elif choice == "2":
            visit_kitchen()

        elif choice == "3":
            visit_bedroom()

        elif choice == "4":
            visit_hall()

        elif choice == "5":
            print("Ты вышел из игры.")
            break

        else:
            print("Такой комнаты нет. Попробуй ещё раз.")
        input("\nНажми Enter, чтобы вернуться в коридор...")

    if door_open == "да":
        print("\nТы выбрался из дома")

play()