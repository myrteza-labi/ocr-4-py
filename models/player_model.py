from tinydb import TinyDB, Query

PATH = "datas/player.json"


class PlayerModel:
    def __init__(
        self,
        nom,
        prenom,
        date_de_naissance,
        identifiant_national,
        couleur=None,
        scoreglobal=0,
        scoretournois=0,
    ):
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.identifiant_national = identifiant_national
        self.couleur = couleur
        self.scoreglobal = scoreglobal
        self.scoretournois = scoretournois

    @staticmethod
    def get_all_player_from_db():
        players_db = TinyDB(PATH, indent=4)
        players_db.all()
        players = []
        for item in players_db:
            player = PlayerModel(
                item["nom"],
                item["prenom"],
                item["date_de_naissance"],
                item["identifiant_national"],
                item["couleur"] if "couleur" in item else None,
                item["scoreglobal"] if "scoreglobal" in item else 0,
                item["scoretournois"] if "scoretournois" in item else 0,
            )
            players.append(player)
        players_db.close()

        return players

    @staticmethod
    def add_point_to_player(nationnal_id, point):
        players_db = TinyDB(PATH, indent=4)
        query = Query()
        player = players_db.search(query.identifiant_national == nationnal_id)

        current_score = 0
        if len(player) == 1 and "score" in player[0]:
            current_score = int(player[0]["score"])
        ret = players_db.update(
            {"score": current_score + point}, query.identifiant_national == nationnal_id
        )
        players_db.close()

        return ret

    @staticmethod
    def load_player(nationnal_id):
        players_db = TinyDB(PATH, indent=4)
        query = Query()
        ret = players_db.search(query.identifiant_national == nationnal_id)
        players_db.close()

        return ret

    def get_color_str(self):
        if not self.couleur:
            return "BLANC"
        return "NOIR"

    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "date_de_naissance": self.date_de_naissance,
            "identifiant_national": self.identifiant_national,
            "scoreglobal": self.scoreglobal,
        }

    def to_dict_for_tournament(self):
        return {
            "identifiant_national": self.identifiant_national,
            "scoretournois": self.scoretournois,
        }

    def to_dict_for_tour(self):
        return {
            "identifiant_national": self.identifiant_national,
            "couleur": self.couleur,
            "scoretournois": self.scoretournois,
        }

    def save(self):
        db = TinyDB(PATH, indent=4)
        query = Query()
        tournoi = db.search(query.identifiant_national == self.identifiant_national)

        if len(tournoi) == 0:
            ret = db.insert(self.to_dict())
        else:
            ret = db.update(self.to_dict(), query.nom == self.nom)
        db.close()

        return ret

    def __str__(self):
        return (
            f"{self.nom} {self.prenom} {self.date_de_naissance} {self.identifiant_national}"
            f" {self.scoreglobal} {self.scoretournois}"
        )

    def __repr__(self):
        return (
            f"{self.nom} {self.prenom} {self.date_de_naissance} {self.identifiant_national} "
            f"{self.scoreglobal} {self.scoretournois}"
        )


def getPlayerFromID(idnational, scoretournois=0):
    players_db = TinyDB(PATH, indent=4)
    query = Query()
    player_dict = players_db.search(query.identifiant_national == idnational)
    if player_dict:
        return PlayerModel(
            player_dict[0]["nom"],
            player_dict[0]["prenom"],
            player_dict[0]["date_de_naissance"],
            player_dict[0]["identifiant_national"],
            player_dict[0]["scoreglobal"] if "scoreglobal" in player_dict[0] else 0,
            scoretournois,
        )
    return None
