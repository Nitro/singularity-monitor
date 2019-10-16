import datetime
import os
import sys
import time
import itertools
import threading

from sgmon.event import Insights
from sgmon.http import HTTPClient
from sgmon.log import get_logger
from sgmon.task import TaskManager
from sgmon.utils import env_lookup
from sgmon.nr import agent, init_newrelic_agent
from sgmon import health

logger = get_logger(__name__)

DEBUG = False
if DEBUG:
    import http.client
    http.client.HTTPConnection.debuglevel = 1

TASK_STATES = [
    "TASK_ERROR",
    "TASK_FAILED",
    "TASK_KILLED",
    "TASK_LOST",
]

SINGULARITY_URL = env_lookup("SINGULARITY_URL", "Singularity URL")
TASK_ENDPOINT = SINGULARITY_URL
TASK_API = "/api/history/tasks?lastTaskStatus={state}"
TASK_URL = TASK_ENDPOINT + TASK_API
PERIOD = os.environ.get("PERIOD", 60)
NEWRELIC_ACCOUNT = env_lookup("NEWRELIC_ACCOUNT_ID", "New Relic account id")
NEWRELIC_API = "/v1/accounts/{}/events".format(NEWRELIC_ACCOUNT)
NEWRELIC_INSIGHTS_KEY = env_lookup("NEWRELIC_INSIGHTS_KEY",
                                   "New Relic Insights api key")
NEWRELIC_ENDPOINT = "https://insights-collector.newrelic.com"
EVENT_TYPE = "SingularityTaskEvent"
NEWRELIC_URL = NEWRELIC_ENDPOINT + NEWRELIC_API


def fetch_tasks_state(url, state):
    application = agent.application()
    name = "fetch-{0}".format(state.lower().replace("_", "-"))
    with agent.BackgroundTask(application, name=name, group="Task"):
        try:
            url = url.format(state=state)
            client = HTTPClient(url)
            logger.debug("Fetching tasks state from {}".format(url))
            return client.get()
        except Exception as err:
            logger.exception("Exception when fetching tasks: {}".format(err))
            return []


def sorted_updated(json):
    try:
        return int(json["updatedAt"])
    except KeyError:
        return 0


@agent.background_task(name="mainloop", group="Task")
def loop_forever():
    insights = Insights(NEWRELIC_URL, NEWRELIC_INSIGHTS_KEY, EVENT_TYPE)
    manager = TaskManager()
    while True:
        now = int(datetime.datetime.utcnow().strftime("%s"))
        period = int(PERIOD)
        url = TASK_URL + "&updatedAfter={0}".format(now - period)

        tasks_events = []

        for state in TASK_STATES:
            tasks_events.append(fetch_tasks_state(url, state))

        tasks_events = itertools.chain.from_iterable(tasks_events)

        for task in sorted(tasks_events, key=sorted_updated):
            if task["updatedAt"] > now - period:
                if task not in manager.get_tasks():
                    task["pushed"] = False
                    manager.add_task(task)

        application = agent.application()
        with agent.BackgroundTask(application, name="insights-push",
                                  group="Task"):
            tasks_to_push = manager.get_tasks()
            insights.push_events(tasks_to_push)

        logger.info("Processed {0} tasks".format(len(tasks_to_push)))
        time.sleep(period)


def main():
    init_newrelic_agent()
    try:
        server_thread = threading.Thread(target=health.serve_forever,
                                         name="server")
        server_thread.start()
        loop_forever()
    except KeyboardInterrupt:
        sys.exit(1)

    return 0


if __name__ == "__main__":
    sys.exit(main())
