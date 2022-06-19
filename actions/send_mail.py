import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lib import base_action


class SendMail(base_action.OpsAnyCoreRestAPI):
    def send_mail(self, receiver, subject, text, text_type):
        API = "/api/c/compapi/workbench/send_mail/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_access_token": self.access_token,
            "operator": "admin",
            "receiver": receiver,
            "subject": subject,
            "text": text,
            "text_type": text_type  # 1： Text  2： Html
        }
        URL = self.api_url + API
        response = requests.post(url=URL, json=req, headers=self.headers, verify=False)
        print(response.text)

        end_data = json.loads(response.text)
        if end_data.get("result"):
            return True, end_data.get("message") or "success"
        else:
            return False, end_data.get("message")

    def run(self, receiver, subject, text):
        status, message = self.send_mail(receiver, subject, text, 1)
        if not status:
            return False, {"success": [], "error": {"message": message}}
        return True, {"success": {"message": message}, "error": []}


if __name__ == '__main__':
    receiver, subject, text = "hu5427@163.com", "主题", "内容"
    res = SendMail().run(receiver, subject, text)
