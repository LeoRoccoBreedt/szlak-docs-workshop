# Szlak Docs - House Style

These rules are enforced by `./build.sh`. Read them before you write.

1. **It is a trip.** Never "journey", "voyage", or "adventure".

2. **No "simply", "just", or "easily".** If it were simple they would not be
   reading the documentation.

3. **Parameter tables have exactly these columns, in this order:**
   `Name | Type | Required | Default | Description`

4. **Polish place names keep their diacritics.** Kraków, Gdańsk, Łódź, Wrocław,
   Poznań, Białowieża, Świnoujście. Not Krakow, Gdansk, Lodz.

5. **Code samples live in `samples/` and are included by reference.**
   Never paste a code block into a page. Use:
   `<!-- include: samples/your_sample.py -->`

6. **Prices in prose are written in złoty with two decimals** (249.00 PLN), and
   in code as grosze integers (`24900`). Always say which unit you mean.
