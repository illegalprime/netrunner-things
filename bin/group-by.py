#!/usr/bin/env python3
import argparse
from lib.db import DB
from lib.deck import Deck


def main(deck_paths, blacklist):
    # build card "database"
    db = DB(blacklist)
    # map cards in deck to cards in db
    cards = Deck(None, {
        card: count
        for path in deck_paths
        for card, count in Deck.from_txt_deck(path).cards.items()
    })

    print(cards.to_markdown(
        db,
        title=None,
        columns=[
            ('cycle', 'Cycle', Deck.card_cycle),
            ('type', 'Type', Deck.card_type),
        ],
        sort_by='cycle'
    ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='list cards needed by given decks by set'
    )
    parser.add_argument(
        'decks',
        metavar='DECK',
        type=str,
        nargs='+',
        help='paths to all decklists to consider'
    )
    parser.add_argument(
        '--exclude',
        help='exclude data packs by code, e.g. core2,sc19,ur'
    )
    args = parser.parse_args()
    exclude = args.exclude.split(',') if args.exclude else []
    main(args.decks, exclude)
