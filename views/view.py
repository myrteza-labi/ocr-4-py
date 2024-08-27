import re
from datetime import datetime


class View:
    def affichage_menu(self, titre, choix, donnees_valide):
        selection_option = None
        while selection_option not in donnees_valide:
            if selection_option is not None:
                print("Il y a une erreur dans la saisie")

            print(titre)
            for valeur in choix:
                print(valeur)
            selection_option = input(
                "Selectionnez une option parmi les propositions suivantes : "
            )
        return selection_option

    def input_int(self, texte, defaut_value=None):
        while True:
            saisie = input(texte)
            if not saisie:
                if defaut_value is not None:
                    if isinstance(defaut_value, int) and defaut_value >= 0:
                        return defaut_value
                    else:
                        print("Valeur par défaut invalide.")
                else:
                    print("Erreur de saisie : veuillez entrer un nombre.")
            elif saisie.isnumeric() and int(saisie) >= 0:
                return int(saisie)
            else:
                print("Erreur de saisie : Veuillez entrer un nombre valide.")

    def input_str(self, texte):
        while True:
            saisie = input(texte)
            if saisie.isalpha():
                return saisie
            else:
                print("Erreur de saisie : veuillez entrer uniquement des lettres.")

    def input_id(self, texte):
        while True:
            saisie = input(texte)
            if re.match("^[a-zA-Z]{2}[0-9]{5}$", saisie):
                return saisie.upper()
            else:
                print("\nErreur de saisie, merci de recommencer.\n")

    def input_date(self, texte):
        while True:
            saisie = input(texte)
            try:
                datetime.strptime(saisie, "%m/%d/%Y")  # Format MM/JJ/AAAA
                return saisie
            except ValueError:
                print(
                    "Date de naissance invalide, veuillez entrer une date au format MM/JJ/AAAA."
                )

    def select_many_in_list(self, listdata, nb, name_element):
        if len(listdata) == 0:
            return []

        id_selected = []  # Liste des ids sélectionnés
        liste_elem_enregistres = []  # Liste des éléments sélectionnés
        while len(id_selected) < nb:
            print("====================================")
            for idx, elem in enumerate(listdata):
                if idx not in id_selected:
                    print(f"[{idx+1}]", elem)
            elem_id_select = self.input_int(
                f"Selectionner ... (encore {nb - len(id_selected)} {name_element} à sélectionner): "
            )
            elem_id_select -= 1
            if (
                0 <= elem_id_select < len(listdata)
                and elem_id_select not in id_selected
            ):
                liste_elem_enregistres.append(listdata[elem_id_select])
                id_selected.append(elem_id_select)
            else:
                print("Erreur de sélection, veuillez choisir un numéro valide.")
        return liste_elem_enregistres

    def select_one_in_list(self, listdata, name_element):
        if len(listdata) == 0:
            return None
        while True:
            for idx, elem in enumerate(listdata):
                print(f"[{idx+1}]", elem)
            elem_id_select = self.input_int(f"Selectionner un {name_element}: ")
            elem_id_select -= 1
            if 0 <= elem_id_select < len(listdata):
                return listdata[elem_id_select]
            else:
                print("Erreur de sélection, veuillez choisir un numéro valide.")
