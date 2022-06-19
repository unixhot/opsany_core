import json
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lib import base_action


class ControlRunCommand(base_action.OpsAnyCoreRestAPI):
    def run_script(self, host_list, script_url, script_arg):
        API = "/api/c/compapi/control/post_script/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_access_token": self.access_token,
            "host_list": host_list,  # [unique1, unique2, unique3]
            "script_url": script_url,
            "script_arg": script_arg
        }
        URL = self.api_url + API
        response = requests.post(url=URL, json=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("data"):
            return end_data.get("data")
        return ""

    def get_request_id_status(self, request_id):
        API = "/api/c/compapi/control/get_request_id_status/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_access_token": self.access_token,
            "request_id": request_id
        }
        URL = self.api_url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("data"):
            return end_data.get("data")
        return []

    def run(self, host_list, shell_command):
        requests_id = self.run_script(host_list, shell_command, "")
        if not requests_id:
            return False, {"success": [], "error": {"message": "config error requests_id doesn't exist"}}
        return self.get_return(requests_id)


if __name__ == '__main__':
    host_list, script_url = ["dev_node2"], r"/uploads/"
    ControlRunCommand().run(host_list, script_url)
