#!/usr/bin/env python3
import re
import copy


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


def markdown_deck(deck):
    identity, annotated = deck
    # print the identity as a title
    lines = [
        '',
        '## {}'.format(identity),
        '',
        'Total: {}'.format(sum(annotated.values())),
        '',
    ]
    lines += [
        '- {}x **{}**'.format(count, card)
        for card, count in annotated.items()
    ]
    return '\n'.join(lines)


def markdown_transition(diff):
    return '\n'.join([
        '',
        '### Transition',
        '',
    ] + [
        '- **{}** _{}_'.format(
            ('+' if count > 0 else '') + str(count),
            card
        )
        for card, count in sorted(diff.items(), key=lambda c: c[1] > 0)
    ])


def transition(a, b):
    return {
        card: b.get(card, 0) - a.get(card, 0)
        for card in set(a.keys()).union(b.keys())
        if b.get(card) != a.get(card)
    }


def main(deck_paths):
    # parse files for deck info
    decks = list(map(import_txt_deck, deck_paths))

    # diff each pair
    print(markdown_deck(decks[0]))
    for i in range(1, len(decks)):
        diff = transition(decks[i - 1][1], decks[i][1])
        print(markdown_transition(diff))
        print(markdown_deck(decks[i]))


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
