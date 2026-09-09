"""Modele domenowe MiniCRM."""

from datetime import datetime, timezone

from app import db

OFFER_STATUSES = ["szkic", "wyslana", "zaakceptowana", "odrzucona"]

STATUS_LABELS_PL = {
    "szkic": "Szkic",
    "wyslana": "Wysłana",
    "zaakceptowana": "Zaakceptowana",
    "odrzucona": "Odrzucona",
}


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(40), nullable=False, default="handlowiec")

    offers = db.relationship("Offer", back_populates="owner")


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(120))
    email = db.Column(db.String(200))

    offers = db.relationship("Offer", back_populates="client")


class Offer(db.Model):
    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(40), nullable=False, unique=True)
    status = db.Column(db.String(40), nullable=False, default="szkic")

    net_amount = db.Column(db.Float, nullable=False, default=0.0)
    discount_percent = db.Column(db.Float, nullable=False, default=0.0)
    vat_rate = db.Column(db.Float, nullable=False, default=23.0)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    client = db.relationship("Client", back_populates="offers")
    owner = db.relationship("User", back_populates="offers")

    @property
    def status_label(self):
        return STATUS_LABELS_PL.get(self.status, self.status)
