from aiomysql import Pool

from app.config import settings


async def create_new_user(login: str, name: str, pool: Pool) -> int:
    async with pool.acquire() as connection:
        cursor = await connection.cursor()
        try:
            await cursor.execute(
                "INSERT INTO logins (login, pwdmethod, password) VALUES (%s, %s, %s)",
                (login, 0, settings.database.common_ejudge_password),
            )
            await connection.commit()
        except Exception as e:
            pass

        await cursor.execute("SELECT user_id FROM logins WHERE login = %s", (login,))
        user_id = (await cursor.fetchone())[0]

        try:
            await cursor.execute(
                "INSERT INTO cntsregs (user_id, contest_id) VALUES (%s, %s)",
                (user_id, settings.database.default_contest_id),
            )
            await connection.commit()
        except Exception as err:
            pass

        try:
            await cursor.execute(
                "INSERT INTO users (user_id, contest_id, username) VALUES (%s, %s, %s)",
                (user_id, settings.database.default_contest_id, name),
            )
            await connection.commit()
        except Exception as err:
            pass

    return user_id
