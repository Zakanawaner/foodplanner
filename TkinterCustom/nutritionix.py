import json
import requests
from BD.dataBaser import DataBaser
from TopSecret.Shhh import NutUrl, NutAppId, NutAppKey, NutUserId


class EchoMaker:
    def __init__(self):
        self.Url = NutUrl
        self.AppId = NutAppId
        self.AppKey = NutAppKey
        self.UserId = NutUserId
        self.dataBaser = DataBaser()

    def natural_nutrients(self, food):
        url = self.Url + "natural/nutrients"
        headers = {"Accept": "application/json",
                   "x-app-id": self.AppId,
                   "x-app-key": self.AppKey,
                   "x-remote-user-id": self.UserId,
                   "Content-Type": "application/json"}
        response = json.loads(requests.post(url, headers=headers, data=json.dumps({"query": food})).content)
        self.dataBaser.save_food(response['foods'], 100)
