import json

from sgmon.http import HTTPClient
from sgmon.log import get_logger
from sgmon.task import TaskManager

logger = get_logger(__name__)


class Insights(object):
    def __init__(self, url, key, event_type):
        self.url = url
        self.key = key
        self.event_type = event_type

    def push_event(self, task):
        if task.get("pushed"):
            return True

        headers = {
            "X-Insert-Key": self.key,
            "Content-Type": "application/json",
        }

        payload = {
            "eventType": self.event_type,
            "timestamp": str(task["updatedAt"]),
            "version": 1,
        }
        manager = TaskManager()

        for k in task["taskId"]:
            payload[k] = task["taskId"][k]
        for k in ["updatedAt", "lastTaskState"]:
            payload[k] = str(task[k])

        logger.debug("Task data: {0}".format(json.dumps(payload, indent=4)))

        client = HTTPClient(self.url)
        client.set_headers(headers)
        resp = client.post(json.dumps(payload))
        logger.info("Post response: {0}".format(resp))

        logger.debug("Task '{0}' pushed".format(payload["id"]))

        manager.remove_task(task)

        return True

    def push_events(self, tasks):
        if len(tasks) == 1 and isinstance(tasks[0], dict):
            task = tasks[0]
            return self.push_event(task)

        headers = {
            "X-Insert-Key": self.key,
            "Content-Type": "application/json",
        }

        logger.debug("Number of tasks to post: {0}".format(len(tasks)))

        payloads = []
        manager = TaskManager()

        for task in tasks:
            payload = {
                "eventType": self.event_type,
                "timestamp": str(task["updatedAt"]),
                "version": 1,
            }
            for k in task["taskId"]:
                payload[k] = task["taskId"][k]
            for k in ["updatedAt", "lastTaskState"]:
                payload[k] = str(task[k])
            payloads.append(payload)
            manager.remove_task(task)

        client = HTTPClient(self.url)
        client.set_headers(headers)
        resp = client.post(json.dumps(payloads))
        logger.info("Post batch response: {0}".format(resp))

        return True
