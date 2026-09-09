"""Testy widoków."""


def test_lista_ofert_wymaga_logowania(client):
    response = client.get("/offers", follow_redirects=True)
    assert "Wybierz użytkownika" in response.get_data(as_text=True)


def test_lista_ofert_po_zalogowaniu(client, sample_data):
    client.get(f"/login/{sample_data['user_id']}")
    response = client.get("/offers")
    assert response.status_code == 200
    assert "OF-TEST-001" in response.get_data(as_text=True)


def test_szczegoly_oferty(client, sample_data):
    client.get(f"/login/{sample_data['user_id']}")
    response = client.get(f"/offers/{sample_data['offer_id']}")
    assert response.status_code == 200
