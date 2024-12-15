import json
import requests
from requests import Response
from typing import TypedDict
from datetime import datetime

class Task(TypedDict):
    id: int
    user: int
    title: str
    finished: bool
    created_at: str
    due: str | None
    repeat: int | None
    in_group: int | None
    note: str | None

def is_task_overdue(task: Task) -> bool:
    if task["due"] == None:
        return False
    
    date = datetime.strptime(task["due"], "%Y/%m/%d %H:%M:%S")
    return datetime.now().timestamp() - date.timestamp() > 0

class Client:
    api_url = "https://kairo.dawn.rest/api"
    token = "Bearer Guest"

    task_cache: list[Task] | None = None

    # HTTP Functions

    def get(self, url: str) -> Response:
        return requests.get(url=(self.api_url + url), headers={"Authorization": self.token})

    def fetch_tasks(self) -> list[Task]:
        result = [Task(**task_data) for task_data in json.loads(self.get(url="/tasks").content)]
        self.task_cache = result
        return result
    
    # Util functions

    def get_overdue(self) -> list[Task]:
        if self.task_cache == None:
            return []
        
        return [
            task 
            for task in self.task_cache 
            if task["due"] != None and is_task_overdue(task)
        ] 
    
CLIENT = Client()