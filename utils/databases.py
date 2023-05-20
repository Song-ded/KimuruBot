import aiosqlite
import disnake


class UsersDataBase:
    def __init__(self):
        self.name = 'dbs/users.db'
        self.name2 = 'dbs/messages.db'

    async def create_table(self):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                money INTEGER,
                premium FLOAT
            )'''
            await cursor.execute(query)
            await db.commit()

    async def create_table2(self):
        async with aiosqlite.connect(self.name2) as db:
            cursor = await db.cursor()
            query = '''CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                messagess INTEGER
            )'''
            await cursor.execute(query)
            await db.commit()

    async def get_user(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM users WHERE id = ?'
            await cursor.execute(query, (user.id,))
            return await cursor.fetchone()

    async def get_stats(self, user: disnake.Member):
        async with aiosqlite.connect(self.name2) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM messages WHERE id = ?'
            await cursor.execute(query, (user.id,))
            return await cursor.fetchone()

    async def add_user(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            if not await self.get_user(user):
                cursor = await db.cursor()
                query = 'INSERT INTO users (id, money, premium) VALUES (?, ?, ?)'
                await cursor.execute(query, (user.id, 0, 0))
                await db.commit()

    async def add_ustats(self, user: disnake.Member):
        async with aiosqlite.connect(self.name2) as db:
            if not await self.get_stats(user):
                cursor = await db.cursor()
                query = 'INSERT INTO messages (id, messagess) VALUES (?, ?)'
                await cursor.execute(query, (user.id, 0))
                await db.commit()

    async def update_money(self, user: disnake.Member, money: int, premium: float):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'UPDATE users SET money = money + ?, premium = premium + ? WHERE id = ?'
            await cursor.execute(query, (money, premium, user.id))
            await db.commit()

    async def update_stats(self, user: disnake.Member, messagess: int):
        async with aiosqlite.connect(self.name2) as db:
            cursor = await db.cursor()
            query = 'UPDATE messages SET messagess = messagess + ? WHERE id = ?'
            await cursor.execute(query, (messagess, user.id))
            await db.commit()
    async def get_top(self):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM users ORDER BY money DESC'
            await cursor.execute(query)
            return await cursor.fetchall()
