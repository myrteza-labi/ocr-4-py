import random

from models.tournament_model import TournamentModel, load_tournement_all_tournament
from views.tournament_view import TournamentView
from models.round_model import RoundModel
from models.match_model import MatchModel


BLANC = 0
NOIR = 1
EGALITE = 2

PLAYER_1 = 0
PLAYER_2 = 1

liste_match_deja_joue = []


class TournamentController:
    def __init__(self):
        self.tournament = None
        self.view = TournamentView()

    def create_tounament(self):
        sortie = self.view.show_menu()
        nom = sortie[0]
        lieu = sortie[1]
        date_de_debut = sortie[2]
        nombre_de_tours = sortie[3]
        numero_de_tour = sortie[4]
        liste_joueurs_enregistres = sortie[5]
        descritpion_remarque = sortie[6]
        self.tournament = TournamentModel(
            nom,
            lieu,
            date_de_debut,
            nombre_de_tours,
            numero_de_tour,
            [],
            liste_joueurs_enregistres,
            descritpion_remarque,
        )
        self.tournament.save()
        self.start_tournament()

    def load_tournament(self):
        list_tournament = load_tournement_all_tournament(only_not_finish=True)

        self.tournament = self.view.show_menu_load(list_tournament)
        # On recupere les données du tournoi "name" dans tinyDB
        if self.tournament is not None:
            self.extract_match_deja_joue()
            self.start_tournament()
        else:
            print("Aucun tournoi n'a été initialisé")

    def start_tournament(self):
        if self.tournament:
            # on mélange la liste des joueurs.
            random.shuffle(self.tournament.liste_joueurs_enregistres)
            # print(self.tournament.liste_joueurs_enregistres)
            while self.tournament.numero_de_tour < self.tournament.nombre_de_tours:
                print(f" --- ROUND {self.tournament.numero_de_tour + 1}---")
                if not liste_match_deja_joue:
                    round = self.generation_paire(
                        self.tournament.liste_joueurs_enregistres,
                        f"Round {self.tournament.numero_de_tour +1}",
                    )
                else:
                    round = self.generation_paire_by_score(
                        self.tournament.liste_joueurs_enregistres,
                        f"Round {self.tournament.numero_de_tour +1}",
                    )
                self.view.show_match_player(round.liste_match)
                # +++++++++++++++++++++++++++++++++++++++++++++++
                self.scoring_player(round.liste_match)
                # ++++++++++++++++++++++++++++++++++++++++++++++++
                self.tournament.liste_des_tours.append(round)
                self.inc_tour()
                round.finish()

                self.tournament.save()

                self.saveAllPlayer()
            self.tournament.finish()
            self.tournament.save()

        else:
            print("Tournament pas init")

    def scoring_player(self, liste_match):
        num_match = 1
        # Affichage du round Player 1 VS Player 2
        for player_paire in liste_match:
            liste_match_deja_joue.append(
                (
                    player_paire.player1[0].identifiant_national,
                    player_paire.player2[0].identifiant_national,
                )
            )
            print(f" --- Match {num_match}---")
            print(
                f"{player_paire.player1[0].nom} {player_paire.player1[0].prenom}"
                f" {player_paire.player1[0].get_color_str()}\n"
                f"{player_paire.player2[0].nom} {player_paire.player2[0].prenom} "
                f"{player_paire.player2[0].get_color_str()}"
            )

            vainqueur = self.view.select_one_in_list(
                ["Blanc", "Noir", "Egalité"], "resultat"
            )

            if vainqueur == "Blanc":
                if player_paire.player1[0].couleur == BLANC:
                    player_paire.player1 = (
                        player_paire.player1[0],
                        player_paire.player1[1] + 1,
                    )

                    print(f"le joueur {player_paire.player1[0].nom} à gagner 1 point.")

                    self.add_score_player(
                        player_paire.player1[0].identifiant_national, 1
                    )
                    self.add_score_player(
                        player_paire.player2[0].identifiant_national, 0
                    )
                else:
                    player_paire.player2 = (
                        player_paire.player2[0],
                        player_paire.player2[1] + 1,
                    )
                    print(f"le joueur {player_paire.player2[0].nom} à gagner 1 point.")

                    self.add_score_player(
                        player_paire.player2[0].identifiant_national, 1
                    )
                    self.add_score_player(
                        player_paire.player1[0].identifiant_national, 0
                    )

            elif vainqueur == "Noir":
                if player_paire.player1[0].couleur == NOIR:
                    player_paire.player1 = (
                        player_paire.player1[0],
                        player_paire.player1[1] + 1,
                    )
                    print(f"le joueur {player_paire.player1[0].nom} a gagner 1 point.")
                    self.add_score_player(
                        player_paire.player1[0].identifiant_national, 1
                    )
                    self.add_score_player(
                        player_paire.player2[0].identifiant_national, 0
                    )
                else:
                    player_paire.player2 = (
                        player_paire.player2[0],
                        player_paire.player2[1] + 1,
                    )
                    print(f"le joueur {player_paire.player2[0].nom} a gagner 1 point.")
                    self.add_score_player(
                        player_paire.player2[0].identifiant_national, 1
                    )
                    self.add_score_player(
                        player_paire.player1[0].identifiant_national, 0
                    )
            elif vainqueur == "Egalité":
                player_paire.player1 = (
                    player_paire.player1[0],
                    player_paire.player1[1] + 0.5,
                )
                player_paire.player2 = (
                    player_paire.player2[0],
                    player_paire.player2[1] + 0.5,
                )

                self.add_score_player(player_paire.player1[0].identifiant_national, 0.5)
                self.add_score_player(player_paire.player2[0].identifiant_national, 0.5)
                print("Match nul 0.5 point pour chaque joueur.")

            # sauvegarde le match
            num_match += 1

    def saveAllPlayer(self):
        for player in self.tournament.liste_joueurs_enregistres:
            player.save()

    def generation_paire(self, list_joueurs, name):
        liste_paire_joueurs = []
        
        random.shuffle(list_joueurs)

        for x in range(0, len(list_joueurs), 2):
            list_joueurs[x].couleur = BLANC
            list_joueurs[x + 1].couleur = NOIR
            
            instance_match = MatchModel(list_joueurs[x], list_joueurs[x + 1])
            liste_paire_joueurs.append(instance_match)

        round = RoundModel(name, liste_paire_joueurs)
        return round


    def swap_player_colors_if_needed(self, player1, player2):
        if player1.couleur == player2.couleur:
            player1.couleur = NOIR if player1.couleur == BLANC else BLANC
            player2.couleur = NOIR if player2.couleur == BLANC else BLANC


    def generation_paire_by_score(self, list_joueurs, name) -> RoundModel:
        list_pairing = []
        list_joueurs_sorted = sorted(
            list_joueurs, key=lambda x: x.scoretournois, reverse=True
        )
        players_selected = []
        for player_white in list_joueurs_sorted:
            if player_white not in players_selected:
                players_selected.append(player_white)
                for player_black in list_joueurs_sorted:
                    if (
                        player_black not in players_selected
                        and not self.match_deja_joue(player_white, player_black)
                    ):
                        self.swap_player_colors_if_needed(player_white, player_black)

                        instance_match = MatchModel(player_white, player_black)
                        list_pairing.append(instance_match)
                        players_selected.append(player_black)
                        break
        round = RoundModel(name, list_pairing)
        return round



    def match_deja_joue(self, j1, j2):
        global liste_match_deja_joue
        if (
            j1.identifiant_national,
            j2.identifiant_national,
        ) not in liste_match_deja_joue and (
            j2.identifiant_national,
            j1.identifiant_national,
        ) not in liste_match_deja_joue:
            return False
        return True

    def add_score_player(self, nationalid, point):
        for player in self.tournament.liste_joueurs_enregistres:
            if player.identifiant_national == nationalid:
                player.scoretournois += point
                player.scoreglobal += point

    def add_pairs_round(self, round):
        self.tournament.liste_des_tours.append(round)

    def inc_tour(self):
        self.tournament.numero_de_tour += 1

    def extract_match_deja_joue(self):
        global liste_match_deja_joue

        if self.tournament is not None:
            for round in self.tournament.liste_des_tours:
                for match in round.liste_match:
                    liste_match_deja_joue.append(
                        (
                            match.player1[0].identifiant_national,
                            match.player2[0].identifiant_national,
                        )
                    )

    def __str__(self):
        if self.tournament:
            return "Tournois init\n"
        else:
            return "Tournois pas init\n"
