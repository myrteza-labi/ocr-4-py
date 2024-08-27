from utils.date_manip import get_timestamp


class RoundModel:
    def __init__(self, nom, liste_match, date_de_debut=get_timestamp(), date_de_fin=""):
        self.nom = nom
        self.liste_match = liste_match
        self.date_de_debut = date_de_debut
        self.date_de_fin = date_de_fin

    def finish(self):
        self.date_de_fin = get_timestamp()

    def to_dict(self):
        liste_match_dict = []
        for match in self.liste_match:
            liste_match_dict.append(
                (
                    [match.player1[0].identifiant_national, match.player1[1]],
                    [match.player2[0].identifiant_national, match.player2[1]],
                )
            )

        return {
            "nom": self.nom,
            "date_de_debut": self.date_de_debut,
            "date_de_fin": self.date_de_fin,
            "liste_match": liste_match_dict,
        }
