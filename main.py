import requests
import os

from datetime import date
from dateutil.relativedelta import relativedelta
from terminaltables import AsciiTable
from dotenv import load_dotenv


def predict_salary(salary_from, salary_to):

    if salary_from and salary_to:

        expected_salary = (salary_from + salary_to)/2
    else:

        if salary_from:

            expected_salary = salary_from * 1.2  

        else:

            expected_salary = salary_to * 0.8

    return expected_salary

  
def predict_rub_salary(vacancy):

    expected_salary = None

    if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':

        expected_salary = predict_salary(vacancy['salary']['from'], vacancy['salary']['to'])
  
    return expected_salary


def predict_rub_salary_sj(vacancy):

    expected_salary = None 
    
    if (vacancy['payment_from'] or vacancy['payment_to']) and vacancy['currency'] == 'rub':

        expected_salary = predict_salary(vacancy['payment_from'], vacancy['payment_to'])
  
    return expected_salary


def print_table(languages_information, title):

    table_data = [['Язык программирования','Вакансий найдено',
                   'Вакансий обработано','Средняя зарплата']]
    
    for language, language_information in languages_information.items():
    
      table_data.append([language,            
                         language_information['vacancies_found'],
                         language_information['vacancies_processed'],
                         language_information['average_salary']
                        ])
      
    table = AsciiTable(table_data, title)
    print(table.table)


def get_hh_information(programming_languages):

    url_hh = 'https://api.hh.ru/vacancies'

    languages_information_hh = {}

    salaries_hh = []

    for programming_language in programming_languages :
    
        params_hh = {  
                'text' : f'Программист {programming_language}',
                'area' : 1,
                'date_from': date.today() - relativedelta(months=1)
        }
      
        response_hh = requests.get(url_hh, params=params_hh)
      
        response_hh.raise_for_status()
      
        response_hh_formatted = response_hh.json()
      
        sum_vacancies_hh = response_hh_formatted['found']
      
        vacancies_hh = response_hh_formatted['items']
      
        vacancies_processed_hh = 0
      
        salaries_hh.clear()
      
        for vacancy_hh in vacancies_hh :
      
            expected_salary_hh = predict_rub_salary(vacancy_hh)
      
            if expected_salary_hh:
            
                salaries_hh.append(expected_salary_hh)
      
                vacancies_processed_hh += 1
              
        if  salaries_hh :
        
            average_salary_hh = sum(salaries_hh)/len(salaries_hh)
      
        else:
      
            average_salary_hh = 'Вакансий не найдено'
        
        languages_information_hh[programming_language] = { 
              "vacancies_found": sum_vacancies_hh,
              "vacancies_processed": vacancies_processed_hh,
              "average_salary": average_salary_hh
          }
      
    return languages_information_hh


def get_sj_information(programming_languages, key_sj):
      
    url_sj = 'https://api.superjob.ru/2.0/vacancies/'
    
    languages_information_sj = {}
    
    salaries_sj = []
    
    headers_sj = {
       'X-Api-App-Id':key_sj, 
      }
    
    for programming_language in programming_languages :
    
        params_sj = {
           'keyword': f'Программист {programming_language}',
           'catalogues':33, 
           'town':4
          }
          
        response = requests.get(url_sj, headers=headers_sj, params=params_sj)
        
        response_formatted_sj = response.json()
        
        vacancies_sj = response_formatted_sj['objects']
    
        vacancies_processed_sj = 0
        
        average_salary_sj = 0
        
        salaries_sj.clear()
      
        for vacancy_sj in vacancies_sj:
    
            expected_salary_sj = predict_rub_salary_sj(vacancy_sj)
        
            if expected_salary_sj:
              
                 salaries_sj.append(expected_salary_sj)
    
                 vacancies_processed_sj+=1
        
        if len(salaries_sj):
        
            average_salary_sj = sum(salaries_sj) / len(salaries_sj)
    
        else:
    
            average_salary_sj = 'Вакансии не найдены'
        
        languages_information_sj[programming_language] = {
                "average_salary": average_salary_sj,
                "vacancies_found": response_formatted_sj['total'],
                "vacancies_processed": vacancies_processed_sj
        }
    
    return languages_information_sj


if __name__ == "__main__":

  load_dotenv()

  key_sj = os.environ['KEY_SUPER_JOB']

  programming_languages = ['JavaScript','Java','Python','Ruby','PHP','C++','C#', 'C']

  languages_information_hh = get_hh_information(programming_languages)

  languages_information_sj = get_sj_information(programming_languages, key_sj)

  print_table(languages_information_hh, 'HeadHunter Moscow')

  print_table(languages_information_sj, 'SuperJob Moscow')
  











