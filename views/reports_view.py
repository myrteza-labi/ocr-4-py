from views.view import View


class ReportsView(View):
    def show_menu(self):
        menu = [
            "1 : liste de tous les joueurs par ordre alphabétique.",
            "2 : liste de tous les tournois.",
            "3 : nom et dates d’un tournoi donné.",
            "4 : liste des joueurs du tournoi par ordre alphabétique.",
            "5 : liste de tous les tours du tournoi et de tous les matchs du tour.",
            "r : retour dans le menu principal.",
        ]
        choix = self.affichage_menu(
            "\n=== RAPPORTS ===\n", menu, ["1", "2", "3", "4", "5", "r"]
        )
        return choix

    def show_select_in_list(self, list_data, name):
        return self.select_one_in_list(list_data, name)
