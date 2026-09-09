"""Wypełnia bazę danymi demonstracyjnymi. Uruchom: python seed.py"""

from datetime import datetime, timedelta, timezone

from app import create_app, db
from app.models import Client, Offer, User

CLIENTS = [
    ("Zakład Stolarski Kowalski", "Poznań", "biuro@stolarnia-kowalski.pl"),
    ("Piekarnia Złoty Kłos sp. z o.o.", "Wrocław", "kontakt@zlotyklos.pl"),
    ("Gospodarstwo Ogrodnicze Wiśniewscy", "Kalisz", "wisniewscy@example.com"),
    ("Hurtownia Elektryczna VOLT", "Łódź", "zamowienia@volt-hurt.pl"),
    ("Serwis Samochodowy Turbo", "Gdynia", "warsztat@turbo-serwis.pl"),
    ('Biuro Rachunkowe "Saldo"<script>alert(1)</script>', "Kraków", "saldo@example.com"),
]

USERS = [("Anna Nowak", "handlowiec"), ("Marek Zieliński", "handlowiec")]

OFFERS = [
    # (numer, status, netto, rabat %, owner_idx, client_idx, dni_temu)
    ("OF-2026-001", "zaakceptowana", 12500.00, 0, 0, 0, 40),
    ("OF-2026-002", "wyslana", 8400.00, 10, 0, 1, 35),
    ("OF-2026-003", "szkic", 21000.00, 0, 0, 2, 30),
    ("OF-2026-004", "odrzucona", 4300.00, 5, 0, 3, 28),
    ("OF-2026-005", "wyslana", 15750.00, 15, 0, 4, 21),
    ("OF-2026-006", "zaakceptowana", 9900.00, 0, 0, 5, 18),
    ("OF-2026-007", "szkic", 33200.00, 20, 0, 0, 14),
    ("OF-2026-008", "wyslana", 6150.00, 0, 0, 1, 10),
    ("OF-2026-009", "zaakceptowana", 18400.00, 8, 0, 2, 7),
    ("OF-2026-010", "szkic", 2750.00, 0, 0, 3, 3),
    ("OF-2026-011", "wyslana", 45000.00, 12, 1, 4, 25),
    ("OF-2026-012", "zaakceptowana", 7800.00, 0, 1, 5, 12),
]


def main():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        users = [User(name=n, role=r) for n, r in USERS]
        clients = [Client(name=n, city=c, email=e) for n, c, e in CLIENTS]
        db.session.add_all(users + clients)
        db.session.flush()

        for number, status, net, disc, owner_i, client_i, days in OFFERS:
            db.session.add(
                Offer(
                    number=number,
                    status=status,
                    net_amount=net,
                    discount_percent=disc,
                    vat_rate=23.0,
                    created_at=datetime.now(timezone.utc) - timedelta(days=days),
                    owner_id=users[owner_i].id,
                    client_id=clients[client_i].id,
                )
            )

        db.session.commit()
        print(f"Zasiano: {len(users)} użytkowników, {len(clients)} klientów, {len(OFFERS)} ofert.")


if __name__ == "__main__":
    main()
