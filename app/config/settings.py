"""Centralized application settings.

All hardcoded values should be moved here and optionally configured via environment variables.
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DatabaseSettings:
    """Database connection settings."""

    # MongoDB
    mongo_uri: str = field(default_factory=lambda: os.environ["MONGO_URI"])
    app_name: str = field(default_factory=lambda: os.environ["APP_NAME"])

    # MySQL (Ejudge)
    mysql_host: str = "localhost"
    mysql_db: str = "ejudge"
    mysql_user: str = field(default_factory=lambda: os.environ["EJUDGE_USER"])
    mysql_password: str = field(default_factory=lambda: os.environ["EJUDGE_PASSWORD"])

    # Common ejudge password for new users
    common_ejudge_password: str = field(
        default_factory=lambda: os.environ["COMMON_EJUDGE_PASSWORD"]
    )

    # Default contest ID for registration
    default_contest_id: int = 999999


@dataclass
class ConfigRepoSettings:
    """Settings for configuration repository."""

    repo_name: str = "t-edu-config"
    main_branch: str = "main"
    repo_full_path: str = field(
        default_factory=lambda: f"git@github.com:DimaTomsk/t-edu-config.git"
    )
    configs_path: str = "configs"


@dataclass
class EmailSettings:
    """Email sending settings."""

    access_key: str = field(default_factory=lambda: os.environ["EMAIL_ACCESS_KEY"])
    secret_key: str = field(default_factory=lambda: os.environ["EMAIL_SECRET_KEY"])
    from_email: str = "info@t-edu.tech"
    yandex_postbox_url: str = "https://postbox.cloud.yandex.net/v2/email/outbound-emails"
    yandex_region: str = "ru-central1"
    email_subject: str = "Логин для входа"
    email_body_template: str = (
        "Привет! Данные для входа в {site_url}\n"
        "Логин: {login}\n"
        "Пароль: {password}\n"
    )
    site_url: str = "https://algocourses.ru"


@dataclass
class AuthSettings:
    """Authentication settings."""

    cookie_ttl: int = 60 * 60 * 24  # 24 hours in seconds
    session_cookie_name: str = "session_id"
    smartcaptcha_server_key: str = field(
        default_factory=lambda: os.environ["SMARTCAPTCHA_SERVER_KEY"]
    )
    admin_secret: str = field(default_factory=lambda: os.environ["ADMIN_SECRET"])


@dataclass
class UrlSettings:
    """URL and domain settings."""

    # Main domains
    main_domain: str = "https://algocourses.ru"
    api_domain: str = "https://t-edu.tech"
    local_domain: str = "http://127.0.0.1:8000"

    # Ejudge redirect URL
    ejudge_redirect_base: str = "https://ej-3.t-edu.tech/ejudge/redirect"

    # Video platforms for parsing
    vkvideo_domain: str = "vkvideo.ru"
    youtube_short_domain: str = "youtu.be"


@dataclass
class UISettings:
    """UI settings."""

    version: str = "21"


@dataclass
class StaticFilesSettings:
    """Static files mount settings."""

    styles_mount: str = "/styles"
    styles_directory: str = "resources/styles"
    scripts_mount: str = "/scripts"
    scripts_directory: str = "resources/scripts"
    images_mount: str = "/images"
    images_subdir: str = "teachers"
    files_mount: str = "/files"
    files_subdir: str = "files"


@dataclass
class UserSettings:
    """User-related settings."""

    login_prefix: str = "t-gen"
    login_max_length: int = 300
    login_min_length: int = 1
    value_max_length: int = 300


@dataclass
class Settings:
    """Main settings container."""

    database: DatabaseSettings = field(default_factory=DatabaseSettings)
    config_repo: ConfigRepoSettings = field(default_factory=ConfigRepoSettings)
    email: EmailSettings = field(default_factory=EmailSettings)
    auth: AuthSettings = field(default_factory=AuthSettings)
    urls: UrlSettings = field(default_factory=UrlSettings)
    ui: UISettings = field(default_factory=UISettings)
    static_files: StaticFilesSettings = field(default_factory=StaticFilesSettings)
    user: UserSettings = field(default_factory=UserSettings)


# Global settings instance
settings = Settings()
