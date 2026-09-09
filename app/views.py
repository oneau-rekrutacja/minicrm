"""Widoki MiniCRM."""

from flask import Blueprint, redirect, render_template, request, session, url_for

from app import db
from app.models import OFFER_STATUSES, Client, Offer, User
from app.services import calculate_offer_totals, summarize_offers

bp = Blueprint("main", __name__)

PER_PAGE = 5


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(User, user_id)


@bp.route("/")
def index():
    return redirect(url_for("main.offer_list"))


@bp.route("/login/<int:user_id>")
def login(user_id):
    """Uproszczone logowanie — wybór użytkownika bez hasła (tylko demo)."""
    session["user_id"] = user_id
    return redirect(url_for("main.offer_list"))


@bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("main.offer_list"))


@bp.route("/offers")
def offer_list():
    user = current_user()
    if not user:
        return render_template("login.html", users=User.query.all())

    status = request.args.get("status", "")
    page = request.args.get("page", 1, type=int)

    query = Offer.query.filter(Offer.owner_id == user.id)
    if status:
        query = query.filter(Offer.status == status)

    offers = query.order_by(Offer.created_at.desc()).paginate(
        page=page, per_page=PER_PAGE, error_out=False
    )

    # Podsumowanie musi obejmowac wszystkie oferty, nie tylko biezaca strone.
    all_offers = Offer.query.all()
    summary = summarize_offers(all_offers)

    return render_template(
        "offers.html",
        user=user,
        offers=offers,
        summary=summary,
        statuses=OFFER_STATUSES,
        active_status=status,
        totals=calculate_offer_totals,
    )


@bp.route("/offers/<int:offer_id>")
def offer_detail(offer_id):
    user = current_user()
    if not user:
        return redirect(url_for("main.offer_list"))

    offer = db.session.get(Offer, offer_id)
    if offer is None:
        return render_template("not_found.html"), 404

    return render_template(
        "offer_detail.html", user=user, offer=offer, totals=calculate_offer_totals(offer)
    )


@bp.route("/offers/<int:offer_id>/edit", methods=["GET", "POST"])
def offer_edit(offer_id):
    user = current_user()
    if not user:
        return redirect(url_for("main.offer_list"))

    offer = db.session.get(Offer, offer_id)
    if offer is None:
        return render_template("not_found.html"), 404

    if request.method == "POST":
        offer.net_amount = request.form.get("net_amount", type=float) or 0.0
        offer.discount_percent = request.form.get("discount_percent", type=float) or 0.0
        offer.status = request.form.get("status") or offer.status
        db.session.commit()
        return redirect(url_for("main.offer_detail", offer_id=offer.id))

    return render_template(
        "offer_edit.html", user=user, offer=offer, statuses=OFFER_STATUSES
    )


@bp.route("/clients")
def client_list():
    user = current_user()
    if not user:
        return redirect(url_for("main.offer_list"))
    return render_template("clients.html", user=user, clients=Client.query.all())
