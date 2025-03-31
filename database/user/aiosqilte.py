import aiosqlite


class DatabaseUser:
    def __init__(self, path_to_db="user.db"):
        self.path_to_db = path_to_db

    async def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        async with aiosqlite.connect(self.path_to_db) as connection:
            cursor = await connection.execute(sql, parameters)
            data = None

            if commit:
                await connection.commit()
            if fetchall:
                data = await cursor.fetchall()
            if fetchone:
                data = await cursor.fetchone()
            await cursor.close()
        return data

    async def create_table_user(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER UNIQUE,
            ActiveUsername TEXT,
            FirstName TEXT,
            LastName TEXT,
            BirthDate TEXT,
            BirthDateType TEXT,
            HasPrivateForwards INTEGER,
            LanguageCode TEXT,
            UserStartDate TEXT,
            Status TEXT,
            Premium INTEGER,       
            PersonalChatUsername TEXT,
            Referal TEXT
        );
        """
        await self.execute(sql, commit=True)

    async def add_user(self, user_id: int, active_username: str, first_name: str, last_name: str,
                       birth_date: str, birth_date_type, has_private_forwards: str, language_code: str, user_start_date: str,
                       status: str, premium: str, personal_chat_username: str, referal: str):
        sql = """
        INSERT INTO Users(UserID, ActiveUsername, FirstName, LastName, BirthDate, BirthDateType,
        HasPrivateForwards, LanguageCode, UserStartDate, Status, Premium,
        PersonalChatUsername, Referal)
         VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        await self.execute(sql,
                           parameters=(user_id, active_username, first_name, last_name, birth_date, birth_date_type,
                                       has_private_forwards, language_code, user_start_date,
                                       status, premium,
                                       personal_chat_username, referal),
                           commit=True)

    async def update_user_status(self, status, user_id):
        sql = "UPDATE Users SET Status=? WHERE UserID=?"
        await self.execute(sql=sql, parameters=(status, user_id), commit=True)

    async def return_status_member_users_id(self):
        sql = "SELECT UserID FROM Users WHERE Status='MEMBER'"
        return await self.execute(sql=sql, fetchall=True)

    async def return_kicked_status_users_count(self):
        sql = "SELECT COUNT(*) FROM Users WHERE Status='KICKED'"
        return await self.execute(sql=sql, fetchone=True)

    async def return_status_member_premium_users(self):
        sql = "SELECT UserID FROM Users WHERE Status='MEMBER' AND Premium = 1"
        return await self.execute(sql=sql, fetchall=True)

    async def return_user(self, user_id):
        sql = "SELECT * FROM Users WHERE UserId = ?"
        return await self.execute(sql=sql, parameters=(user_id,), fetchone=True)

    async def return_status_kicked_premium_users(self):
        sql = "SELECT UserID FROM Users WHERE Status='KICKED' AND Premium = 1"
        return await self.execute(sql=sql, fetchall=True)

    async def return_status_member_count(self):
        sql = "SELECT COUNT(*) FROM Users WHERE Status='MEMBER'"
        return await self.execute(sql=sql, fetchone=True)

    async def return_status_member_premium_count(self):
        sql = "SELECT COUNT(*) FROM Users WHERE Premium = 1"
        return await self.execute(sql=sql, fetchone=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetchall=True)

    async def count_users(self):
        return await self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    async def delete_block_user(self):
        query = f"DELETE FROM Users WHERE Status = 'KICKED'"
        await self.execute(sql=query, commit=True)

    async def return_last_ten(self):
        query = 'SELECT * FROM Users ORDER BY ROWID DESC LIMIT 10;'
        return await self.execute(sql=query, fetchall=True)
