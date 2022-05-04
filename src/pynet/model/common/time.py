from datetime import datetime

today = lambda: datetime.now().strftime("%Y.%m.%d")
now = lambda: datetime.now().strftime("%H:%M:%S.%f")
now_lite = lambda: datetime.now().strftime("%H:%M")
