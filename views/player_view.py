from views.view import View


class PlayerView(View):
    def show_menu(self):
        prenom = self.input_str("Veuillez entrez le prénom du joueur: ")
        nom = self.input_str("Veuillez entrez le nom du joueur: ")
        date_de_naissance = self.input_date(
            "Veuillez entrer la date de naissance du joueur (JJ/MM/AAAA): "
        )
        identifiant_national = self.input_id("Veuillez entrez l'identifiant national du joueur: ")
        return nom, prenom, date_de_naissance, identifiant_national

    @staticmethod
    def display_error(message):
        print("Erreur", message)

    @staticmethod
    def display_succes(message):
        print(message)