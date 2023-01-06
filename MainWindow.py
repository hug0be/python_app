import json
import sys

from PySide6 import QtUiTools
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader


loader = QUiLoader()

class Account:
    def __init__(self, username:str, password:str):
        self.username = username
        self.password = password
    def save(self):
        """Sauvegarde un compte"""
        with open('data/accounts.json', 'r+') as accounts_file:
            accounts = json.load(accounts_file)
            accounts.append({'username': self.username, 'password': self.password})
            accounts_file.seek(0)
            json.dump(accounts, accounts_file)
    @staticmethod
    def exists(username:str):
        """Teste si un compte existe"""
        with open('data/accounts.json', 'r') as file:
            for account in json.load(file):
                if username == account['username']: return True
            return False

    @staticmethod
    def access(username:str, password:str):
        """
        Test si un compte existe et si le mot de passe est juste
        Renvoie une UnknownAccountException s'il n'existe pas
        Renvoie une WrongPasswordException si le mot de passe est incorrecte
        Renvoie True s'il existe
        """
        with open('data/accounts.json', 'r') as file:
            accounts = json.load(file)
            for account in accounts:
                if username == account['username']:
                    if password == accounts['password']: return True
                    raise WrongPasswordException
            raise UnknownAccountException
class WrongPasswordException(Exception): pass
class UnknownAccountException(Exception): pass
def create_account_attempt():
    """Méthode appeler pour une tentative de création de compte"""

    #Obtention des identifiants
    username = window.accountUsername.toPlainText()
    password = window.accountPassword.toPlainText()

    #Validation des identifiants
    if not username:
        print("Le pseudo est vide")
        return False
    if not password:
        print("Le mot de passe est vide")
        return False

    #Check si les identifiants existent
    if Account.exists(username):
        print("Ce compte existe déjà")
        return False

    #All good !
    Account(username, password).save()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    #Page principale
    window = loader.load("untitled.ui", None)
    window.setWindowIcon(QIcon('resources/images/favicon_96x96.png'))
    loader = QtUiTools.QUiLoader()

    #Bouton "Se connecter"
    # window.connectButton.clicked.connect(connexionAttempt)
    window.createAccountButton.clicked.connect(create_account_attempt)

    window.show()
    sys.exit(app.exec())
