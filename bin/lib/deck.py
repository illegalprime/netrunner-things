import re


class Deck():
    def __init__(self, identity, cards):
        self.identity = identity
        self.cards = cards

    def from_txt_deck(path):
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
            return Deck(identity, cards)

    # create a deck that is the delta of how to get to `self` from `deck`
    def diff(self, deck):
        return Deck(self.identity, {
            card: self.cards.get(card, 0) - deck.cards.get(card, 0)
            for card in set(self.cards.keys()).union(deck.cards.keys())
            if self.cards.get(card) != deck.cards.get(card)
        })

    def card_type(db, card):
        name = db.types[db.cards[card]['type_code']]['name']
        return { 'display': name, 'sort': name }

    def card_cycle(db, card):
        info = db.cards[card]
        pack = db.packs[info['pack_code']]
        cycle = db.cycles[pack['cycle_code']]
        name = '{}, {}'.format(cycle['name'], info['position'])
        sort = (cycle['position'], info['position'])
        return { 'display': name, 'sort': sort }

    def to_markdown(
            self,
            db,
            title=True,
            total=True,
            diff=False,
            sort_by='type',
            columns=[('type', 'Type', card_type)]
    ):
        return '\n'.join(([
            '',
            '## ' + self.identity if title == True else title
        ] if title else []) + ([
            '',
            'Total: {}'.format(sum(self.cards.values())),
        ] if total else []) + [
            '',
            '| Count | Name | ' + ' | '.join([
                name for _, name, _ in columns
            ]) + ' |',
            '| :---: | ---- |' + (' ---- |' * len(columns)),
        ] + [
            '| **{}x** | [{}]({}) |'.format(
                ('+' if diff and info['count'] > 0 else '') + str(info['count']),
                info['name'],
                'https://netrunnerdb.com/en/card/{}'.format(db.cards[info['name']]['code']),
            ) + '|'.join([
                ' _{}_ '.format(info[key]['display'])
                for key, _, _ in columns
            ] + [''])
            for info in sorted([
                dict([
                    ('count', count),
                    ('name', card),
                ] + [
                    (key, f(db, card))
                    for key, _, f in columns
                ])
                for card, count in self.cards.items()
            ], key=lambda i: i[sort_by]['sort'])
        ])


