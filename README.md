# MiniCRM

Uproszczony CRM ofertowy — Flask + SQLAlchemy + Jinja2, baza SQLite, testy w pytest.
Aplikacja obsługuje klientów, oferty, wyliczanie kwot (rabat, VAT, brutto) i prostą listę
z filtrowaniem oraz paginacją.

## Uruchomienie

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python seed.py
.venv/bin/python run.py
```

Aplikacja startuje na http://localhost:5000. Logowanie jest uproszczone (demo):
na stronie startowej wybierasz użytkownika, bez hasła.

Skrót: `./setup.sh` robi wszystkie trzy pierwsze kroki naraz.

## Testy

```bash
.venv/bin/python -m pytest
```

## Struktura

```
app/__init__.py     — fabryka aplikacji
app/models.py       — modele: User, Client, Offer
app/services.py     — logika wyceny i podsumowań
app/views.py        — widoki (blueprint)
app/templates/      — szablony Jinja2
seed.py             — dane demonstracyjne
tests/              — testy pytest
```

## Dane demonstracyjne

`seed.py` zakłada dwóch użytkowników (Anna Nowak, Marek Zieliński), sześciu klientów
i dwanaście ofert w różnych statusach.
