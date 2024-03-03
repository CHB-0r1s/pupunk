"""
pip install -r requirements.txt
python main.py
"""

import logging
from dubbler import Dubbler, FatFingerNotFound
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        token = os.environ["TOKEN"]
    except KeyError:
        logger.warning(
            "Token wasn't provided to the application.\n Run like TOKEN=azaza python main.py"
        )
        exit(1)

    dubler = Dubbler(token)

    while True:
        try:
            dubler.poll()
        except FatFingerNotFound as e:
            logger.debug(e.arg[0])
