# Назначение программы
Набор программ Quality Gate осуществляет предрелизную проверку сервиса на соответствие требованиям SRE

## Расположение заданий в Jenkins

### Версия ПСИ, которая и есть основная
https://nlb-jenkins-sigma-psi.sigma.mvv.ru/global/job/HR_CI01978215/job/SRE/job/quality_gate/

### Версия ДЕВ, для разработки
https://test-jenkins.sigma.mvv.ru/marsh/job/HR-PLATFORM/job/SRE/job/quality_gate/


# Сборка программы
В ветке _dev_ проходит разработка, ветка _uat_ используется для сборки приложения для дальнейшего использования на ПСИ.

## Задание Jenkins для сборки
* Откройте https://test-jenkins.sigma.mvv.ru/marsh/job/HR-PLATFORM/job/SRE/job/build_app_distributive/build?delay=0sec и выберите _quality_gate_ из выпадающего списка.
* Запомните номер сборки задания. Обычно он выглядит как _Build #72 (26 окт. 2022 г., 14:22:50)_. Вам нужна цифра **72** из этой строки.
* Откройте _Jenkinsfile_ из этого репозитория и впишите новую версию собранного приложения в значение переменной **TOOL_VERSION**.
* Сохраните изменения на сервер Bitbucket.
* Новая версия приложения тут же начнёт работать.
