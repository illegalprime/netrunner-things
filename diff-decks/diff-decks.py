#!/usr/bin/env python3
import re
import copy


CORPS = set(['HB', 'NBN', 'Jinteki', 'Weyland'])


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


def shorten_name(name):
    short = name.split(':')[0].split()[0]
    return {
        'Haas-Bioroid': 'HB',
    }.get(short, short)


def markdown_deck(identity, annotated):
    # print the identity as a title
    lines = [
        '',
        '## {}'.format(identity),
        '',
        'Total: {}'.format(sum(list(zip(*annotated.values()))[0])),
        '',
    ]
    lines += [
        '- {}x **{}**'.format(count, card)
        + ('' if not others else ' _[{}]_'.format(', '.join([
            '{}x {}'.format(count, shorten_name(owner))
            for owner, count in others.items()
        ])))
        for card, (count, others) in annotated.items()
    ]
    return '\n'.join(lines)


def main(deck_paths):
    # parse files for deck info
    decks = dict(map(import_txt_deck, deck_paths))

    # keep track of where every card is used
    owners = {}
    for identity, deck in decks.items():
        for card, count in deck.items():
            owners.setdefault(card, {})[identity] = count

    # merge this data with decks
    annotated = {
        identity: {
            card: (count, {
                owner: alt_count
                for owner, alt_count in owners[card].items()
                if owner != identity
                if sum(owners[card].values()) > 3 # HACK
            })
            for card, count in deck.items()
        }
        for identity, deck in decks.items()
    }

    # print out hackers first
    for identity, deck in annotated.items():
        if shorten_name(identity) not in CORPS:
            print(markdown_deck(identity, deck))
    for identity, deck in annotated.items():
        if shorten_name(identity) in CORPS:
            print(markdown_deck(identity, deck))


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
