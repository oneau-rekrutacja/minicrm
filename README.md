# MiniCRM

Uproszczony CRM ofertowy — Flask + SQLAlchemy + Jinja2, baza SQLite, testy w pytest.
Aplikacja obsługuje klientów, oferty, wyliczanie kwot (rabat, VAT, brutto) i prostą listę
z filtrowaniem oraz paginacją.

Wymagany **Python 3.10 lub nowszy** i **git**. Nic poza tym.

## Uruchomienie

### Linux i macOS

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python seed.py
.venv/bin/python run.py
```

Skrót: `./setup.sh` wykonuje trzy pierwsze kroki naraz.

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python seed.py
.venv\Scripts\python run.py
```

Katalog z plikami wykonywalnymi środowiska nazywa się na Windowsie `Scripts`, a nie `bin` —
to jedyna różnica. Jeśli `py` nie działa, użyj `python`.

Aplikacja startuje na http://localhost:5000. Logowanie jest uproszczone (demo):
na stronie startowej wybierasz użytkownika, bez hasła.

## Testy

```bash
.venv/bin/python -m pytest          # Linux, macOS
.venv\Scripts\python -m pytest      # Windows
```

## Struktura

```
app/__init__.py     — fabryka aplikacji
app/models.py       — modele: User, Client, Offer
app/services.py     — logika wyceny i podsumowań
app/views.py        — widoki (blueprint)
app/templates/      — szablony Jinja2
seed.py             — dane demonstracyjne
setup.sh            — skrót instalacyjny dla Linuksa i macOS
requirements.txt    — zależności (Flask, SQLAlchemy, pytest)
tests/              — testy pytest
oddaj_prace.py      — pakuje pracę do przekazania (patrz niżej)
```

## Dane demonstracyjne

`seed.py` zakłada dwóch użytkowników (Anna Nowak, Marek Zieliński), sześciu klientów
i dwanaście ofert w różnych statusach.

## Przekazanie pracy

Na koniec zadania, z katalogu projektu:

```bash
python oddaj_prace.py "Imię Nazwisko"      # Linux, macOS
py oddaj_prace.py "Imię Nazwisko"          # Windows
```

Skrypt zbiera Twoje pliki, gałęzie i commity do jednego archiwum ZIP w katalogu domowym
i wypisze jego ścieżkę. Zabiera też zmiany, których nie zdążyłeś zacommitować, oraz nowe
pliki nieznane jeszcze gitowi — nic nie przepada. Nie wymaga żadnych bibliotek ani konta
GitHub.

Powstały plik odsyłasz w odpowiedzi na maila, którego dostałeś przed spotkaniem.
