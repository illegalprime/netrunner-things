#!/usr/bin/env python3
import argparse
from lib.db import DB
from lib.deck import Deck


def main(deck_paths, blacklist, columns, sort_by):
    # build card "database"
    db = DB(blacklist)

    # turn all the deck files into decks
    decks = list(map(Deck.from_txt_deck, deck_paths))

    # map cards in deck to cards in db
    cards = Deck(None, {
        card: count
        for deck in decks
        for card, count in deck.cards.items()
    })

    # lookup for IDs of decks
    id_lookup = {
        card: deck.identity
        for deck in decks
        for card in deck.cards
    }

    # lookup identity if needed
    def get_identity(deck, db, card):
        identity = id_lookup[card]
        return { 'display': identity, 'sort': (identity,) }

    all_columns = {
        'cycle': ('Cycle', Deck.card_cycle),
        'type': ('Type', Deck.card_type),
        'identity': ('Identity', get_identity),
        'faction': ('Faction', Deck.card_faction),
    }

    print(cards.to_markdown(
        db,
        title=None,
        columns=[
            (key, all_columns[key][0], all_columns[key][1])
            for key in columns
        ],
        sort_by=sort_by
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
    parser.add_argument(
        '--cols',
        default='cycle,type',
        help='columns to print, e.g. cycle,type,identity'
    )
    parser.add_argument(
        '--sort',
        default=None,
        help='list of columns to sort by, e.g. type,faction'
    )
    args = parser.parse_args()
    exclude = args.exclude.split(',') if args.exclude else []
    columns = args.cols.split(',')
    sort_by = args.sort.split(',') if args.sort else columns
    main(args.decks, exclude, columns, sort_by)
