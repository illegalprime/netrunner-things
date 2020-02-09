#!/usr/bin/env python3
import argparse
from lib.db import DB
from lib.deck import Deck


def shorten_name(name):
    short = name.split(':')[0].split()[0]
    return {
        'Haas-Bioroid': 'HB',
    }.get(short, short)


def main(deck_paths, shorten):
    # build card db
    db = DB()
    # parse all decks
    decks = list(map(Deck.from_txt_deck, deck_paths))

    # keep track of where every card is used
    owners = {}
    for deck in decks:
        for card, count in deck.cards.items():
            owners.setdefault(card, {})[deck.identity] = count

    # create the 'seen elsewhere' column
    def other_owners(deck, db, card):
        others = {
            owner: alt_count
            for owner, alt_count in owners[card].items()
            if owner != deck.identity
            if sum(owners[card].values()) > 3 # HACK
        }
        text = ', '.join([
            '{}x {}'.format(
                count,
                shorten_name(identity) if shorten else identity
            )
            for identity, count in others.items()
        ])
        return {
            'display': text,
            'sort': text,
        }

    for deck in decks:
        print(deck.to_markdown(
            db,
            columns=[
                ('owners', 'Used Elsewhere', other_owners),
                ('type', 'Type', Deck.card_type),
            ],
            sort_by='type',
        ))


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
    parser.add_argument(
        '--shorten',
        default=False,
        action='store_true',
        help='attempt to shorten identity names',
    )
    args = parser.parse_args()
    main(args.decks, args.shorten)
