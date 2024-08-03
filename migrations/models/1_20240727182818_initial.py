from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "first_name" VARCHAR(150) NOT NULL,
    "last_name" VARCHAR(150) NOT NULL,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "password" VARCHAR(100) NOT NULL,
    "passport_series" VARCHAR(4) NOT NULL,
    "passport_number" VARCHAR(6) NOT NULL
);
COMMENT ON COLUMN "user"."id" IS 'Первичный ключ';
COMMENT ON COLUMN "user"."first_name" IS 'Имя';
COMMENT ON COLUMN "user"."last_name" IS 'Фамилия';
COMMENT ON COLUMN "user"."email" IS 'Электронная почта';
COMMENT ON COLUMN "user"."password" IS 'Пароль';
COMMENT ON COLUMN "user"."passport_series" IS 'Серия паспорта';
COMMENT ON COLUMN "user"."passport_number" IS 'Номер паспорта';
COMMENT ON TABLE "user" IS 'Модель для пользователя ';
CREATE TABLE IF NOT EXISTS "wallet" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "number" VARCHAR(19) NOT NULL UNIQUE,
    "balance" DECIMAL(10,2) NOT NULL  DEFAULT 0,
    "currency" VARCHAR(3) NOT NULL,
    "wallet_type" VARCHAR(20) NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "wallet"."id" IS 'Первичный ключ';
COMMENT ON COLUMN "wallet"."number" IS 'Номер';
COMMENT ON COLUMN "wallet"."balance" IS 'Баланс';
COMMENT ON COLUMN "wallet"."currency" IS 'Валюта';
COMMENT ON COLUMN "wallet"."wallet_type" IS 'Тип кошелька';
COMMENT ON TABLE "wallet" IS 'Модель для кошелька ';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
