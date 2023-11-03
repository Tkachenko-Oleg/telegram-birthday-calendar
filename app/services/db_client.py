# import psycopg2
#
#
# class DataBase:
#     def __init__(self):
#         self.connect = psycopg2.connect(
#             database="default_db",
#             user="gen_user",
#             password=".Far-KOSvLS9Nb",
#             host="89.223.64.171",
#             port=5432
#         )
#
#         self.cursor = self.connect.cursor()
#
#
#     def drop_table(self):
#         pass
#
#
#     # def create_table(self):
#     #     try:
#     #         self.cursor.execute(
#     #             """
#     #             CREATE TABLE users (
#     #             id SERIAL PRIMARY KEY,
#     #             username VARCHAR(255) NOT NULL,
#     #             language VARCHAR(10) NOT NULL,
#     #             birthday DATE
#     #             )
#     #             """
#     #         )
#     #
#     #         self.cursor.close()
#     #         self.connect.commit()
#     #     except (Exception, psycopg2.DatabaseError) as error:
#     #         print(error)
#     #     finally:
#     #         if self.connect is not None:
#     #             self.connect.close()
#
#
#     # async def find_name_by_date(self, date: str):
#     #     with cls.connect:
#     #         cls.cursor.execute(f"SELECT name FROM birthdays WHERE date = {date}")
#     #         return cls.cursor.fetchone()
#
# if __name__ == "__main__":
#     db = DataBase()
#     # db.create_table()
#
