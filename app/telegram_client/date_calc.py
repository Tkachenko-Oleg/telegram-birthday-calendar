import datetime


class Date:
    @staticmethod
    def get_today_date():
        return datetime.date.today().month, datetime.date.today().day


    # @staticmethod
    # def get_today_date():

