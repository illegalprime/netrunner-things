#!/usr/bin/env python3
import argparse
from lib.db import DB
from lib.deck import Deck


def main(deck_paths):
    db = DB()
    decks = list(map(Deck.from_txt_deck, deck_paths))

    # diff each pair
    print(decks[0].to_markdown(db))
    for i in range(1, len(decks)):
        diff = decks[i].diff(decks[i - 1])
        print(diff.to_markdown(
            db,
            title='### Transition',
            total=False,
            diff=True,
            sort_by='count'
        ))
        print(decks[i].to_markdown(db))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='print sequantial deltas between decks'
    )
    parser.add_argument(
        'decks',
        metavar='DECK',
        type=str,
        nargs='+',
        help='paths to all decklists to consider'
    )
    args = parser.parse_args()
    main(args.decks)

