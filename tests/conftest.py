import pytest

from app import create_app, db
from app.models import Client, Offer, User


@pytest.fixture
def app():
    app = create_app({"SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", "TESTING": True})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_data(app):
    with app.app_context():
        user = User(name="Anna Nowak", role="handlowiec")
        other = User(name="Marek Zieliński", role="handlowiec")
        klient = Client(name="Zakład Stolarski Kowalski", city="Poznań")
        db.session.add_all([user, other, klient])
        db.session.flush()

        offer = Offer(
            number="OF-TEST-001",
            status="wyslana",
            net_amount=10000.0,
            discount_percent=10.0,
            vat_rate=23.0,
            owner_id=user.id,
            client_id=klient.id,
        )
        db.session.add(offer)
        db.session.commit()
        return {"user_id": user.id, "other_id": other.id, "offer_id": offer.id}
