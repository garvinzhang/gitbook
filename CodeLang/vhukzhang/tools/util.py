from datetime import datetime, date, timedelta


class Util(object):
    def GetNowtime(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def GetDate(self, backDay: int = 0) -> str:
        return (date.today() - timedelta(backDay)).strftime("%Y-%m-%d")

    def GetDs(self, backDay: int = 0) -> int:
        return int((date.today() - timedelta(backDay)).strftime("%Y%m%d"))


UTIL = Util()
