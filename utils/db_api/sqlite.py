# import sqlite3
#
# class Database:
#     def __init__(self, path_to_db="main.db"):
#         self.path_to_db = path_to_db
#
#     @property
#     #ma'lumotlar bazasiga ulanish
#     def connection(self):
#         return sqlite3.connect(self.path_to_db)
#
#     #SQL komandalarini ishga tushirish
#     def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
#         if not parameters:
#             parameters = ()
#         connection = self.connection
#         connection.set_trace_callback(logger)
#         cursor = connection.cursor()
#         data = None
#         cursor.execute(sql, parameters)
#
#         if commit:
#             connection.commit()
#         if fetchall:
#             data = cursor.fetchall()
#         if fetchone:
#             data = cursor.fetchone()
#         connection.close()
#
#         return data
#
#     def create_table_users(self):
#         sql = """
#         CREATE TABLE Users (
#             id int NOT NULL,
#             Name varchar(255) NOT NULL,
#             phone varchar(30),
#             PRIMARY KEY (id)
#             );
#             """
#         self.execute(sql, commit=True)
#
#     @staticmethod
#     def format_args(sql, parameters: dict):
#         sql += " AND ".join([
#             f"{item} = ?" for item in parameters
#         ])
#         return sql, tuple(parameters.values())
#
#     def add_user(self, id: int, name: str, phone: str=None):
#         #SQL_EXAMPLE = "INSERT INTO Users(id, Name, phone) VALUES (1,'Aziz', '+99899888888'"
#         sql = """
#         INSERT INTO Users(id, Name, phone) VALUES(?, ?, ?)
#         """
#         self.execute(sql, parameters=(id, name, phone), commit=True)
#
#     def select_all_users(self):
#         sql = """
#         SELECT * FROM Users
#         """
#         return sels.execute(sql, fetchall=True)
#
#     def select_user(self, **kwargs):
#         #SQL_EXAMPLE = "SELECT * FROM Users WHERE id=1 AND NAME='John'"
#         sql = "SELECT * FROM Users WHERE "
#         sql, parameters = self.format_args(sql, kwargs)
#
#         return self.execute(sql, parameters=parameters, fetchone=True)
#
#     def count_user(self, **kwargs):
#         return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)
#
#     def update_user_phone(self, phone, id):
#         #SQL_EXAMPLE = "UPDATE Users SET phone=9898989898 WHERE id=4394"
#         sql = f"""
#         UPDATE Users SET phone = ? WHERE id=?
#         """
#         return self.execute(sql, parameters=(phone, id), commit=True)
#
#     def logger(statement):
#         print(f"""
#     ---------------------------------------
#     Bajarilyabdi...
#     {statement}
#     ---------------------------------------
#     """)
