token = "ur_data"

import requests
from datetime import datetime, timedelta

ACCESS_TOKEN = token
A = 235  # ID беседы
CHAT_ID = 2000000000 + A

# Функция для получения ближайшего воскресенья
def get_next_sunday():
    today = datetime.today()
    days_until_sunday = (6 - today.weekday()) % 7  # 6 - это воскресенье
    next_sunday = today + timedelta(days=days_until_sunday)
    return next_sunday.strftime('%d.%m.%y')  # Форматируем как "День.Месяц.Год" (например, "23.03.25")

# Предустановленные опросы
polls = {
    1: {
        'question': 'НИИ, {date}?',
        'options': ['1.1 Еду на тачке, с севера, подкину от башни', '1.2 Еду на тачке с юга, подкину (москвская? - пиши ниже от куда)', '1.3 Хочу в тачку, с севера (башня)Среда', '1.4 Хочу в тачку, с юга (московская? - от водилы зависит)', '1.5 Доеду сам', '2.1 Вся снаряга своя', '2.2 Нужно всё (под вопросом)', 'Я слабый диванный воин'],
        'message': "@all Тренировка {date} на полигоне НИИ связи (м. Электросила, Варшавская ул 11), сбор у полигона в 10.30. \n\n Клубной снаряги к сожалению пока нет, поэтому едем только со всем своим/договариваемся одолжить.\n\nСбор в 10.30 у полигона, в 11.00 начинаем убирать полигон, в 13.00 заканчиваем работать (мб раньше, если много сделаем) и начинаем тренировку. Покатаем интересные сценарии с доставкой флага, штурм/оборона и т.д. Полигон закрытый, но без отопления, поэтому во время уборки желательно быть одетым хотя бы в 2 слоя, иметь балаклаву от пыли.\n\nС водилами договариваться лично и обязательно скинуть деньгу на бенз, водилам просьба написать откуда стартуете.\n\n‼️Обращаю внимание на необходимость посещать минимум 1 тренировку в месяц! В противном случае в дальнейшем будет исключение. Также важно голосовать в любых опросах даже если вы не едете на игру."
    },
    2: {
        'question': 'Какую еду вы предпочитаете?',
        'options': ['Пицца', 'Бургеры', 'Суши', 'Салаты'],
        'message': "Этот опрос поможет нам узнать, какую еду вы предпочитаете. Выберите из предложенных вариантов."
    },
    3: {
        'question': 'Какой цвет вам нравится?',
        'options': ['Красный', 'Синий', 'Зеленый', 'Желтый', 'Черный'],
        'message': "Мы хотим узнать, какой цвет вам нравится. Пожалуйста, выберите один из вариантов."
    },
}

# Печать всех доступных опросов с вариантами
def print_poll_choices():
    next_sunday = get_next_sunday()  # Получаем ближайшее воскресенье
    print("Доступные опросы:")
    for key, poll in polls.items():
        # Формируем вопрос и сообщение с актуальной датой
        question = poll['question'].format(date=next_sunday)
        message = poll['message'].format(date=next_sunday)
        print(f"{key}. {question}")
        print(f"Сообщение: {message}")
        for idx, option in enumerate(poll['options'], 1):
            print(f"   {idx}. {option}")
        print()  # Печатаем пустую строку между опросами

# Функция для создания опроса
def create_poll(question, answers):
    poll_create_url = "https://api.vk.com/method/polls.create"
    poll_params = {
        "access_token": ACCESS_TOKEN,
        "v": "5.131",
        "question": question,
        "add_answers": str(answers).replace("'", '"'),
        "is_anonymous": 0,
        "is_multiple": 1
    }
    poll_response = requests.post(poll_create_url, params=poll_params).json()
    poll_id = poll_response.get("response", {}).get("id")
    owner_id = poll_response.get("response", {}).get("owner_id")
    return poll_id, owner_id

# Функция для отправки опроса с текстом в чат
def send_poll_with_text_to_chat(poll_id, owner_id, message_text=""):
    send_url = "https://api.vk.com/method/messages.send"
    send_params = {
        "access_token": ACCESS_TOKEN,
        "v": "5.131",
        "peer_id": CHAT_ID,
        "message": message_text,  # Текстовое сообщение
        "attachment": f"poll{owner_id}_{poll_id}",  # Вложение (опрос)
        "random_id": 0
    }
    requests.post(send_url, params=send_params)

# Основная логика
def main():
    print_poll_choices()  # Печатаем все доступные опросы

    # Получаем выбор пользователя
    selected_poll = None
    while selected_poll not in polls:
        try:
            selected_poll = int(input("Выберите номер опроса: "))  # Ожидаем выбора пользователя
        except ValueError:
            pass  # Игнорируем, если пользователь ввел не число

    # Получаем данные выбранного опроса
    selected_poll_data = polls[selected_poll]
    next_sunday = get_next_sunday()  # Получаем дату ближайшего воскресенья
    question = selected_poll_data["question"].format(date=next_sunday)
    answers = selected_poll_data["options"]
    message = selected_poll_data["message"].format(date=next_sunday)  # Сообщение с датой

    # Создаем опрос
    poll_id, owner_id = create_poll(question, answers)

    # Отправляем опрос и текст в чат
    send_poll_with_text_to_chat(poll_id, owner_id, message)

    print(f"Опрос '{question}' успешно отправлен в чат с текстом: {message}")

# Запуск программы
if __name__ == "__main__":
    main()
