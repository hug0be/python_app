# -*- coding: utf-8 -*-
import json

from src.quizz import Quizz

class HistoryItem:
    def __init__(self, quizz:Quizz, best_score:int = 0, time:float = 0):
        self.quizz = quizz
        self.best_score = best_score
        self.time = time

    def __str__(self):
        res = f"\"{self.quizz.title}\"\n" \
              f"Meilleur score: {self.best_score} / {self.quizz.nb_questions()}\n" \
              f"Temps: {self.time}\n"
        return res

    def to_json(self):
        return {'quizz': self.quizz.title, 'best_score': self.best_score, 'time': self.time}

    @staticmethod
    def from_json(item:dict):
        return HistoryItem(
            Quizz.get(item["quizz"]),
            item["best_score"],
            item["time"],
        )

class History:
    def __init__(self, items:[HistoryItem]=[]):
        self.items = items

    @staticmethod
    def compare_item(item, itemToEdit: HistoryItem)->HistoryItem:
        """Renvoie l'item avec les meilleurs stats"""
        mustBeReplaced = item.best_score < itemToEdit.best_score or (item.best_score == item.best_score and item.time > item.time)
        return itemToEdit if mustBeReplaced else item

    def update_item(self, itemToUpdate: HistoryItem)->bool:
        """
        Ajoute ou remplace une instance d'historique
        - Ajoute si le quizz n'a jamais été fait par l'user
        - Remplace si le score/temps est meilleur que l'ancienne instance
        """
        for i_item, item in enumerate(self.items):
            if item.quizz.title == itemToUpdate.quizz.title:
                self.items[i_item] = History.compare_item(itemToUpdate, item)
                return True
        self.items.append(itemToUpdate)
        return True

    def save(self, user):
        """Sauvegarde un historique"""
        # TODO : vérifier si le compte existe
        # if not Account.exists(user):
        #     raise UnknownAccountException(f"Le compte '{user}' n'existe pas")

        with open('data/accounts.json', 'r+') as account_file:
            accounts = json.load(account_file)
            for account in accounts:
                if account['username'] == user:
                    account['history'] = self.to_json()
                    break
            account_file.seek(0)
        with open('data/accounts.json', 'w') as account_file:
            json.dump(accounts, account_file, indent=4)

    @staticmethod
    def load(user:str):
        """Renvoie l'historique de l'utilisateur"""
        with open('data/accounts.json', 'r') as account_file:
            accounts = json.load(account_file)
            for account in accounts:
                if account['username'] == user:
                    return History.from_json(account['history'])
            return None

    @staticmethod
    def from_json(items:list):
        return History([HistoryItem.from_json(item) for item in items])

    def to_json(self):
        return [item.to_json() for item in self.items]

    def __str__(self):
        return "\n".join(item.__str__() for item in self.items)