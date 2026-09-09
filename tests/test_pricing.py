"""Testy wyceny ofert."""

from types import SimpleNamespace

from app.services import apply_discount, calculate_offer_totals, summarize_offers


def make_offer(net, discount=0.0, vat=23.0):
    return SimpleNamespace(net_amount=net, discount_percent=discount, vat_rate=vat)


def test_apply_discount_bez_rabatu():
    assert apply_discount(1000.0, 0) == 1000.0


def test_apply_discount_dziesiec_procent():
    assert apply_discount(1000.0, 10) == 900.0


def test_calculate_offer_totals_zwraca_komplet_kluczy():
    result = calculate_offer_totals(make_offer(1000.0, 10))
    assert result is not None
    assert "net" in result and "vat" in result and "gross" in result


def test_summarize_offers_liczy_pozycje():
    offers = [make_offer(1000.0), make_offer(2000.0)]
    assert summarize_offers(offers)["count"] == 2


def test_podsumowanie_obejmuje_wszystkie_oferty(client, sample_data):
    client.get(f"/login/{sample_data['user_id']}")
    response = client.get("/offers")
    assert "Suma wartości wszystkich ofert" in response.get_data(as_text=True)
