import pickle


# Шаблон
user_dict_template: dict = {'page': 1,
                            'bookmarks': set()}

# Инициализируем "базу данных"
with open('database/database.pkl', 'rb') as file:
    users_dt: dict = pickle.load(file)


def save_progress():
    '''Функция сохраняет текущее состояние'''

    with open('database/database.pkl', 'wb') as file:
        pickle.dump(users_dt, file)
