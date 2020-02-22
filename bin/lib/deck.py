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

    def card_type(deck, db, card):
        kind = db.types[db.cards[card]['type_code']]
        return {
            'display': kind['name'],
            'sort': (kind['side_code'], kind['name']),
        }

    def card_faction(deck, db, card):
        faction = db.factions[db.cards[card]['faction_code']]
        is_neutral = faction['code'] in ['neutral-corp', 'neutral-runner']
        return {
            'display': faction['name'],
            'sort': (faction['side_code'], str(int(is_neutral)), faction['name'])
        }

    def card_cycle(deck, db, card):
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
            sort_by=['type'],
            columns=[('type', 'Type', card_type)]
    ):
        rows = sorted([
            dict([
                ('count', count),
                ('name', card),
            ] + [
                (key, f(self, db, card))
                for key, _, f in columns
            ])
            for card, count in self.cards.items()
        ], key=lambda card: [
            key
            for col in sort_by
            for key in (
                card[col]['sort'] if type(card[col]) is dict else (card[col],)
            )
        ])

        widths = {
            col: max(map(lambda row: len(
                row[col]['display'] if type(row[col]) is dict else str(row[col])
            ), rows))
            for col in rows[0].keys()
        }

        return '\n'.join(([
            '',
            '## ' + self.identity if title == True else title
        ] if title else []) + ([
            '',
            'Total: {}'.format(sum(self.cards.values())),
        ] if total else []) + [
            '',
            '|'.join([
                '',
                ' Count'.ljust(widths['count'] + 7),
                ' Name'.ljust(widths['name'] + 43),
            ] + [
                ' ' + name.ljust(widths[key] + 4)
                for key, name, _ in columns
            ] + ['']),
            '|'.join([
                '',
                ' :{}: '.format('-' * (widths['count'] + 3)),
                ' {} '.format('-' * (widths['name'] + 41)),
            ] + [
                ' {} '.format('-' * (widths[key] + 3))
                for key, _, _ in columns
            ] + [''])
        ] + [
            '|'.join([
                '',
                ' **{}x** '.format(
                    ('+' if diff and info['count'] > 0 else '') + str(info['count'])
                ).ljust(widths['count'] + 7),

                ' [{}]({}) '.format(
                    info['name'],
                    'https://netrunnerdb.com/en/card/{}'.format(db.cards[info['name']]['code'])
                ).ljust(widths['name'] + 43),
            ] + [
                ' _{}_ '.format(info[key]['display']).ljust(widths[key] + 5)
                if info[key]['display'] else ' ' * (widths[key] + 5)
                for key, _, _ in columns
            ] + [''])
            for info in rows
        ])


