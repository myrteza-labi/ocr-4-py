from controllers.reports_controller import ReportController
from views.view import View
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController


class MainView(View):
    def show_menu(self):
        menu = [
            "1 : Créer un joueur",
            "2 : Créer un tournoi",
            "3 : Reprendre un tournoi en cours",
            "4 : Voir les rapports",
            f"\033[91mQ : Quitter l'application\033[0m"
        ]
        choix_utilisateur = self.affichage_menu(
            f"\n\033[93m MENU PRINCIPAL\033[0m\n", menu, ["1", "2", "3", "4", "q"]
        )

        match choix_utilisateur:
            case "1":
                PlayerController().create_player()
            case "2":
                tourn_instance = TournamentController()
                tourn_instance.create_tounament()
            case "3":
                tourn_instance = TournamentController()
                tourn_instance.load_tournament()
            case "4":
                report_instance = ReportController()
                report_instance.create_report()
            case "Q":
                return True
            case _:
                print("Erreur")
        return False
