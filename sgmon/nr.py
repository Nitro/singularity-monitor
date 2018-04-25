import os
import logging
import newrelic.agent as agent

from sgmon.log import get_logger

logger = get_logger(__name__)


def init_newrelic_agent():
    try:
        _ = os.environ["NEW_RELIC_LICENSE_KEY"]
    except KeyError:
        logger.info("Agent will not report data to New Relic APM")
    else:
        config_file = os.environ.get("NEW_RELIC_CONFIG_FILE")
        env = os.environ.get("NEW_RELIC_ENVIRONMENT")
        log_file = "stdout"
        log_level = logging.DEBUG
        agent.initialize(config_file, env, log_file, log_level)
        logger.info("Agent start reporting data to New Relic APM")
