import json
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lib import base_action


class GitlabCloneProject(base_action.OpsAnyCoreRestAPI):
    def run_shell(self, host_list, command):
        API = "/api/c/compapi/control/post_shell/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_access_token": self.access_token,
            "host_list": host_list,  # [unique1, unique2, unique3]
            "command": command
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

    def run(self, host_list, project_dir, project_url, api_token, project_branch="master"):
        project_url_split = project_url.split("//")
        if len(project_url_split) != 2:
            return False, {"error": "project_url error"}
        api_token_url = "{http}//oauth2:{api_token}@{url}".format(http=project_url_split[0], api_token=api_token, url=project_url_split[-1])

        command = "cd {project_dir} && git clone -b {project_branch} {api_token_url}".format(
            project_dir=project_dir,
            project_branch=project_branch,
            api_token_url=api_token_url
        )
        requests_id = self.run_shell(host_list, command)
        if not requests_id:
            return False, {"success": [], "error": {"message": "config error requests_id doesn't exist"}}
        return self.get_return(requests_id)


if __name__ == '__main__':
    host_list = []
    project_dir = ""
    project_branch = "develop"
    project_url = ""
    api_token = ""
    res = GitlabCloneProject().run(host_list, project_dir, project_branch, project_url, api_token)
    print("res", res)
