import json
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lib import base_action


class NexusProject(base_action.OpsAnyCoreRestAPI):
    def download_nexus_project(self, download_url):
        API = "/api/c/compapi/devops/nexus_project/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_access_token": self.access_token,
            "download_url": download_url
        }
        URL = self.api_url + API
        response = requests.post(url=URL, json=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("data"):
            return True, end_data.get("data")
        return False, end_data.get("message")

    def post_file(self, host_list, file_url, file_path):
        API = "/api/c/compapi/control/post_file/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_access_token": self.access_token,
            "host_list": host_list,  # [unique1, unique2, unique3]
            "file_url": file_url,
            "file_path": file_path
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

    def run(self, host_list, project_dir, download_url, timeout=600):
        status, get_url = self.download_nexus_project(download_url)
        print("get_url", get_url)
        if not status:
            return False, {"success": {}, "error": {"message": "download nexus project error({})".format(get_url)}}

        requests_id = self.post_file(host_list, file_url=get_url, file_path=project_dir)
        if not requests_id:
            return False, {"success": [], "error": {"message": "config error requests_id doesn't exist"}}
        return self.get_return(requests_id)


if __name__ == '__main__':
    host_list = ["dev_node2"]
    project_dir = "/data/"
    download_url = ""
    res = NexusProject().run(host_list, project_dir, download_url)
    print(res)
