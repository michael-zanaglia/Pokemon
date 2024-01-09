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
    
    def Nature(self) :
        # Choisis une nature aléatoire.
        random_nature = random.choice(self.list_nature)
        return random_nature
    
    def Stat(self) :
        # Stat permet d'avoir des statistique unique pour chaque pokemon. La nature affectera ces dernières.
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
            print(f"N°{self.num_pokedex} Pokemon : {self.nom}\nType : {self.type}\nNature : {self.nature}")
        else :
            print(f"N°{self.num_pokedex} Pokemon : {self.nom}\nType : {self.type}, {self.type2}\nNature : {self.nature}")
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
test = Pokemon("Miascarade","male",50,76,110,70,81,70,123,0)
test.Stat()
test.AfficherStats()


########## Faire heriter Pokemon a 54 classes enfants et y gerer leurs faiblesses et resistances ?? ##############