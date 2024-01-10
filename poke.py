import json
import random

class Pokemon():
    def __init__(self, nom, sexe, niv, hp, atk, defense, atk_spe, def_spe, vit, liste_atk, num_pokedex="", nature = "", type = "") :
        self.nom = nom
        if num_pokedex == "" :
            self.num_pokedex = self.NumPokedex()
        if type == "" :
            self.l_type = self.Type_()
            if len(self.l_type) == 2 :
                self.type = self.l_type[0]
                self.type2 = self.l_type[1]
            else :
                self.type = self.l_type[0]
        self.sexe = sexe
        self.niv = niv
        self.list_nature = [
                        "Hardi",
                        "Solo",
                        "Rigide",
                        "Mauvais",
                        "Brave",
                        "Assuré",
                        "Docile",
                        "Malin",
                        "Lâche",
                        "Relax",
                        "Modeste",
                        "Doux",
                        "Pudique",
                        "Discret",
                        "Sérieux",
                        "Calme",
                        "Gentil",
                        "Prudent",
                        "Bizarre",
                        "Foufou",
                        "Timide",
                        "Pressé",
                        "Jovial",
                        "Naïf",
                        "Malpoli"
                        ]
        if nature == "" :
            self.nature = self.Nature()
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.atk_spe = atk_spe
        self.def_spe = def_spe
        self.vit = vit
        self.liste_atk = liste_atk
        self.weak, self.res, self.immune = self.OpenJson()
        self.pkm_faiblesse, self.pkm_double, self.pkm_resistance, self.pkm_double_res, self.pkm_immune = self.FoundWeakness()
    
    def NumPokedex(self) :
        #j'ouvre un fichier JSON. si je trouve le nom du pokemon il me retourne son numero associe.
        with open("pokedex.json", "r") as pokedex :
            file = json.load(pokedex)
        for pokemons in file:
            for num, infos in pokemons.items() :
                for noms in infos[0] :
                    if self.nom == noms :
                        numero = num
        return numero
    
    
    def Type_(self) :
        #j'ouvre un fichier JSON. si je trouve le numero du pokemon dans le pokedex, il me retourne son type.
        with open("pokedex.json", "r") as pokedex :
            file = json.load(pokedex)
        for pokemons in file:
            for num, infos in pokemons.items() :
                if self.num_pokedex == num : 
                    t = infos[1]
        return t

