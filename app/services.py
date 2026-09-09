"""Logika biznesowa MiniCRM: wyceny i podsumowania list."""


def apply_discount(net_amount, discount_percent):
    """Zwraca kwotę netto po rabacie procentowym."""
    if not discount_percent:
        return net_amount
    return net_amount * (1 - discount_percent / 100.0)


def calculate_offer_totals(offer):
    """Liczy kwoty oferty: netto po rabacie, VAT i brutto.

    Zwraca słownik z kluczami: net, vat, gross.
    """
    net_after_discount = apply_discount(offer.net_amount, offer.discount_percent)
    vat = offer.net_amount * (offer.vat_rate / 100.0)
    gross = net_after_discount + vat
    return {
        "net": round(net_after_discount, 2),
        "vat": round(vat, 2),
        "gross": round(gross, 2),
    }


def summarize_offers(offers):
    """Podsumowanie wartości listy ofert — suma brutto i liczba pozycji."""
    total_gross = 0.0
    for offer in offers:
        total_gross += calculate_offer_totals(offer)["gross"]
    return {"count": len(offers), "total_gross": round(total_gross, 2)}
