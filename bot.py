import os
import asyncio
import csv
import io
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN", "8108367367:AAGgZXVaS0lVbacNjzcnVxoO1XddDSijD3M")
# Google Sheets источники данных
TENANTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTJMucwthLrL_6GLDUUMBJymZEsqZ79nAjQ1eAW7oPU53RYFyh1ocl2Xl0SqUKjBWNaVQ0TlaJqRHRz/pub?gid=2073630276&single=true&output=csv"
PAYMENTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTJMucwthLrL_6GLDUUMBJymZEsqZ79nAjQ1eAW7oPU53RYFyh1ocl2Xl0SqUKjBWNaVQ0TlaJqRHRz/pub?gid=84433962&single=true&output=csv"


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def _format_decimal(value: Decimal | None) -> str:
    if value is None:
        return "—"
    # Отображаем целые значения без копеек, десятичные - с двумя знаками
    quantized = (
        value.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        if value == value.to_integral()
        else value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    )
    parts = f"{quantized:,}".replace(",", " ")
    return parts


def _safe_get(row: dict, key: str) -> str:
    value = row.get(key, "") if row else ""
    value = value.strip()
    return value or "—"


async def _fetch_csv(session: aiohttp.ClientSession, url: str) -> list[dict]:
    async with session.get(url, timeout=10) as response:
        response.raise_for_status()
        text = await response.text()
    reader = csv.DictReader(io.StringIO(text))
    return list(reader)


def _sum_amounts(rows: list[dict]) -> Decimal:
    total = Decimal("0")
    for row in rows:
        raw_amount = row.get("amount", "").replace(" ", "")
        if not raw_amount:
            continue
        try:
            amount = Decimal(raw_amount)
        except InvalidOperation:
            continue
        total += amount
    return total


def _filter_by_username(rows: list[dict], username: str) -> list[dict]:
    username = (username or "").strip().lower()
    return [row for row in rows if row.get("username", "").strip().lower() == username]


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    username = message.from_user.username if message.from_user else None
    if not username:
        await message.answer("Не удалось найти твои данные в таблице.")
        return

    async with aiohttp.ClientSession() as session:
        tenants_rows, payments_rows = await asyncio.gather(
            _fetch_csv(session, TENANTS_URL),
            _fetch_csv(session, PAYMENTS_URL),
        )

    user_tenants = _filter_by_username(tenants_rows, username)
    user_payments = _filter_by_username(payments_rows, username)

    if not user_tenants and not user_payments:
        await message.answer("Не удалось найти твои данные в таблице.")
        return

    tenant = user_tenants[0] if user_tenants else {}
    total_income = _sum_amounts(user_payments)

    name = _safe_get(tenant, "name")
    monthly_rent_raw = _safe_get(tenant, "monthly_rent")
    deposit_raw = _safe_get(tenant, "deposit")
    pets = _safe_get(tenant, "pets")
    pdf_link = _safe_get(tenant, "pdf_link")
    photos_link = _safe_get(tenant, "photos_links")

    def _parse_decimal(raw: str) -> Decimal | None:
        if raw == "—":
            return None
        normalized = raw.replace(" ", "")
        try:
            return Decimal(normalized)
        except InvalidOperation:
            return None

    monthly_rent_value = _parse_decimal(monthly_rent_raw)
    deposit_value = _parse_decimal(deposit_raw)

    total_income_formatted = _format_decimal(total_income)
    monthly_rent_formatted = _format_decimal(monthly_rent_value)
    deposit_formatted = _format_decimal(deposit_value)

    message_lines = [
        f"Ваш доход: {total_income_formatted} GEL",
        f"Имя: {name}",
        f"Сумма аренды: {monthly_rent_formatted}",
        f"Депозит: {deposit_formatted}",
        f"Животные: {pets}",
        "📄 [Договор]({})".format(pdf_link) if pdf_link != "—" else "📄 Договор: —",
        "📷 [Фото квартиры]({})".format(photos_link) if photos_link != "—" else "📷 Фото квартиры: —",
    ]

    await message.answer("\n".join(message_lines), disable_web_page_preview=True)


async def main():
    await dp.start_polling(bot)


async def start_bot():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
