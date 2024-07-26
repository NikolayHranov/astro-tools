import logging


logger = logging.getLogger(__name__)

streamH = logging.StreamHandler()
streamH.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s: %(name)s: %(levelname)s:  %(message)s")
streamH.setFormatter(formatter)
logger.addHandler(streamH)



logger.info("Hello from Nikolay Hranov!")