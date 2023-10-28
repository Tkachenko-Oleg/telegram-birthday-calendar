class InterfaceCommandLogic:
    """class bot command logic"""
    @classmethod
    def get_all_birthdays(cls, db: dict, user_id: str) -> str:
        """
        Get all birthdays from database

        :param user_id: user id from telegram
        :param db: database with all birthdays
        :return: string with all birthdays
        """
        pass

    @classmethod
    def get_today_birthdays(cls, db: dict, user_id: str) -> str:
        """
        Get all birthdays whose date is equal to today's date

        :param user_id: user id from telegram
        :param db: database with all birthdays
        :return: string with all birthdays whose date is equal to today's date
        """
        pass

    @classmethod
    def add_new_birthday(cls, db: dict, data: dict, user_id: str) -> None:
        """
        Add a new birthday to the database

        :param user_id: user id from telegram
        :param db: database with birthdays
        :param data: dictionary with username, year, month, day to add to the database
        :return: None
        """
        pass

    @classmethod
    def check_correct_data(cls,
                           year: str = '0001',
                           month: str = '01',
                           day: str = '01') -> bool:
        """
        Checking the date for correctness

        :param year: entered year
        :param month: entered month
        :param day: entered day
        :return: if date is correct return True else False
        """
        pass