########################################### GERER FAIBLESSES DU POKEMON ###########################################
   
    def OpenJson(self) :
        # J'ouvre 3 fichiers afin de les affectes a des attributs de mon constructeurs
        with open("weak.json", "r") as weak_ :
            weak = json.load(weak_)
        with open("res.json", "r") as res_ :
            res = json.load(res_) 
        with open("immune.json", "r") as immune_ :
            immune = json.load(immune_) 
        return weak, res, immune
                
    
    def FoundWeakness(self) :
        # La fonction me permet de retourner une liste specifique pour mon Pokemon : Faiblesses, Resistances, Immunité.
        
        # Je cree des listes vides afin de les utiliser pour la suite. 
        liste_weak = []
        double = []
        liste_res = []
        double_res = []
        liste_immune = []
        # Si j'ai un pokemon avec 2 types :
        if len(self.l_type) == 2 :
            # J'appelle ma fonction Weak_Res en recursivité, l'une pour les faiblesses et l'autre pour les résistances.
            liste_weak, double = self.Weak_Res(self.weak, liste_weak, double)
            liste_res, double_res = self.Weak_Res(self.res, liste_res, double_res)
            
            # J'ai remarqué qu'il fallait vérifier ma tables de types sinon cette derniere n'etait pas juste. 
            #Celle qui est checké par le for doit etre la plus longue ce qui n'est pas forcement le cas pour tous. 
            # Donc une checkup dans lautre sens est nécéssaire.
            liste_res, liste_weak = self.UpdateTypes(liste_res, liste_weak)
            liste_weak, liste_res = self.UpdateTypes(liste_weak, liste_res)
        
            # Si un pokemon possede une imunité il doit lui etre retourné.
            liste_immune = self.Immunise(liste_immune)          
            
        # Si j'ai 1 type :                           
        else :
            # Voir fonction Weak_Res....
            for types in self.weak :
                if self.type in types :
                    for x in types[self.type] :
                        liste_weak.append(x)
            for types in self.res :
                if self.type in types :
                    for x in types[self.type] :
                        liste_res.append(x)
            liste_immune = self.Immunise(liste_immune)      
                        
        return liste_weak, double, liste_res, double_res, liste_immune
                
    def Weak_Res(self, weak_res, liste, double) :
        # Je recupere les deux listes dont j'ai besoin : La liste des Faiblesses normales(x2) et la liste des Doubles Faiblesses(x4)
            # /!\ A noter qu'il s'agira du meme processus pour les Resistances.
        
            
            # Pour chaque Dictionaire dans ma liste des faiblesses normales : 
            for lt in weak_res :
                # Si le type est dans le Dictionnaire :
                if self.type in lt :
                    # Alors pour chaque éléments dans la valeur de mon dictionnaire ayant pour clé Le type(Puisqui'il existe bel et bien) :
                    for x in lt[self.type] :
                        # Il me l'ajoute dans ma liste.
                        liste.append(x)
            # Je reitere pour le deuxieme type....            
            for lt in weak_res :
                if self.type2 in lt :
                    for y in lt[self.type2] :
                        #... Seulement, si les éléments sont deja dans la liste alors il ira vers la liste des doubles faiblesses et 
                        #le suprimera du précédent.
                        if y in liste :
                            double.append(y)
                            liste.remove(y)
                        # Sinon il me l'ajoute.
                        else :
                            liste.append(y)            
            return liste, double
        
    def Immunise(self, liste) :
        # Pour chaque Dictionaire(D) dans ma liste
        for i in self.immune :
            # Pour chaque Clé et Valeur dans ce D :
            for k,v in i.items() :
                # Si j'ai deux types :
                if len(self.l_type) == 2 :
                    # Je check si un des deux types se trouve en cle dans self.immune et si c'est le cas il me l'ajoute dans la liste des imunitées
                    if self.type == k or self.type2 == k:
                        for j in v :
                            liste.append(j)
                # Sinon si j'ai un seul type   :         
                else : 
                    print(self.type)
                    print(k)
                    if self.type == k :
                        print("Un des deux types a", k)
                        for j in v :
                            liste.append(j)               
        return liste
    
    def UpdateTypes(self, liste_a, liste_b) :
        # Voir explication dans FoundWeakness
        for x in liste_a :
                if x in liste_b :
                    print(liste_b)
                    liste_b.remove(x)
                    liste_a.remove(x)
        return liste_a, liste_b

