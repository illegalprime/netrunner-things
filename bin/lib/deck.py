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

    def sort_by_type(card):
        card, count, kind = card
        return kind

    def sort_by_count(card):
        card, count, kind = card
        return count

    def to_markdown(
            self,
            db,
            title=True,
            total=True,
            diff=False,
            sort=sort_by_type,
    ):
        return '\n'.join(([
            '',
            '## ' + self.identity if title == True else title
        ] if title else []) + ([
            '',
            'Total: {}'.format(sum(self.cards.values())),
        ] if total else []) + [
            '',
            '| Count | Name | Type |',
            '| :---: | ---- | ---- |',
        ] + [
            '| **{}x** | [{}]({}) | _{}_ |'.format(
                ('+' if diff and count > 0 else '') + str(count),
                card,
                'https://netrunnerdb.com/en/card/{}'.format(db.cards[card]['code']),
                kind,
            )
            for card, count, kind in sorted([
                (card, count,
                 db.types[db.cards[card]['type_code']]['name'])
                for card, count in self.cards.items()
            ], key=sort)
        ])

