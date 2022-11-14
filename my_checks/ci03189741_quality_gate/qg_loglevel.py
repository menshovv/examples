import os
import json
import argparse
import time
import config_loglevel
import requests
import re
from requests.structures import CaseInsensitiveDict
import yaml
from pprint import pprint


host = (config_loglevel.victoriametrics_hosts['uat'])
host_shoulder = (config_loglevel.victoriametrics_hosts['uat_shoulder'])

#Добавляем переменные из Jenkins в Python
parser = argparse.ArgumentParser(description="QG replications")
parser.add_argument("--app-name", required=True)
parser.add_argument("--workspace", required=True)
args = parser.parse_args()

application_name = args.app_name
print(application_name)

exclude_conf = args.workspace+"/exclude_loglevel.txt"  
bb_conf = args.workspace+"/config-repo/resources/configs/projects-config.yaml"

#Обьявляем переменные для составления POST запроса
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Authorization"] = "Basic dweduh2yu3guy23ye2ig"
Ttime = int(time.time()) - 100
print(Ttime)

kubernetes_name='{'+f'kubernetes_name="{application_name}",job="loglevel"'+'}'
data = f'match[]=probe_success{kubernetes_name}&start={Ttime}&end={Ttime}'
print(data)

#Читаем файл с исключениями
file=open(exclude_conf,'r')
text=file.read()

#Читаем DevOps configmap
with open(bb_conf) as f:
    templates = yaml.safe_load(f)

#Осуществляем проверку переменных
if application_name not in templates:
    print(application_name, 'Некорректно указано имя сервиса')
    exit("'Имя сервиса указано некорректно или отсутствует'")

#Читаем DevOps configmap
with open(bb_conf) as f:
    templates = yaml.safe_load(f)

#Проверка сервиса на тип сервиса = %Backend%
config_devops = []
service_type = []
config_devops = str(templates.get(application_name)['serviceType'])
print(config_devops)
service_type = re.search("backend", config_devops)
print(service_type)

#Проверяем тип сервиса
if service_type == None:
    print('ERROR')
    print('QG проверяет только сервиса типа BACK')
    exit(0)
else:
    if service_type == None and application_name in text:
        print('Некорректный тип сервиса', service_type)
        print(application_name, 'Cервис присутствует в исключениях')
        print('SUCCESS')

#Дергаем метрику из Viktoriametrics
resp = None
try:
    resp = requests.post(f"{host}/api/v1/export", headers=headers, data=data, verify=False)
except requests.exceptions.ConnectionError:
    print("Failed to establish a new connection with Victoriametrics")
if resp is None:
    resp = requests.post(f"{host_shoulder}/api/v1/export", headers=headers, data=data, verify=False)
    print(f"Trying to get data from shoulder endpoint {host_shoulder}")
    
print(resp.json())             


#Проверяем статус отдаваемой метрики, по задаче HRPRUN-19311 предпологается что если probe_success 1, то effectiveLevel = INFO
loglevel = int(resp.json().get('values')[0])
print(loglevel)
if loglevel == 1:
    print('SUCCESS')
else: 
    print('FAILURE')
    exit('Уровень логирования отличен от требуемого INFO')