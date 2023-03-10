# Сравниваем вакансии программистов

Данный проект создан для скачивания данных о вакансиях с сайтов HeadHunter и SuperJob, с последующим их выводом в консоль в виде таблицы. 

В данной таблице содержится следующая информация :

* Язык программирования;
* Общее количество вакансий; 
* Количество обработанных вакансий; 
* Средняя зарплата.

Для работы с программой вам необходимо запустить файл ```main.py```. 

Ниже описаны функции и пример запуска программы. 


## main.py

Является главным файлом проекта, который в процессе выполнения задействует каждую функцию проекта.

Для запуска программы необходимо выполнить команду: 

```
python main.py
```
Пример запуска программы представлен ниже:

![image](https://user-images.githubusercontent.com/42433463/213409208-eabce8bc-690a-4b2e-90c4-e5a6196cd95e.png)



## get_hh_information

Данная функция принимает на вход список языков и возвращает полученную информацию о вакансиях разных языков программирования.

Для каждого языка функция делает запрос на сайт HeadHunter со следующими параметрами:

* Запрос вакансий с языком программирования;
* Город Москва;
* Вакансии за последний месяц.

После получения информации первоначально функция получает общее количество записей. 

Затем происходит обработка каждой вакансии и с помощью функции ```predict_rub_salary_hh``` получает ожидаемую зарплату на каждой из вакансий. 

Из полученной информации функция определяет среднюю зарплату и количетсво обработанных вакансий

После обработки всех вакансий программа добавляет обработанную информацию в словарь с общей информацией о вакансиях и начинает работу с новым языком. 

После обработки всех языков функция возвращает словарь с общей информацией о вакансиях.


## get_sj_information

Данная функция принимает на вход список языков и возвращает полученную информацию о вакансиях разных языков программирования.

Для каждого языка функция делает запрос на сайт superjob.ru со следующими параметрами:

* Запрос вакансий с языком программирования
* Каталог категорий в котором необходимо искать вакансии
* Город Москва

Из полученной информации функция определяет среднюю зарплату и количетсво обработанных вакансий

После обработки всех вакансий программа добавляет обработанную информацию в словарь с общей информацией о вакансиях и начинает работу с новым языком. 

После обработки всех языков функция возвращает словарь с общей информацией о вакансиях.


## predict_rub_salary_hh

Функция принимает на вход информацию о вакансии и возвращает ожидаемую зарплату на ней.

Данная функция необходима для обработки вакансии полученной с сайта HeadHunter. 

Программа проверяет наличие информации о зарплате в вакансии а также проверяет факт, что зарплата вычисляется в рублях.

Если все условия выполняются, то программа передает нижний и верхний пределы зарплаты в функцию ``` expected_salary``` для определения ожидаемой зарплаты на вакансии.

Результатом работы функции будет данное значение зарплаты


## predict_rub_salary_sj

Функция принимает на вход информацию о вакансии и возвращает ожидаемую зарплату на ней.

Данная функция необходима для обработки вакансии полученной с сайта superjob.ru. 

Программа проверяет наличие одной из границ зарплат (от или до) в вакансии а также проверяет факт, что зарплата вычисляется в рублях.

Если все условия выполняются, то программа передает нижний и верхний пределы зарплаты в функцию ``` expected_salary``` для определения ожидаемой зарплаты на вакансии.

Результатом работы функции будет данное значение зарплаты


## predict_salary

Функция принимает на вход информацию о минимальном и максимальном значении зарплаты и возвращает ожидаемую зарплату.

Изначально функция проверяет наличие обоих значений. При их наличии программа выполняет рассчет ожидаемой зарплаты. 

Если же одно из значений отсутствет, то функция проверяет наличие минимального значения. 

При наличии минимальной зарплаты функция получает ожидаемую зарплату умножив жто значение на 1.2 

Если же минимальное значение отсутствует, то функция получает ожидаемую зарплату умножив максимальное значение зарплаиы на 0.8

После получения ожидаемой зарплаты функция возвращает его


## print_table

Функция принимает на вход общую информацию о вакансиях и название таблицы в которую будет выведена общая информация о вакансиях для каждого языка. 

Изначально создается специальная переменная с заголовками столбцов таблицы. 

Затем для каждого языка программирования в эту переменную добавляетчя соответствующая каждому столбцу информация

Результатом работы программы будет вывод в консоль таблицы с информацией


### Как установить

Для корректной работы программы вам необходимо зарегестрировать приложение по [ссылке регистрации](https://api.superjob.ru/register/)

Затем вам необходимо создать в папке проекта файл ```.env``` и добавить в него ваш API_КЛЮЧ для сайта SuperJob следующего формата:

```
SJ_API_KEY=ВАШ_API_КЛЮЧ

```

Python3 должен быть уже установлен. 

Также вам необходимо установить соответствующие внешние пакеты. Версии данных пакетов вы можете найти в файле requirements.txt

Используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
