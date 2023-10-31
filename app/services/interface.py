class InterfaceClientLogic:
    """class db client logic.

    You need to create variables: connect, cursor:

    connect = psycopg2.connect(
        database=db_name,
        user=username,
        password=password,
        host=host,
        port=port
    )

    cursor = connect.cursor()"""

    @classmethod
    async def find_name_by_date(cls, date: str):
        """
        Database Connection,
        make a request,
        returns the result of the query.

        :param date: date which need find
        :return: names of the birthday people, otherwise None
        """
        pass
