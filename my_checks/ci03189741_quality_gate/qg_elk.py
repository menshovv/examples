import json
import config_elk
import argparse
import time
from time import sleep
from datetime import datetime
import elasticsearch
from elasticsearch import Elasticsearch, helpers

#Добавляем переменные из Jenkins в Python
parser = argparse.ArgumentParser(description="QG replications")
parser.add_argument("--app-name", required=True)
parser.add_argument("--workspace", required=True)
args = parser.parse_args()

application_name = args.app_name
print(application_name)

# application_name = 'spine-datalab-importer'

ELASTIC_PASSWORD = config_elk.ELASTIC_PASSWORD
ELASTIC_USER = config_elk.ELASTIC_USER

#Добавляем файл с исключениями
exclude_conf = args.workspace+"/exclude_elk.txt"  

#Читаем файл с исключениями
file=open(exclude_conf,'r')
text=file.read()

if application_name in text:
    print('Сервис присутствует в исключениях')
    exit(0)

gte = int(time.time()) - 500
print(gte)
lte = int(time.time()) 
print(lte)

json_conf_traceid = config_elk.get_json_traceid(application_name,gte,lte)
json_conf_span = config_elk.get_json_traceid(application_name,gte,lte)

sleep_time = config_elk.sleep_time
num_retries  = config_elk.sleep_time

es = elasticsearch.Elasticsearch(
    host="hr-log-uat.menshovv.ru",
    port = 9243,
    verify_certs=True,
    ca_certs=args.workspace+"/testca.pem",
    # ca_certs="/Users/19689700/ci03189741_quality_gate/testca.pem",
    use_ssl=True,
    http_auth=(ELASTIC_USER, ELASTIC_PASSWORD))


def get_traceid(sleep_time, num_retries):
    for x in range(0, num_retries):  
        try:
            res = helpers.scan(
                client = es,
				# scroll = '1s',
                query = json_conf_traceid)
            print("Trying to catch some elk data")
            str_error = None
            for i in res:
                json_str = json.dumps(i)
                dict_json = json.loads(json_str)
                traceid = dict_json["_source"]["doc"]["traceid"]
            if traceid != None:
                return traceid
            else:
                str_error = "Error, no data found"
                print(str_error)
        except Exception as e:
            str_error = str(e)

        if str_error:
            sleep(sleep_time)  # wait before trying to fetch the data again
            sleep_time *= 2  # Implement your backoff algorithm here i.e. exponential backoff
        else:
            break

def get_span(sleep_time, num_retries):
    for x in range(0, num_retries):  
        try:
            res = helpers.scan(
                client = es,
				# scroll = '1s',
                query = json_conf_span)
            print("Trying to catch some elk data")
            str_error = None
            for i in res:
                json_str = json.dumps(i)
                dict_json = json.loads(json_str)
                traceid = dict_json["_source"]["doc"]["traceid"]
            if traceid != None:
                return traceid
            else:
                str_error = "Error, no data found"
                print(str_error)
        except Exception as e:
            str_error = str(e)

        if str_error:
            sleep(sleep_time)  # wait before trying to fetch the data again
            sleep_time *= 2  # Implement your backoff algorithm here i.e. exponential backoff
        else:
            break

if get_traceid(sleep_time, num_retries) !=None:
    print('Traceid присутствует в сервисе')
else:
    exit('Traceid не обнаружен')

if get_span(sleep_time, num_retries) !=None:
    print('Spanid присутствует в сервисе')
else:
    exit('Spanid не обнаружен')