import re
import os
from datetime import datetime
from models.player_model import getPlayerFromID 


class View:
    def affichage_menu(self, titre, choix, donnees_valide):
        selection_option = None
        while selection_option not in donnees_valide:
            if selection_option is not None:
                print("\nIl y a une erreur dans la saisie\n")

            print(titre)
            for valeur in choix:
                print(valeur)
            selection_option = input(
                "\n\033[96mSelectionnez une option parmi les propositions ci-dessus : \033[0m"
            )
            os.system("clear")
        return selection_option

    def input_int(self, texte, defaut_value=None):
        while True:
            saisie = input(texte)
            if not saisie:
                if defaut_value is not None:
                    if isinstance(defaut_value, int) and defaut_value >= 0:
                        return defaut_value
                    else:
                        print("\n\033[91mValeur par défaut invalide.\033[0m\n")
                else:
                    print("\n\033[91mVeuillez entrer un nombre\033[0m\n")
            elif saisie.isnumeric() and int(saisie) >= 0:
                return int(saisie)
            else:
                print("\n\033[91mVeuillez entrer un nombre valide\033[0m\n")

    def input_str(self, texte):
        while True:
            saisie = input(texte)
            if saisie.isalpha():
                return saisie
            else:
                print("\n\033[91mSeules les lettres sont acceptées\033[0m\n")

    def city_input(self, texte): 
        while True: 
            saisie = input(texte)
            reg = r'^[a-zA-Z\s-]+$'
            if (bool(re.match(reg, saisie))): 
                return saisie
            else: 
                print("\n\033[91mSeules les lettres, les espaces et les traits d'union sont acceptés \033[0m\n")

    def input_id(self, texte):
        while True:
            saisie = input(texte)
            if not re.match("^[a-zA-Z]{2}[0-9]{5}$", saisie):
                print("\n\033[91mL'identifiant national n'est pas au bon format, veuillez réessayer (format : AA12345)\033[0m\n")
            elif getPlayerFromID(saisie.upper()):
                print("\n\033[91mCet identifiant national est déjà utilisé\033[0m\n")
            else: 
                return saisie.upper()

    def input_date(self, texte):
        while True:
            date_saisie = input(texte)
            try:
                date = datetime.strptime(date_saisie, "%m/%d/%Y")
                if date > datetime.now(): 
                    print("\n\033[91mLa date ne peut pas être dans le futur, veuillez entrer une date valide.\033[0m\n")
                    continue
                return date_saisie
            except ValueError:
                print(
                    "\n\033[91mDate de naissance invalide, veuillez entrer une date au format MM/JJ/AAAA.\033[0m\n"
                )

    def select_many_in_list(self, listdata, nb, name_element):
        if len(listdata) == 0:
            return []

        id_selected = []  
        liste_elem_enregistres = []  
        while len(id_selected) < nb:
            print("====================================")
            for idx, elem in enumerate(listdata):
                if idx not in id_selected:
                    print(f"[{idx+1}]", elem)
            
            elem_id_select = self.input_int(
                f"\nVous devez sélectionner encore {nb - len(id_selected)} joueur{'s' if nb - len(id_selected) > 1 else ''} : \n"
            )
            os.system("clear")
            elem_id_select -= 1

            if elem_id_select < 0 or elem_id_select >= len(listdata): 
                print(f"\n\033[91mLe joueur choisi n'existe pas. Veuillez sélectionner un joueur valide.\033[0m\n")
            elif elem_id_select in id_selected: 
                player_id = listdata[elem_id_select].identifiant_national
                print(f"\n\033[91mLe joueur avec l'identiant national \033[93m{player_id} \033[91ma déjà été sélectionné. \nVeuillez en sélectionner un autre.\033[0m\n")
            else:
                player_id = listdata[elem_id_select].identifiant_national
                liste_elem_enregistres.append(listdata[elem_id_select])
                id_selected.append(elem_id_select)

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
                print("\n\033[91mVeuillez choisir une option valide.\033[0m\n")
