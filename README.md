<h1>Подготовка среды</h1>

1) Установка зависимостей

> sudo apt-get install python3-dev python3-pip texlive-fonts-recommended texlive-lang-cyrillic texlive-latex-extra texlive-latex-recommended

2) Создать виртуальное окружение:

> python3 -m venv <venv_name>

3) Активировать виртуальное окружение:

> source <venv_name>/bin/activate

4) Загрузить проект в это окружение:

> git clone https://github.com/moevm/mse_functions_interpolation_and_numerical_integration_tasks.git

5) Установить виртуальное окружение:

> pip3 install -r requirments.txt



<h1>Запуск сервера</h1>

> cd Generator

Запуск (временно) выполняется только из директории `Generator`

> python3 manage.py runserver


<h1>Трекер задач</h1>

[Task tracker](https://github.com/moevm/mse_functions_interpolation_and_numerical_integration_tasks/projects/1?add_cards_query=is%3Aopen)

<h1>Сборка через Docker</h1>
<ol>
    <li>Перейдите в каталог, в котором находится файл Dockerfile</li>
    <li>Выполниет следующие команды:
        <ol>
        <li>docker build -t tasks .</li>
        <li>docker run -p 8000:8000 tasks</li>
        </ol>
    </li>
    <li>Откройте браузер по адресу: http://localhost:8000/</li>
</ol>
