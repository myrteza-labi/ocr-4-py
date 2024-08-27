from views.view import View


class PlayerView(View):
    def show_menu(self):
        nom = self.input_str("Nom du joueur: ")
        prenom = self.input_str("Prénom du joueur: ")
        date_de_naissance = self.input_date(
            "Date de naissance du joueur (JJ/MM/AAAA): "
        )
        identifiant_national = self.input_id("Identifiant national du joueur: ")
        return nom, prenom, date_de_naissance, identifiant_national

    @staticmethod
    def display_error(message):
        print("Erreur", message)
