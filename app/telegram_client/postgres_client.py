import psycopg2

from config import Config

class PostgresClient:
    def __init__(self):
        self.connect = psycopg2.connect(
            database=Config.database,
            user=Config.username,
            password=Config.password,
            host=Config.host,
            port=Config.port)
        self.cursor = self.connect.cursor()


    def get_all(self, date):
        with self.connect:
            self.cursor.execute(
                """
                with all_fields as (
                    select tg_users.user_id, friend_id, tg_id, user_nickname, user_name, language, birth_date, phone_number
                    from tg_users
                    inner join user_relations on tg_users.user_id = user_relations.user_id
                ),
        
                pairs as (
                    select friend_id, user_id
                    from all_fields
                    where birth_date = %s
                ),
        
                table_with_tg_ids as (
                    select tg_id, pairs.user_id
                    from tg_users
                    inner join pairs on tg_users.user_id = pairs.friend_id
                ),
        
                output as (
                    select table_with_tg_ids.tg_id, user_name, phone_number
                    from table_with_tg_ids
                    inner join tg_users on table_with_tg_ids.user_id = tg_users.user_id
                )

                select * from output;
                """,
                (date,)
            )

        data = self.cursor.fetchall()
        return data



















        # out = dict()
        # with self.connect:
        #     self.cursor.execute(
        #         """
        #         select user_id
        #         from tg_users
        #         where birth_date = %s;
        #         """,
        #         (date,)
        #     )
        # res = self.cursor.fetchall()
        # ids_birthday_users = [x[0] for x in res]            # keys
        #
        #
        # for i in ids_birthday_users:
        #     with self.connect:
        #         self.cursor.execute(
        #             """
        #             select user_id
        #             from user_relations
        #             where friend_id = %s
        #             """,
        #             (i, )
        #         )
        #     out[i] = self.cursor.fetchall()
        #
        # print(out)
        #
        # for i in out:
        #     a = []
        #     b = []
        #     for k in out[i]:
        #         with self.connect:
        #             self.cursor.execute(
        #                 """
        #                 select tg_id
        #                 from tg_users
        #                 where user_id = %s;
        #                 """,
        #                 (k[0],)
        #             )
        #         a.append( self.cursor.fetchall() )
        #
        #     for k in out[i]:
        #         with self.connect:
        #             self.cursor.execute(
        #                 """
        #                 select user_name, phone_number, language
        #                 from tg_users
        #                 where user_id = %s;
        #                 """,
        #                 (k[0],)
        #             )
        #         b.append( self.cursor.fetchall() )
        #
        #     out[i] = a
        #
        #
        # print(ids_birthday_users)
        # print(out)
        #
        #
















    # def get_all(self, date):
    #     with self.connect:
    #         self.cursor.execute(
    #             """
    #             select user_id
    #             from tg_users
    #             where birth_date = %s;
    #             """,
    #             (date,)
    #         )
    #     ids_birthday_users = self.cursor.fetchall()
    #
    #     with self.connect:
    #         self.cursor.execute(
    #             """
    #             select user_name, phone_number, language
    #             from tg_users
    #             where birth_date = %s;
    #             """,
    #             (date,)
    #         )
    #     info_birthday_users = self.cursor.fetchall()
    #
    #
    #     print(dict(zip(ids_birthday_users, info_birthday_users)))
    #
    #
    #     # print(ids_birthday_users, info_birthday_users, sep="\n")
    #
    #
    #
    #
    #     # ids = [x[0] for x in ids_birthday_users]
    #     relations = dict()
    #     for i in ids_birthday_users:
    #         with self.connect:
    #             self.cursor.execute(
    #                 """
    #                 select user_id
    #                 from user_relations
    #                 where friend_id = %s;
    #                 """,
    #                 (i,)
    #             )
    #         relations[i] = self.cursor.fetchall()
    #         # relations[i] = [x[0] for x in self.cursor.fetchall()]
    #     print(relations)
    #     tg_ids = dict()
    #     for i in relations:
    #         for k in relations[i]:
    #             with self.connect:
    #                 self.cursor.execute(
    #                     """
    #                     select tg_id
    #                     from tg_users
    #                     where user_id = %s;
    #                     """,
    #                     (k,)
    #                 )
    #             tg_ids[k] = self.cursor.fetchall()
    #     print(tg_ids)







    # def get_today_birthdays(self, today_month, today_day):
    #     with self.connect:
    #         self.cursor.execute(
    #             """
    #             select user_id
    #             from tg_users
    #             where birth_date = %s;
    #             """,
    #             (f"2000-{today_month}-{today_day}",)
    #         )
    #     data = self.cursor.fetchall()
    #     return data
    #
    #
    # # def get

