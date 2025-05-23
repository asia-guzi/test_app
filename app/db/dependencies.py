# app/dependencies.py
from .config import async_session
from sqlalchemy.ext.asyncio import AsyncSession

# Zależność zarządzająca sesją SQLAlchemy ORM
'''For example, you could use this to create a database session and close it after finishing.

Only the code prior to and including the yield statement is executed before creating a response:'''
async def get_session() -> AsyncSession:
    # session = async_session()
    # try: #try to catch eg. rollback
    #     yield session  # Udostępnienie sesji
    # finally:
    #     await session.close()  # Zamknięcie sesji po zakończeniu


        async with async_session() as session:
            yield session

"""
2. Główna różnica między nimi
Główna różnica dotyczy zakresu odpowiedzialności za zarządzanie zasobami:

try-finally:

Wymaga od Ciebie ręcznego utworzenia sesji i jej zamknięcia.
Jesteś odpowiedzialny za upewnienie się, że sesja zostanie zamknięta w bloku finally.
Większe ryzyko błędów, np. możesz zapomnieć dodać await session.close() w bloku finally.
async with:

Automatyzuje obsługę zasobu (sesji). To obiekt sesji SQLAlchemy (lub inny zasób) implementuje tę logikę w swoim __aexit__.
Uproszczona składnia zmniejsza ryzyko błędów.
Python wywołuje __aexit__, które automatycznie zamknie sesję.


Cechy	try-finally	async with
Tworzenie sesji	Ręczne	Automatyczne (__aenter__)
Zamykanie w przypadku wyjątku	Musisz ręcznie dodać finally: await session.close()	Automatyczne (__aexit__)
Czytelność kodu	Mniej czytelny, więcej kodu	Bardziej elegancki i Pythoniczny
Ryzyko błędów (np. brak zamknięcia)	Większe ryzyko	Mniejsze ryzyko, zamknięcie jest wymuszone
Użycie w SQLAlchemy	Możesz użyć, ale wymaga ręcznego zarządzania	Zalecana metoda, SQLAlchemy natywnie wspiera async with
"""