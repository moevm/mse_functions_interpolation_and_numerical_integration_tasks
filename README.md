
# Генератор заданий и билетов по вычислительной математике

## Запуск

### Подготовка среды

1. Установите зависимости

```shell
sudo apt-get install python3-dev python3-pip texlive-fonts-extra texlive-lang-cyrillic texlive-lang-greek texlive-latex-recommended
```

2. Создайте виртуальное окружение:

```shell
python3 -m venv <venv_name>
```

3. Активируйте виртуальное окружение:

```shell
source <venv_name>/bin/activate
```

4. Загрузите проект в это окружение:

```shell
git clone https://github.com/moevm/mse_functions_interpolation_and_numerical_integration_tasks.git
```

5. Установите виртуальное окружение:

```shell
pip3 install -r requirements.txt
```

### Запуск сервера

```shell
python3 Generator/manage.py runserver
```

#### Сборка через Dockerfile

1. Перейдите в каталог, в котором находится файл Dockerfile

```shell
cd mse_functions_interpolation_and_numerical_integration_tasks/
```

2. Выполните следующие команды:

```shell
docker build -t tasks .
docker run -p 8000:8000 tasks
```

3. Откройте браузер по адресу: [http://localhost:8000/](http://localhost:8000/)

#### Сборка через DockerHub

1. Выполните следующие команды:

```shell
docker pull mukhamux/tasks:1.0
docker run -p 8000:8000 tasks
```
    
2. Откройте браузер по адресу: [http://localhost:8000/](http://localhost:8000/)

## Тестирование 

**what about unit tests???**

## Состояние задач

[kanban доска](https://github.com/moevm/mse_functions_interpolation_and_numerical_integration_tasks/projects/2)
