import pathlib
import json
import os
from os import path


ROOT = pathlib.Path(__file__).parent


class DB():
    def __init__(self, blacklist=[]):
        pack_ban = list(map(lambda p: p + '.json', blacklist))

        self.cycles = {
            cycle['code']: cycle
            for cycle in json.load(open(path.join(ROOT, 'cycles.json')))
        }

        self.packs = {
            pack['code']: pack
            for pack in json.load(open(path.join(ROOT, 'packs.json')))
        }

        self.types = {
            kind['code']: kind
            for kind in json.load(open(path.join(ROOT, 'types.json')))
        }

        self.factions = {
            faction['code']: faction
            for faction in json.load(open(path.join(ROOT, 'factions.json')))
        }

        ordered_packs = self.__sort_packs(
            self.packs, self.cycles, os.listdir(path.join(ROOT, 'packs'))
        )
        self.cards = {
            card['title']: card
            for pack in ordered_packs
            if pack not in pack_ban
            for card in json.load(open(path.join(ROOT, 'packs', pack), 'r'))
        }

    def __sort_packs(self, packs, cycles, files):
        def pack_key(name):
            pack = packs[path.splitext(name)[0]]
            return cycles[pack['cycle_code']]['position']
        return sorted(files, key=pack_key)
