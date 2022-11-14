import argparse

import qg
import qg_zabbix

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quality Gate Checks")
    parser.add_argument("--app-name", required=True)
    parser.add_argument("--workspace", required=True)

    args = parser.parse_args()

    qg.run(args.app_name, args.workspace)
    qg_zabbix.run(args.app_name, args.workspace)
