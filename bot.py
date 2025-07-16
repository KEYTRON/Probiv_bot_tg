import asyncio
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart

# Directory containing search files
DATA_DIR = Path('data')

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Отправьте ФИО для поиска")


def search_files(query: str) -> list[str]:
    """Search for query in .csv and .txt files under DATA_DIR."""
    results = []
    for path in DATA_DIR.rglob('*'):
        if path.suffix.lower() not in {'.csv', '.txt'}:
            continue
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if query.lower() in line.lower():
                        results.append(f"{path}: {line.strip()}")
        except Exception as e:
            print(f"Failed to read {path}: {e}")
    return results


@router.message()
async def search_handler(message: types.Message):
    query = message.text.strip()
    if not query:
        return
    matches = search_files(query)
    if matches:
        await message.answer('\n'.join(matches[:50]))
    else:
        await message.answer('Ничего не найдено')


def main() -> None:
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise RuntimeError('BOT_TOKEN is not set')
    bot = Bot(token)
    dp = Dispatcher()
    dp.include_router(router)
    asyncio.run(dp.start_polling(bot))


if __name__ == '__main__':
    main()
