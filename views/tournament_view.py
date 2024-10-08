from views.view import View
from models.player_model import PlayerModel
from utils.date_manip import get_timestamp


PLAYER_1 = 0
PLAYER_2 = 1


class TournamentView(View):
    def show_menu(self):
        nom = self.city_input("Entrez le nom du tournois: ")
        lieu = self.city_input("Veuillez indiquer la ville où se déroule le tournoi : ")
        date_de_debut = get_timestamp()
        all_player = PlayerModel.get_all_player_from_db()
        while True:
            nombre_de_tours = self.input_int(
                "Indiquez le nombre de tours ou appuyez sur Entrée pour sélectionner 4 tours par défaut :", defaut_value=4
            )
            if nombre_de_tours * 2 > len(all_player):
                print(
                    "Vous avez selectionner trop de tour par rapport au nombre de joueurs inscrit"
                )
            else:
                break

        numero_de_tour = 0
        nb_player = nombre_de_tours * 2
        liste_joueurs_enregistres = self.select_many_in_list(
            all_player, nb_player, "player"
        )
        descritpion_remarque = self.input_str("remarque général: ")

        return (
            nom,
            lieu,
            date_de_debut,
            nombre_de_tours,
            numero_de_tour,
            liste_joueurs_enregistres,
            descritpion_remarque,
        )

    def show_menu_load(self, list_tournament):
        while True:
            if list_tournament == []:

                print("\n\nAucun tournois en cours\n\n")

                return None
            else:
                for idx, tournament in enumerate(list_tournament):
                    print(
                        f"[{idx}] \033[36m{tournament.nom}\033[0m {tournament.lieu.upper()} ( {tournament.date_de_debut} )"
                    )

                tournament_id_select = self.input_int(
                    "\n\033[93mVeuillez sélectionner le tournoi à reprendre : \033[0m\n"
                )

                if tournament_id_select in range(len(list_tournament)):
                    return list_tournament[tournament_id_select]
                else:
                    print(
                        "L id sélectionné(",
                        tournament_id_select,
                        ") n'est pas correct.",
                    )

    def show_match_player(self, list_match):
        for player_paire in list_match:
            print(
                f"{player_paire.player1[0].nom} {player_paire.player1[0].get_color_str()}  VS "
                f"{player_paire.player2[0].nom} {player_paire.player2[0].get_color_str()} "
            )
            
        input("\nAppuyez sur la touche \033[36m'Entrer'\033[0m pour demarrer")
