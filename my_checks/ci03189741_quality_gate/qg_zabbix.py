import re
import sys

import requests
import yaml
from pyzabbix import ZabbixAPI

import config_zabbix

excluded_services = [
    "app-something-back",
    "app-something-front",
    "etc",
]


def run(app_name, workspace):
    print(app_name)

    # Добавляем конфигурации
    user = config_zabbix.zabbix_creds["user"]
    password = config_zabbix.zabbix_creds["password"]

    # Добавляем devops config
    bb_conf = workspace + "/config-repo/resources/configs/projects-config.yaml"

    # Читаем DevOps configmap
    with open(bb_conf) as f:
        templates = yaml.safe_load(f)

    # Осуществляем проверку переменных
    if app_name not in templates:
        print(f"Некорректно указано имя сервиса: '{app_name}'", file=sys.stderr)
        print("Имя сервиса указано некорректно или отсутствует", file=sys.stderr)
        sys.exit(1)

    # Проверка сервиса на тип сервиса = %Backend%
    config_devops = str(templates.get(app_name)["serviceType"])
    print(config_devops)
    service_type = re.search("frontend", config_devops)

    # Проверяем тип сервиса
    if service_type == None:
        print("WARNING")
        print("QG проверяет только сервисы типа FRONT")
        sys.exit(0)
    else:
        if service_type == None and app_name in excluded_services:
            print("Некорректный тип сервиса", service_type)
            print(app_name, "Cервис присутствует в исключениях")
            print("SUCCESS")

    sess = requests.Session()
    sess.verify = False
    zabbix = ZabbixAPI("https://zabbix.hr-uat.menshovv.ru", sess)
    zabbix.login(f"{user}", f"{password}")
    answer = zabbix.do_request("apiinfo.version")

    if answer == None:
        print("error")
    else:
        print("Authorized Succesfully ")

    def match_application(name, zabbix):
        for element in zabbix.httptest.get(selectSteps=["name"]):
            if element["steps"][0]["name"] == name:
                return True
        return False

    if match_application(app_name, zabbix):
        print("SUCCESS")
    else:
        if app_name in excluded_services:
            print("Сервис ненайден в шаблонах, но присутствует в исключениях")
        else:
            print("ERROR: API cant call for requests")
