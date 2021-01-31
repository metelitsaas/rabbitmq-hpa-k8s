import logging
import sys

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(FORMATTER)

logger = logging.getLogger("Logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
