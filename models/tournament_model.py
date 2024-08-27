from tinydb import TinyDB, Query
from models.player_model import getPlayerFromID
from models.round_model import RoundModel
from models.match_model import MatchModel
from utils.date_manip import get_timestamp

PATH = "datas/tournament.json"
PLAYER_1 = 0
PLAYER_2 = 1


class TournamentModel:
    def __init__(
        self,
        nom,
        lieu,
        date_de_debut,
        nombre_de_tours: 4,
        numero_de_tour,
        liste_des_tours,
        liste_joueurs_enregistres,
        descritpion_remarque,
    ):
        self.nom = nom
        self.lieu = lieu
        self.date_de_debut = date_de_debut
        self.date_de_fin = ""
        self.nombre_de_tours = nombre_de_tours
        self.numero_de_tour = numero_de_tour
        self.liste_des_tours = liste_des_tours
        self.liste_joueurs_enregistres = liste_joueurs_enregistres
        self.descritpion_remarque = descritpion_remarque

    def save(self):
        db = TinyDB(PATH, indent=4)
        query = Query()
        tournoi = db.search(query.nom == self.nom)

        if len(tournoi) == 0:
            return db.insert(self.to_dict())
        else:
            return db.update(self.to_dict_for_update(), query.nom == self.nom)

    def finish(self):
        """
        Méthode qui permet de terminer le tournoi.
        """
        self.date_de_fin = get_timestamp()

    def to_dict(self):
        liste_joueurs_enregistres_dict = []
        for player in self.liste_joueurs_enregistres:
            # liste_joueurs_enregistres_dict.append(player.identifiant_national)
            liste_joueurs_enregistres_dict.append(player.to_dict_for_tournament())

        return {
            "nom": self.nom,
            "lieu": self.lieu,
            "date_de_debut": self.date_de_debut,
            "date_de_fin": self.date_de_fin,
            "nombre_de_tours": self.nombre_de_tours,
            "numero_de_tour": self.numero_de_tour,
            "liste_des_tours": self.liste_des_tours,
            "liste_joueurs_enregistres": liste_joueurs_enregistres_dict,
            "descritpion_remarque": self.descritpion_remarque,
        }

    def to_dict_for_update(self):
        liste_joueurs_enregistres_dict = []
        for player in self.liste_joueurs_enregistres:
            liste_joueurs_enregistres_dict.append(player.to_dict_for_tournament())

        liste_round_dict = []
        for round in self.liste_des_tours:
            liste_round_dict.append(round.to_dict())

        return {
            "date_de_fin": self.date_de_fin,
            "numero_de_tour": self.numero_de_tour,
            "liste_des_tours": liste_round_dict,
            "liste_joueurs_enregistres": liste_joueurs_enregistres_dict,
        }

    def __str__(self):
        return self.nom


def load_tournement_all_tournament(only_not_finish=False):
    # On recupere les données du tournoi "name" dans tinyDB
    db = TinyDB(PATH, indent=4)
    if only_not_finish:
        x = [
            item
            for item in db.all()
            if item["nombre_de_tours"] != item["numero_de_tour"]
        ]
    else:
        x = db.all()

    list_tournois = []
    for tournoi in x:
        list_tournois.append(dict_to_tournament(tournoi))
    return list_tournois


def load_tournament(name):
    # On recupere les données du tournoi "name" dans tinyDB
    db = TinyDB(PATH, indent=4)
    tournoi_query = Query()
    # je recupère tous les tournois qui correspond à la condition.
    x = db.search(tournoi_query.nom == name)
    # on verifie que l'on recupère qu'un seul tournois donnée.

    if len(x) == 1:
        return dict_to_tournament(x[0])
    return None


def dict_to_tournament(dict_tournament):
    listPlayer = []
    for player in dict_tournament["liste_joueurs_enregistres"]:
        inst_player = getPlayerFromID(
            player["identifiant_national"],
            player["scoretournois"] if "scoretournois" in player else 0,
        )
        listPlayer.append(inst_player)

    liste_des_tours = []
    for round in dict_tournament["liste_des_tours"]:
        list_match = []
        for match in round["liste_match"]:
            instance_match = MatchModel(
                getPlayerFromID(match[PLAYER_1][0]),
                getPlayerFromID(match[PLAYER_2][0]),
                match[PLAYER_1][1],
                match[PLAYER_2][1],
            )
            list_match.append(instance_match)
        liste_des_tours.append(
            RoundModel(
                round["nom"], list_match, round["date_de_debut"], round["date_de_fin"]
            )
        )
    tournament = TournamentModel(
        dict_tournament["nom"],
        dict_tournament["lieu"],
        dict_tournament["date_de_debut"],
        dict_tournament["nombre_de_tours"],
        dict_tournament["numero_de_tour"],
        liste_des_tours,
        listPlayer,
        dict_tournament["descritpion_remarque"],
    )

    tournament.date_de_fin = dict_tournament["date_de_fin"]
    return tournament
