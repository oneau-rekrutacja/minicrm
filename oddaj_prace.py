#!/usr/bin/env python3
"""Pakuje całą Twoją pracę do jednego pliku. Uruchom na koniec zadania:

    python oddaj_prace.py "Imię Nazwisko"

Na Windowsie, jeśli `python` nie działa, spróbuj `py oddaj_prace.py "Imię Nazwisko"`.
Skrypt nie wymaga żadnych bibliotek poza standardowymi.
"""

import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from datetime import datetime
from pathlib import Path

PLIKI = ["BUGS.md", "PR.md", "REVIEW.md", "NOTATKI.md"]


def slug(tekst):
    """Zamienia imię i nazwisko na bezpieczną nazwę pliku."""
    # ł, Ł, ø, đ nie rozkładają się w NFKD — trzeba je zmapować ręcznie
    tekst = tekst.translate(str.maketrans("łŁøØđĐ", "lLoODD"))
    tekst = unicodedata.normalize("NFKD", tekst).encode("ascii", "ignore").decode("ascii")
    tekst = re.sub(r"[^A-Za-z0-9]+", "-", tekst).strip("-").lower()
    return tekst or "kandydat"


def git(*args):
    """Uruchamia polecenie gita i zwraca jego wyjście (pusty tekst przy błędzie)."""
    try:
        wynik = subprocess.run(
            ["git", *args], capture_output=True, text=True, timeout=30, encoding="utf-8"
        )
        return wynik.stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print("Podaj swoje imię i nazwisko, na przykład:")
        print('  python oddaj_prace.py "Anna Nowak"')
        return 1

    imie = sys.argv[1].strip()
    nazwa = f"praca-{slug(imie)}-{datetime.now():%Y%m%d-%H%M}"

    print(f"Pakuję pracę: {imie}\n")

    tymczasowy = Path(tempfile.mkdtemp())
    katalog = tymczasowy / nazwa
    katalog.mkdir()

    # 1. Pliki, które napisałeś
    znalezione = 0
    for plik in PLIKI:
        zrodlo = Path(plik)
        if zrodlo.is_file():
            shutil.copy2(zrodlo, katalog / plik)
            print(f"  [+] {plik}")
            znalezione += 1
        else:
            print(f"  [ ] {plik} (brak)")

    if znalezione == 0:
        print("\nUWAGA: nie znalazłem żadnego z plików BUGS.md / PR.md / REVIEW.md.")
        print("Czy na pewno jesteś w katalogu projektu? Pakuję dalej samo repozytorium.")

    # 2. Repozytorium z pełną historią — gałęzie, commity, autorstwo, daty
    bundle = katalog / "repozytorium.bundle"
    git("bundle", "create", str(bundle), "--all")
    if bundle.is_file():
        print("  [+] repozytorium.bundle (Twoje gałęzie i commity)")

    # 3. Podgląd bez rozpakowywania bundla
    twoje = git("log", "origin/main..HEAD", "--format=%h | %an | %ad | %s", "--date=short")
    podglad = "\n".join([
        "GAŁĘZIE",
        git("branch", "-vv"),
        "",
        "TWOJE COMMITY (poza punktem startowym)",
        twoje.strip() or "  brak — nic nie zostało zacommitowane",
        "",
        "NIEZACOMMITOWANE ZMIANY",
        git("status", "--short").strip() or "  brak",
        "",
        "PEŁNA HISTORIA",
        git("log", "--all", "--format=%h | %an | %ad | %s", "--date=short"),
    ])
    (katalog / "podglad.txt").write_text(podglad, encoding="utf-8")
    print("  [+] podglad.txt")

    # 4. Diff wobec punktu startowego
    zmiany = git("diff", "origin/main...HEAD")
    if zmiany.strip():
        (katalog / "zmiany.patch").write_text(zmiany, encoding="utf-8")
        print("  [+] zmiany.patch")

    # 5. Praca poza commitem — bez tego przepadłaby przy oddaniu
    robocze = git("diff", "HEAD")
    if robocze.strip():
        (katalog / "zmiany-niezacommitowane.patch").write_text(robocze, encoding="utf-8")
        print("  [+] zmiany-niezacommitowane.patch (zmiany, których nie zdążyłeś zacommitować)")

    # 6. Nowe pliki, o których git jeszcze nie wie (bez tych z .gitignore)
    nieznane = [
        linia.strip()
        for linia in git("ls-files", "--others", "--exclude-standard").splitlines()
        if linia.strip() and linia.strip() not in PLIKI
    ]
    if nieznane:
        cel = katalog / "pliki-nowe"
        skopiowane = 0
        for wzgledna in nieznane:
            zrodlo = Path(wzgledna)
            # Pomijamy to, co i tak nie jest pracą: bazy, archiwa, duże binaria
            if not zrodlo.is_file() or zrodlo.stat().st_size > 1_000_000:
                continue
            docelowy_plik = cel / wzgledna
            docelowy_plik.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(zrodlo, docelowy_plik)
            skopiowane += 1
        if skopiowane:
            print(f"  [+] pliki-nowe/ — pliki spoza commitów: {skopiowane}")

    # 7. Jedno archiwum ZIP w katalogu domowym — otwiera się wszędzie bez narzędzi
    docelowy = Path.home() / nazwa
    archiwum = Path(shutil.make_archive(str(docelowy), "zip", tymczasowy, nazwa))
    shutil.rmtree(tymczasowy, ignore_errors=True)

    rozmiar = archiwum.stat().st_size / 1024
    print(f"\nGotowe. Twoja praca jest w jednym pliku:\n")
    print(f"  {archiwum}\n")
    print(f"Rozmiar: {rozmiar:.0f} KB. Przekaż go osobie prowadzącej.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
