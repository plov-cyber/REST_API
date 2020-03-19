from requests import put

# Корректный запрос
print(put('http://127.0.0.1:5000/api/jobs/1', json={
    'job': 'Learning Flask',
    'team_leader': 1,
    'work_size': 20,
    'collaborators': '5, 6',
    'is_finished': 0
}).json())

# Некорректные запросы
print(put('http://127.0.0.1:5000/api/jobs/1', json={  # Отсутствует обязательное поле work_size
    'job': 'Learning C++',
    'team_leader': 2,
    'collaborators': '3, 4',
    'is_finished': 1
}).json())
print(put('http://127.0.0.1:5000/api/jobs/9999', json={  # Несуществующий id
    'job': 'Learning Flask',
    'team_leader': 1,
    'work_size': 20,
    'collaborators': '5, 6',
    'is_finished': 0
}).json())
print(put('http://127.0.0.1:5000/api/jobs/1').json())  # Отсутствует json
