#!/usr/bin/env python3
import argparse
from lib.db import DB
from lib.deck import Deck


# TODO use new Deck lib for outputting into markdown


def lookup_deck(db, deck):
    built = {}
    for card in deck.cards:
        info = db.cards[card]
        pack = db.packs[info['pack_code']]
        cycle = db.cycles[pack['cycle_code']]
        built[card] = {
            'name': card,
            'pack': pack['name'],
            'cycle': cycle['name'],
            'cycle_pos': cycle['position'],
            'position': info['position'],
            'count': deck.cards[card],
            'id': deck.identity
        }
    return built


def key_cycle(card):
    return (card['cycle_pos'], card['position'])


def main(deck_paths, blacklist):
    # build card "database"
    db = DB(blacklist)
    # parse files for deck info
    decks = list(map(Deck.from_txt_deck, deck_paths))
    # map cards in deck to cards in db
    cards = [
        card
        for deck in decks
        for card in lookup_deck(db, deck).values()
    ]
    # sort according to cycle and position
    by_cycle = sorted(cards, key=key_cycle)

    # get the longest card name
    card_name_max = max(map(lambda c: len(c['name']), cards))

    # get the longest cycle name
    card_cycle_max = max(map(lambda c: len(c['cycle']), cards))

    for card in by_cycle:
        print('{}x {} {} [{}]'.format(
            card['count'],
            str.ljust(card['name'], card_name_max + 4),
            str.ljust('({}, {})'.format(
                card['cycle'], card['position']
            ), card_cycle_max + 8),
            card['id']
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
