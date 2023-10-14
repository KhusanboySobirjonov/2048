import sqlite3  # sqlite serverini ishlatish

# Database sinfini yaratish
class Database:
    # Ma'lumotlar bazasini yaratish
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    # Ma'lumotlar bazasiga bog'lanish
    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    # Sql kommandalarni ishga tushirish
    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    # scores jadvalini yaratish
    def create_table_scores(self):
        sql = """
            CREATE TABLE scores (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Score INT NOT NULL,
                Created_at DATETIME NOT NULL
            );
        """
        self.execute(sql, commit=True)

    # Bir qancha o'zgaruvchilar bilan ishlash
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    # scores jadvaliga natija qo'shish
    def add_score(self, Score: int, Created_at: str = None):
        sql = """
        INSERT INTO scores(Score, Created_at) VALUES(?, ?);
        """
        self.execute(sql, parameters=(Score, Created_at), commit=True)

    # scores jadvalini olish
    def select_all_scores(self):
        sql = f"SELECT * FROM scores;"
        return self.execute(sql, fetchall=True)

    # scores jadvalidan bitta natija ma'lumotini olish
    def select_score(self, **kwargs):
        sql = "SELECT * FROM scores WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    # scores jadavalidagi natijalar sonini olish
    def count_scores(self):
        return self.execute("SELECT COUNT(*) FROM scores;", fetchone=True)

# Bajariluvchi sql kommandalari haqida xabarni ko'rsatadi
def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")