import json

import aiohttp
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials
from loguru import logger

from app.config import settings


async def send_email(to_address: str, login: str, password: str):
    logger.info("Sending email...)")

    if (
        len(settings.email.secret_key) == 0
        or len(settings.email.access_key) == 0
    ):
        logger.info(f"Skipped sending email -> {to_address} {login}:{password}")
        return

    data = {
        "FromEmailAddress": settings.email.from_email,
        "Destination": {"ToAddresses": [to_address]},
        "Content": {
            "Simple": {
                "Subject": {"Data": settings.email.email_subject},
                "Body": {
                    "Text": {
                        "Data": settings.email.email_body_template.format(
                            site_url=settings.email.site_url,
                            login=login,
                            password=password,
                        )
                    }
                },
            }
        },
    }
    creds = Credentials(settings.email.access_key, settings.email.secret_key)

    try:
        request = AWSRequest(
            method="POST",
            url=settings.email.yandex_postbox_url,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        SigV4Auth(creds, "ses", settings.email.yandex_region).add_auth(request)

        async with aiohttp.ClientSession() as s:
            async with s.post(
                request.url, data=request.body, headers=dict(request.headers)
            ) as r:
                logger.info(await r.text())
    except Exception as e:
        pass
