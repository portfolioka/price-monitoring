from logging import Formatter, FileHandler, DEBUG, getLogger

formatter = Formatter('[%(levelname)s] %(asctime)s - %(message)s')

handler = FileHandler('') #ログを書き込むファイルのフルパスを''内に記載する
handler.setLevel(DEBUG)
handler.setFormatter(formatter)

logger = getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(handler)