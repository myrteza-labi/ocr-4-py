import os
from tinydb import TinyDB
from models.player_model import PlayerModel, getPlayerFromID
from views.player_view import PlayerView


class PlayerController:
    def create_player(self):
        player_view = PlayerView()
        nom, prenom, date_de_naissance, identifiant_national = player_view.show_menu()

        while getPlayerFromID(identifiant_national): 
            PlayerView.display_error(
                f"\n\033[91mCet identifiant national est déjà utilisé, veuillez en entrer un nouveau\033[0m"
            )
            identifiant_national = player_view.request_identifiant_national()


        player = PlayerModel(nom, prenom, date_de_naissance, identifiant_national)
        db = TinyDB("datas/player.json")
        db.insert(
            {
                "nom": player.nom,
                "prenom": player.prenom,
                "date_de_naissance": player.date_de_naissance,
                "identifiant_national": player.identifiant_national,
            }
        )

        os.system("clear")
        player_view.display_succes(f"\n\033[92mLe joueur {prenom} {nom} a été créé avec succès!\033[0m\n")
        input("\nAppuyez sur Entrée pour revenir au menu principal")
        os.system("clear")
