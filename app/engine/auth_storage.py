import secrets
from datetime import datetime, timezone
from typing import Optional

from pymongo import ReturnDocument
from pymongo.collection import Collection

from app.config import settings

COOKIE_TTL = settings.auth.cookie_ttl
SESSION_COOKIE_NAME = settings.auth.session_cookie_name

UPDATE_AT_FIELD = "update_at"


def gen_secret() -> str:
    return secrets.token_urlsafe(32)


class AuthStorage:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection
        self.collection.create_index(UPDATE_AT_FIELD, expireAfterSeconds=COOKIE_TTL)

    def check_cookie(self, cookie: Optional[str]) -> Optional[str]:
        if cookie is None:
            return None
        result = self.collection.find_one_and_update(
            {"_id": cookie},
            {"$set": {UPDATE_AT_FIELD: datetime.now(timezone.utc)}},
            return_document=ReturnDocument.AFTER,
        )
        if result is None:
            return None
        return result["login"]

    def pop_cookie(self, cookie: str):
        self.collection.delete_one({"_id": cookie})

    def new_cookie(self, login: str) -> str:
        cookie = gen_secret()
        self.collection.insert_one(
            {
                "_id": cookie,
                "login": login,
                UPDATE_AT_FIELD: datetime.now(timezone.utc),
            }
        )
        return cookie
