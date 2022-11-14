import sys

import yaml

excluded_services = [
    "app-careerop-model-input",
    "app-careerop-model-job",
    "app-careerop-model-team",
    "app-careerop-model-trainer",
    "app-careerop-model-vacancy",
    "app-da-chatbot-middleware-survey",
    "app-job-profile-scheduler",
    "app-job-profile-marketplace-uploader",
    "app-learning-feed-proxy",
    "app-learning-feed-trainer",
    "app-smart-calendar-analytics",
    "app-smart-profile-sync",
    "spine-authorization-jobs",
    "PostgreSQL",
    "VM",
    "app-web-virtualtrainer",
    "menshovv-paom-uploader",
    "spine-datalab-importer-core",
    "spine-datalab-bootstrap",
    "spine-keycloak-uploader",
    "spine-local-list",
    "spine-ui-feed",
    "app-recruitment-connector-skillaz",
]


def run(app_name, workspace):
    bb_conf = workspace + "/config-repo/resources/configs/projects-config.yaml"
    print(app_name)

    # Читаем DevOps configmap
    with open(bb_conf) as f:
        templates = yaml.safe_load(f)

    # Осуществляем проверку переменных
    if app_name not in templates:
        print(f"Некорректно указано имя сервиса '{app_name}'")
        print("Имя сервиса указано некорректно или отсутствует")
        sys.exit(1)
    if workspace == "":
        print(f"Некорректно указан workspace '{workspace}' для сервиса '{app_name}'", file=sys.stderr)
        print("Некорректно прокидывается путь, проблемы на агенте", file=sys.stderr)
        sys.exit(1)

    # Парсим yml с исключениями
    try:
        bb_repl = int(templates.get(app_name)["environment"]["PROM"]["resources"]["replicas"])
    except KeyError:
        bb_repl = 1
        print(
            "Колличество реплик меньше чем требуется сервису. Текущее колличество реплик - 1 Требуемое колличество реплик >= 2",
            file=sys.stderr,
        )

    # Осуществляем проверку
    if bb_repl >= 2:
        print("SUCCESS")
        print("Колличество реплик в приложении установлены корректно")
    else:
        if bb_repl == 1 and app_name in excluded_services:
            print("Replications -", bb_repl)
            print(app_name, "Cервис присутствует в исключениях т.к. не умеет в многопоточность")
            print("SUCCESS")
        else:
            print(
                "Колличество реплик меньше чем требуется сервису. Текущее колличество реплик -",
                bb_repl,
                "Требуемое колличество реплик >= 2",
            )
            print("FAILURE", file=sys.stderr)
            print("Колличество реплик меньше чем требуется сервису", file=sys.stderr)
            sys.exit(1)
