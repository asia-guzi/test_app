@echo OFF

:: Tworzenie wirtualnego środowiska, jeśli nie istnieje
IF NOT EXIST "venv" (
    echo Tworzenie wirtualnego środowiska...
    python -m venv venv
)

:: Aktywacja środowiska wirtualnego
call venv\Scripts\activate.bat

:: Instalowanie zależności
pip install -r requirements.txt

:: Uruchamianie skryptu do inicjalizacji bazy danych
:: echo Tworzenie bazy danych i tabeli...
:: python start_project\initial_populate.py

:: Dodawanie wirtualnego środowiska jako kernel Jupyter
echo Rejestrowanie kernela Jupyter...
python -m ipykernel install --user --name=venv --display-name "Quiz (venv)"

:: Uruchamianie Jupyter Notebook
echo Uruchamianie Jupyter Notebook...
jupyter notebook start_project\initiate_project.ipynb

:: Uruchamianie serwera FastAPI
echo Uruchamianie serwera FastAPI...
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause