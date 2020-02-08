#!/usr/bin/env python3
import re
import os
import json
import pathlib
from os import path


PACK_BAN = [
    'core2.json',
]
ROOT = pathlib.Path(__file__).parent


def import_txt_deck(path):
    with open(path, 'r') as deck_file:
        # read everything
        text = deck_file.read()
        # remove data pack and influence count
        text = re.sub(r' \(.*', '', text)
        # get the number of copies and the name of the card
        cards = re.findall(r'^([0-9]+)x (.*?)$', text, re.MULTILINE)
        # collect card counts in dict
        cards = {
            card: int(count)
            for count, card in cards
        }
        # the second line is the identity
        identity = text.splitlines()[1].strip()
        return (identity, cards)


def sort_packs(packs, cycles, files):
    def pack_key(name):
        return cycles[packs[path.splitext(name)[0]]['cycle_code']]['position']
    return sorted(files, key=pack_key)


def build_card_db():
    db = {
        'cycles': {
            cycle['code']: cycle
            for cycle in json.load(open(path.join(ROOT, 'cycles.json')))
        },
        'packs': {
            pack['code']: pack
            for pack in json.load(open(path.join(ROOT, 'packs.json')))
        },
    }
    ordered_packs = sort_packs(
        db['packs'],
        db['cycles'],
        os.listdir(path.join(ROOT, 'packs'))
    )
    db['cards'] = {
        card['title']: card
        for pack in ordered_packs
        if pack not in PACK_BAN
        for card in json.load(open(path.join(ROOT, 'packs', pack), 'r'))
    }
    return db


def lookup_deck(db, deck):
    built = {}
    (identity, deck) = deck
    for card in deck:
        info = db['cards'][card]
        pack = db['packs'][info['pack_code']]
        cycle = db['cycles'][pack['cycle_code']]
        built[card] = {
            'name': card,
            'pack': pack['name'],
            'cycle': cycle['name'],
            'cycle_pos': cycle['position'],
            'position': info['position'],
            'count': deck[card],
            'id': identity
        }
    return built


def key_cycle(card):
    return (card['cycle_pos'], card['position'])


def main(deck_paths):
    # parse files for deck info
    decks = map(import_txt_deck, deck_paths)
    # build card "database"
    db = build_card_db()
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
    import sys
    main(sys.argv[1:])