########################################### GERER FAIBLESSES DU POKEMON ###########################################


    def Nature(self) :
        # Choisis une nature aléatoire.
        random_nature = random.choice(self.list_nature)
        return random_nature
    
    def Stat(self) :
        # Stat permet d'avoir des statistiques uniques pour chaques Pokemons. La nature affectera ces dernières.
        if self.nature == "Solo":
            self.atk += int((self.atk*10)/100)
            self.defense -= int((self.defense*10)/100)

        elif self.nature == "Rigide":
            self.atk += int((self.atk*10)/100)
            self.atk_spe -= int((self.atk_spe*10)/100)

        elif self.nature == "Mauvais":
            self.atk += int((self.atk*10)/100)
            self.def_spe -= int((self.def_spe*10)/100)
            
        elif self.nature == "Brave" :
            self.atk += int((self.atk*10)/100)
            self.vit -= int((self.vit*10)/100)

        elif self.nature == "Assuré":
            self.atk -= int((self.atk*10)/100)
            self.defense += int((self.defense*10)/100)

        elif self.nature == "Malin":
            self.defense += int((self.defense*10)/100)
            self.atk_spe -= int((self.atk_spe*10)/100)

        elif self.nature == "Lâche":
            self.defense += int((self.defense*10)/100)
            self.def_spe -= int((self.def_spe*10)/100)

        elif self.nature == "Relax":
            self.defense += int((self.defense*10)/100)
            self.vit -= int((self.vit*10)/100)

        elif self.nature == "Modeste":
            self.atk_spe += int((self.atk_spe*10)/100)
            self.atk -= int((self.atk*10)/100)

        elif self.nature == "Doux":
            self.atk_spe += int((self.atk_spe*10)/100)
            self.defense -= int((self.defense*10)/100)

        elif self.nature == "Discret":
            self.atk_spe += int((self.atk_spe*10)/100)
            self.vit -= int((self.vit*10)/100)
            
        elif self.nature == "Calme":
            self.def_spe += int((self.def_spe*10)/100)
            self.atk += int((self.atk*10)/100)
        
        elif self.nature == "Malpoli" :
            self.def_spe += int((self.def_spe*10)/100)  
            self.vit -= int((self.vit*10)/100)

        elif self.nature == "Gentil":
            self.def_spe += int((self.def_spe*10)/100)
            self.defense -= int((self.defense*10)/100)

        elif self.nature == "Prudent":
            self.def_spe += int((self.def_spe*10)/100)
            self.atk_spe -= int((self.atk_spe*10)/100)

        elif self.nature == "Foufou":
            self.atk_spe += int((self.atk_spe*10)/100)
            self.def_spe -= int((self.def_spe*10)/100)
        
        elif self.nature == "Timide" :
            self.vit += int((self.vit*10)/100)
            self.atk -= int((self.atk*10)/100)

        elif self.nature == "Pressé":
            self.vit += int((self.vit*10)/100)
            self.defense -= int((self.defense*10)/100)

        elif self.nature == "Jovial":
            self.vit += int((self.vit*10)/100)
            self.atk_spe -= int((self.atk_spe*10)/100)

        elif self.nature == "Naïf":
            self.vit += int((self.vit*10)/100)
            self.def_spe -= int((self.def_spe*10)/100)
    
    def AfficherStats(self):
        if len(self.l_type) != 2 :
            print(f"N°{self.num_pokedex} Pokemon : {self.nom}\nType : {self.type}\nNature : {self.nature}\nFaiblesse x2 : {self.pkm_faiblesse}")
            print(f"Resistance 1/2 : {self.pkm_resistance}\nResistance 1/4 : {self.pkm_double_res}\nImmunisé à : {self.pkm_immune}")
        else :
            print(f"N°{self.num_pokedex} Pokemon : {self.nom}\nType : {self.type}, {self.type2}\nNature : {self.nature}\nFaiblesse x2 : {self.pkm_faiblesse}\nFaiblesse x4 : {self.pkm_double}")
            print(f"Resistance 1/2 : {self.pkm_resistance}\nResistance 1/4 : {self.pkm_double_res}\nImmunisé à : {self.pkm_immune}")
        print(f"PV : {self.hp}\nAtk : {self.atk}\nDef : {self.defense}\nAtk Spé : {self.atk_spe}\nDef Spé : {self.def_spe}\nVitesse : {self.vit}")

    
    
    
class Combat():
    def __init__(self, type, puissance, taux_crit, precision, categorie):
        self.type = type
        self.puissance = puissance
        self.taux_crit = taux_crit
        self.precision = precision
        self.categorie = categorie
        
    def CalculDegat(self) :
        # Verifie la precision, si precision est true on passe a la verification suivante sinon renvoie atk echouer
        # Lorsque atk, verifie la categorie et en fonction effectue le calcule de dommage.
        # Lors du calcule de dommage verifie si taux crit si c'est le cas effectue le double des degats 
        # Et si le type de l'attaque et efficace ou non mettre a jour les degat
        pass


# (nom, sexe, niv, hp, atk, defense, atk_spe, def_spe, vit, liste_atk, num_pokedex="", nature = "", type = "")       
nompk = input("Nom pokemon\n").capitalize()
test = Pokemon(nompk,"male",50,76,110,70,81,70,123,0)
test.Stat()
test.AfficherStats()



########## Faire heriter Pokemon a 54 classes enfants et y gerer leurs faiblesses et resistances ?? ##############