
# Diff Decks

Take a bunch of decklists and annotate each card with what other decks use them.
This helps you quickly switch between a set of decks.
An example given is the System Core 2019 demo decks.

## But How?

Download decks from netrunnerdb as `.txt` files, with a different identity for each deck.

Then generate markdown with:

```
./diff-decks.py *.txt
```

You can optionally turn it into an HTML file with `pandoc`:

```
./diff-decks.py *.txt | pandoc \
    -f markdown \
    -t html -s \
    --metadata pagetitle='SC19 Demo Decks' \
    | sed 's/<style>/\0 body { font-family: monospace; }/' \
    > decks.html
```

