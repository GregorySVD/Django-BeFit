# BeFit2 Django – Projekt na laboratoria z Programowania Zaawansowanego

BeFit2 Django to aplikacja webowa stworzona w ramach laboratoriów z przedmiotu *Programowanie zaawansowane*.  
Umożliwia rejestrowanie sesji treningowych, dodawanie wykonanych ćwiczeń oraz przeglądanie statystyk użytkownika.

## Funkcjonalności

- Rejestracja i logowanie użytkowników (Django Auth)
- Tworzenie, edycja i usuwanie sesji treningowych
- Dodawanie wykonanych ćwiczeń (serie, powtórzenia, obciążenie)
- Automatyczne przypisywanie danych do zalogowanego użytkownika
- Walidacja formularzy i danych wejściowych
- Publiczna lista typów ćwiczeń
- Zarządzanie typami ćwiczeń dostępne tylko dla Administratora (is_staff)
- Statystyki użytkownika z ostatnich 28 dni
- Pełna ochrona dostępu (LoginRequired, StaffRequired)

## Modele

- **ExerciseType** – typ ćwiczenia  
- **TrainingSession** – sesja treningowa użytkownika  
- **SessionExercise** – wykonane ćwiczenie w ramach sesji  

## Technologie

- Python 3.12  
- Django 5  
- Django Authentication & Permission System  
- SQLite  
- Bootstrap 5  
- HTML + Django Templates  

## Instalacja i uruchomienie

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/GregorySVD/Django-BeFit.git
   cd Django-BeFit
   ```
2. Utwórz i aktywuj wirtualne środowisko:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
      ```
4. Wykonaj migracje:
   ```bash
   python manage.py migrate
      ```
5. Uruchom serwer:
   ```bash
   python manage.py runserver
      ```
## Tworzenie użytkownika administratora
Po instalacji możesz utworzyć konto administratora:
   ```bash
python manage.py createsuperuser
   ```

   # Autor 
- [@GTerenda](https://github.com/GregorySVD)
