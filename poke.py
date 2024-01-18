import json
import random
import pygame

class Pokemon():
    def __init__(self, nom, sexe, niv = 50, num_pokedex = "", nature = "", type = "") :
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
        # Si le pokemon a deja été utilisé il verifie et si c'est le cas je recupère les valeurs avant qu'il soit echangé.
        
        if self.nom in team.used :
            self.nature = nature
            self.hp, self.atk, self.defense, self.atk_spe, self.def_spe, self.vit = 0, 0, 0, 0, 0, 0
            self.statut, self.alteration, self.count_brulure, self.count_poison = 0, 0, 0, 0
            self.nom, self.nature, self.hp, self.atk, self.defense, self.atk_spe, self.def_spe, self.vit, self.statut, self.alteration, self.count_brulure, self.count_poison = combat.Returned(self.nom, self.nature, self.hp, self.atk, self.defense, self.atk_spe, self.def_spe, self.vit, self.statut, self.alteration, self.count_brulure, self.count_poison)
        elif self.nom in team2.used :
            self.nature = nature
            self.hp, self.atk, self.defense, self.atk_spe, self.def_spe, self.vit = 0, 0, 0, 0, 0, 0
            self.statut, self.alteration, self.count_brulure, self.count_poison = 0, 0, 0, 0
            self.nom, self.nature, self.hp, self.atk, self.defense, self.atk_spe, self.def_spe, self.vit, self.statut, self.alteration, self.count_brulure, self.count_poison = combat.Returned(self.nom, self.nature, self.hp, self.atk, self.defense, self.atk_spe, self.def_spe, self.vit, self.statut, self.alteration, self.count_brulure, self.count_poison)
        else :
            # Si ce n'est pas le cas j'instancie la classe avec les attributs importantes
            if nature == "" :
                self.nature = self.Nature()
            self.hp, self.atk, self.defense, self.atk_spe, self.def_spe, self.vit = self.GetPkmStat()
            self.statut = ""
            self.alteration = False
            self.count_brulure = 0
            self.count_poison = 0
            
        self.liste_atk = self.ListeAttaques()
        self.weak, self.res, self.immune = self.OpenJson()
        self.pkm_faiblesse, self.pkm_double, self.pkm_resistance, self.pkm_double_res, self.pkm_immune = self.FoundWeakness()
        self.etat_ephemere = ""
        self.counting_bluff = 0
        self.combat = False
    
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

    def ListeAttaques(self) :
        l = []
        with open("atk_pokemon.json", "r") as pokedex :
            file = json.load(pokedex)
        for pokemons in file:
            for name, attaques in pokemons.items() : 
                if self.nom == name :
                    for index in range(0,4) :
                        l.append(attaques[index])
        return l
        
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
            for x in liste_weak :
                if x in liste_immune :
                    liste_weak.remove(x)
                    
            
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
                    if self.type == k :
                        for j in v :
                            liste.append(j)               
        return liste
    
    def UpdateTypes(self, liste_a, liste_b) :
        # Voir explication dans FoundWeakness
        for x in liste_a :
                if x in liste_b :
                    liste_b.remove(x)
                    liste_a.remove(x)
        return liste_a, liste_b

########################################### GERER FAIBLESSES DU POKEMON ###########################################


########################################### GERER STATISTIQUES DU POKEMON ###########################################

    def GetPkmStat(self) :
        with open("statistic.json", "r") as stat :
            file = json.load(stat)
        for pokemons in file :
            for k,v in pokemons.items() :
                if self.nom == k :
                    hp = int(int(v[0]))
                    atk = int(v[1])
                    defe = int(v[2])
                    atk_spe = int(v[3])
                    def_spe = int(v[4])
                    vit = int(v[5])
        return hp, atk, defe, atk_spe, def_spe, vit


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
            
########################################### GERER STATISTIQUES DU POKEMON ###########################################
    
    def AfficherStats(self):
        if len(self.l_type) != 2 :
            print(f"N°{self.num_pokedex} Pokemon : {self.nom}\nType : {self.type}\nNature : {self.nature}\nFaiblesse x2 : {self.pkm_faiblesse}")
            print(f"Resistance 1/2 : {self.pkm_resistance}\nResistance 1/4 : {self.pkm_double_res}\nImmunisé à : {self.pkm_immune}")
        else :
            print(f"N°{self.num_pokedex} Pokemon : {self.nom}\nType : {self.type}, {self.type2}\nNature : {self.nature}\nFaiblesse x2 : {self.pkm_faiblesse}\nFaiblesse x4 : {self.pkm_double}")
            print(f"Resistance 1/2 : {self.pkm_resistance}\nResistance 1/4 : {self.pkm_double_res}\nImmunisé à : {self.pkm_immune}")
        print(f"PV : {self.hp}\nAtk : {self.atk}\nDef : {self.defense}\nAtk Spé : {self.atk_spe}\nDef Spé : {self.def_spe}\nVitesse : {self.vit}\n")
        for number in range(0,4) :
            print(f"Attaque {number+1} : {self.liste_atk[number]}")
    
    
    
class Attaque():
    def __init__(self, nom, puissance, precision, type, categorie, priorite, effect, pkm1, pkm2, turn):
        self.nom = nom
        self.type = type
        self.puissance = puissance
        self.precision = precision
        self.categorie = categorie
        self.priorite = priorite
        self.effect = effect
        self.my_pkm = pkm1
        self.pkm_foe = pkm2
        self.stock = 0 
        self.count_para = 0
        self.turn = turn
        self.fail = False
        
        
########################################### EFFETS GLOBALS ###########################################

        ### STATUS EFFECT ###
    def GetStatutChance(self, status) :
        liste = []
        for x in range(0,101):
            liste.append(x)
        choice = random.choice(liste)
        if self.pkm_foe.alteration == False or self.pkm_foe.alteration != "PSN" or self.pkm_foe.alteration != "BRU" :
            if choice < 10 :
                if status == "GEL" and status != "SLP" :
                    print(f"{self.pkm_foe.nom} est gelé.")
                    self.GelEffect(self.pkm_foe)
            elif choice <= 20 :
                if status == "PSN" and status != "SLP" :
                    print(f"{self.pkm_foe.nom} est empoisonné.")
                    self.PoisonedEffect(self.pkm_foe)
                elif status == "BRU" and status != "SLP" :
                    print(f"{self.pkm_foe.nom} est brulé.")
                    self.BruleEffect(self.pkm_foe)
                elif status == "PAR" and status != "SLP" :
                    print(f"{self.pkm_foe.nom} est paralysé.")
                    self.ParalysedEffect(self.pkm_foe)
            else :
                print("Pas d'effet ce coup ci !")
        else :
            print("Deja un statut")
    
    def PoisonedEffect(self, cible) :
        # Chaque fin de tour code partiellement fait
        if cible.hp != 0 :
            #cible.alteration = "PSN"
            if cible.count_poison == 0 :
                cible.hp -= int((cible.hp*10)/100)
                cible.statut = "PSN"
            elif cible.count_poison == 1 :
                cible.hp -= int((cible.hp*12)/100)
            elif cible.count_poison >= 2 :
                dgt = int((cible.hp*16)/100)
                if dgt <  1 :
                    dgt = 1
                cible.hp -= int((cible.hp*16)/100)
                
                
    def BruleEffect(self, cible) :
        # Chaque fin de tour code partiellement fait
        self.stock = cible.atk
        if cible.hp != 0 :
            cible.atk -= int((cible.atk*20)/100)       
        cible.statut = "BRU"
    
    def ParalysedEffect(self, cible) :
        liste_play = [1,2,3]
        liste_time = [1,2,3,4,5,6]
        paralyzed = True
        if paralyzed :
            if self.count_para == 0 :
                self.stock = cible.vit
                cible.vit = int(cible.vit/3)
            self.count_para = 1
            choice_play = random.choice(liste_play)
            if choice_play <= 3 :
                # Message pour dire que le pokemon n'a pas pu attaquer
                print(f"{cible.nom} est paralysé. Il n'a pas pu attaquer.")
                cible.alteration = True
                cible.statut = "PAR"
            choice_time = random.choice(liste_time)
            if choice_time >= 5 :
                print(f"{cible.nom} n'est plus paralysé.")
                paralyzed = not paralyzed
                cible.vit = self.stock
                cible.alteration = False
                cible.statut = ""
                
    def SleepEffect(self, cible) :
        liste_play = [1,2,3,4,5,6,7,8,9,10]
        spleeping = True
        if spleeping :
            choice_play = random.choice(liste_play)
            if choice_play < 9 :
                    print(f"{cible.nom} est endromie")
                    cible.alteration = True
                    cible.statut = "SLP"
            else :
                print(f"{cible.nom} n'est plus endromie")
                spleeping = not spleeping
                cible.alteration = False
                cible.statut = ""
                
    def GelEffect(self, cible) :
            liste_play = [1,2,3]
            liste_time = [1,2,3,4,5,6]
            gel = True
            if gel :
                choice_play = random.choice(liste_play)
                if choice_play in liste_play :
                    print(f"{cible.nom} est gelé.")
                    cible.alteration = True
                    cible.statut = "GEL"
            choice_time = random.choice(liste_time)
            if choice_time == 6 :
                print(f"{cible.nom} n'est plus gelé.")
                gel = not gel
                cible.alteration = False
                cible.statut = ""
        ### STATUS EFFECT ###
        
    
#/!\ Verifier si le heal rend plus que les pv max du pokemon, je dois renvoyer la valeur de base
    def HealAfterFightEffect(self, cible, dgt) :
        with open("statistic.json", "r") as stat :
            file = json.load(stat)
        for pokemons in file :
            for k,v in pokemons.items() :
                if cible.nom == k :
                    if cible.hp != int(v[0]) :
                        print(int(v[0]))
                        cible.hp += int(dgt / 2)
                        if cible.hp > int(v[0]) :
                            cible.hp = int(v[0])
    
    def HealEffect(self, cible) :
        with open("statistic.json", "r") as stat :
            file = json.load(stat)
        for pokemons in file :
            for k,v in pokemons.items() :
                if cible.nom == k :
                    if cible.hp != int(v[0]) :
                        cible.hp += int(int(v[0])*20) / 100
                        if cible.hp >= int(v[0]) :
                            cible.hp = int(v[0])
                        
    def AtterissageEffect(self, cible) :
        with open("statistic.json", "r") as stat :
            file = json.load(stat)
        for pokemons in file :
            for k,v in pokemons.items() :
                if cible.nom == k :
                    if cible.hp != int(v[0]) :
                        cible.hp += int(int(v[0])*50) / 100
                        if cible.hp > int(v[0]) :
                            cible.hp = int(v[0])
       
    def MutilerEffect(self, cible) :
        coup = int(cible.hp*35) / 100
        if coup < 1 :
            coup = 1
        cible.hp -= coup 
        if cible.hp < 1 :
            cible.hp = 0
                    
    def BoostDef(self, cible) :
        print(f"La défense de {cible.nom} augmente.")
        cible.defense = int(cible.defense*1.5)
        
    def BoostAtkSpe(self, cible) :
        print(f"L'attaque spéciale de la {cible.nom} augmente.")
        cible.atk_spe = int(cible.atk_spe*1.5)
    
    def ChanceBoostDef(self, cible) :
        liste = []
        for x in range(1,101) :
            liste.append(x)
        choice = random.choice(liste)
        if choice <= 35 :
            print(f"La defense de {cible.nom} augmente")
            cible.defense += int(cible.defense/2)
    
    def Peur(self, cible) :
        if self.nom != "Dark Lariat" or self.nom != "Vibrobscur" :
            cible.etat_ephemere = "PEUR"
        else :
            choose = random.randint(1,7) 
            if choose == 5 :
                cible.etat_ephemere = "PEUR"
                
    def Bluff(self, cible) :
        # Si c'est la premiere attaque elle est prioritaire et apeure l'ennemie. Marche qu'une fois.
        if self.my_pkm.counting_bluff == 0 :
            self.Peur(cible)
            self.my_pkm.counting_bluff = 1      
        
    def PauseEffect(self,cible) :
        cible.etat_ephemere = "PAUSE"
    
    def ChanceDiminuerDef(self, cible) :
        liste = []
        for x in range(1,101) :
            liste.append(x)
        choice = random.choice(liste)
        if cible.defense < 1 :
            print(f"La défense de {cible.nom} est déja très basse.")
        elif choice <= 20 :
            print(f"La défense de {cible.nom} baisse.")
            cible.defense -= int((cible.defense*25)/100)
            if cible.defense < 1 :
                cible.defense = 0
            
    def ChanceDiminuerDefSpe(self, cible) :
        liste = []
        for x in range(0,101) :
            liste.append(x)
        choice = random.choice(liste)
        if cible.def_spe < 1 :
            print(f"La défense spéciale de {cible.nom} est déja très basse.")
        elif choice <= 20 :
            print(f"La défense spéciale de {cible.nom} baisse.")
            cible.def_spe -= int((cible.def_spe*25)/100)
            if cible.def_spe < 1 :
                cible.def_spe = 0
            
    def ChanceDiminuerAtkSpe(self, cible) :
        liste = []
        for x in range(0,101) :
            liste.append(x)
        choice = random.choice(liste)
        if cible.atk_spe < 1 :
            print(f"L'attaque spéciale de {cible.nom} est déja très basse.")
        elif choice <= 20 :
            print(f"L'attaque spéciale de {cible.nom} baisse.")
            cible.atk_spe -= int((cible.atk_spe*25)/100)
            if cible.atk_spe < 1 :
                cible.atk_spe = 0
            
    def ChanceDiminuerAtk(self, cible) :
        liste = []
        for x in range(0,101) :
            liste.append(x)
        choice = random.choice(liste)
        if cible.atk < 1 :
            print(f"L'attaque spéciale de {cible.nom} est déja très basse.")
        elif choice <= 20 :
            print(f"L'attaque spéciale de {cible.nom} baisse.")
            cible.atk -= int((cible.atk*25)/100)
            if cible.atk < 1 :
                cible.atk = 0
    
    def BaisseLaDef_spe(self, cible) :
        print(f"La défense spéciale de {cible.nom} baisse.")
        cible.def_spe -= int((cible.def_spe*30)/100)
        if cible.def_spe < 1 :
            cible.def_spe = 0
    
    def BaisseLaDef(self, cible) :
        print(f"La défense de {cible.nom} baisse.")
        cible.defense -= int((cible.defense*30)/100)
        if cible.defense < 1 :
            cible.defense = 0
        
    def BaisseAtk(self, cible) :
        print(f"L'attaque de {cible.nom} baisse.")
        cible.atk -= int((cible.atk*30)/100)
        if cible.atk < 1 :
            cible.atk = 0
    
    def BaisseAtkSpe(self, cible) :
        print(f"L'attaque spéciale de {cible.nom} baisse.")
        cible.atk_spe -= int((cible.atk_spe*30)/100)
        if cible.atk_spe < 1 :
            cible.atk_spe = 0
        
    def Abri(self, cible):
        if cible.etat_ephemere == "" :
            print(cible.nom,"se protege.")
            cible.etat_ephemere = "ABRI"
        
    def ChangePkm(self, turn) :
        if turn == "player" :
            if pokemon1.nom in team.used :
                team.used.remove(pokemon1.nom)
            team.used.append(pokemon1.nom)
            while True :
                while True :
                    for x in team.l_pok :
                        print(team.l_pok.index(x)+1, x)
                    next_ = int(input("Qui choisissez vous ?"))
                    pokemon_switched = team.l_pok[next_-1]
                    if pokemon_switched != team.used[-1] and pokemon_switched not in team.liste_ko :
                        self.my_pkm = Pokemon(f'{pokemon_switched}', 'male')
                        break
                    else :
                        print("Envoi Impossible")
                
                if self.my_pkm.nom not in team.used :
                    self.my_pkm.Stat()
                if self.my_pkm.nom not in team.liste_ko :
                    with open("played.json", "r") as played :
                        try :
                            data = json.load(played)
                        except :
                            data = []
                    typo = {pokemon1.nom : [pokemon1.nature, pokemon1.hp, pokemon1.atk, pokemon1.defense, pokemon1.atk_spe, pokemon1.def_spe, pokemon1.vit, pokemon1.statut, pokemon1.alteration, pokemon1.count_brulure, pokemon1.count_poison]}
                    for x in data :
                        if typo.keys() == x.keys() :
                                data.remove(x)
                    data.append(typo)
                    with open("played.json", "w") as played :
                        json.dump(data, played, indent=4)
                    print(f"{pokemon_switched} est envoye au combat")
                    self.my_pkm.combat = True
                    team.EnCombat(self.my_pkm.nom)
                    return self.my_pkm
                
        else :
            # Gestion du changement de pokemon pour l'ordinateur
            if pokemon2.nom in team2.used :
                # Si le pokemon a par hasard été changé par l'ordinateur plusieurs fois, pour eviter un redondance dans la liste je supprime le nom. 
                team2.used.remove(pokemon2.nom)
            # Et ou sinon je l'ajoute.
            team2.used.append(pokemon2.nom)
            while True :
                # J'utilise for pour chercher un pokemon qi n'est non seulement pas K.O mais qu'il ne soit pas non plus le dernier avec lequel j'ai fait l'échange.
                for _ in range(0,11):
                    next_ = random.choice(team2.l_pok)
                    if next_ != team2.used[-1] and next not in team2.ko_bot:
                        break
                    elif team2.used == []:
                        break
                index = team2.l_pok.index(next_)
                # La typologie sous forme de dictionnaire avec les stats actuel du pokemon qui est retire du combat.
                typo = {pokemon2.nom : [pokemon2.nature, pokemon2.hp, pokemon2.atk, pokemon2.defense, pokemon2.atk_spe, pokemon2.def_spe, pokemon2.vit, pokemon2.statut, pokemon2.alteration, pokemon2.count_brulure, pokemon2.count_poison]}
                # J'instancie ma nouvelle classe
                self.my_pkm = Pokemon(f'{team2.l_pok[index]}', 'male') 
                # Si le pokemon existe deja pas besoin de verifier ses stats.
                if self.my_pkm.nom not in team2.used :
                    self.my_pkm.Stat()
                # S'il n'est pas dans la liste des K.O alors je mets typo dans mon fichier JSON et je supprime le precedent s'il y a redondance.
                if self.my_pkm.nom not in team2.ko_bot :
                    with open("played2.json", "r") as played2 :
                        try :
                            data = json.load(played2)
                        except :
                            data = []
                    for x in data :
                        if typo.keys() == x.keys() :
                            data.remove(x)
                    data.append(typo)
                    with open("played2.json", "w") as played2 :
                        json.dump(data, played2, indent=4)
                    print(f"{self.my_pkm.nom} est envoye au combat")
                    self.my_pkm.combat = True
                    team2.EnCombat(self.my_pkm.nom)
                    return self.my_pkm
                else :
                    continue
    
    def Colere(self, cible) :
        if cible.etat_ephemere == "" :
            cible.etat_ephemere = "ANGRY"
        elif cible.etat_ephemere == "ANGRY" :
            continued = random.randint(1,4)
            if continued == 4 :
                print("Sort de colere")
                cible.etat_ephemere = ""
    
    def Invincible(self, cible) :
        if cible.etat_ephemere == "" :
            cible.etat_ephemere = "DISPARU"
        else :
            cible.etat_ephemere = ""
    
    def Voltige(self, voltige, cible) :
        if not voltige :
            self.MutilerEffect(cible)
    
    def DmgWithDefStat(self, cible):
        self.stock = cible.atk
        cible.atk = cible.defense
        


    
    def CalculDegat(self) :
        # Verifie la precision, si precision est true on passe a la verification suivante sinon renvoie atk echouer
        # Lorsque atk, verifie la categorie et en fonction effectue le calcule de dommage.
        # Lors du calcule de dommage verifie si taux crit si c'est le cas effectue le double des degats 
        # Et si le type de l'attaque et efficace ou non mettre a jour les degat
        ## LA GESTION DE CALCUL DE DEGAT EST COMPLEXE. ELLE GERE BEAUCOUP DE CONDITION ET PARAMETRE
        test_precision = []
        echouer = False
        crit = []
        if self.my_pkm.hp != 0 and self.pkm_foe.hp != 0 :
            if self.my_pkm.statut == "GEL":
                self.GelEffect(self.my_pkm)
            elif self.my_pkm == "PAR" :
                self.ParalysedEffect(self.my_pkm)
            critprint = False
            for x in range(1,101) :
                test_precision.append(x)
            if self.nom != "Lame-Feuille" or self.nom != "Lame de Roc" :
                for y in range(1,25) :
                    crit.append(y)
            else : 
                for y in range(1,5) :
                    crit.append(y) 
            choice_crit = random.choice(crit)
            choice_tp = random.choice(test_precision)
            if self.my_pkm.etat_ephemere == "" or self.my_pkm.etat_ephemere == "DISPARU" or self.my_pkm.etat_ephemere == "ANGRY" or self.my_pkm.etat_ephemere == "ABRI": 
                if self.my_pkm.alteration == False or self.my_pkm.alteration == "PSN" or self.my_pkm.alteration == "BRU"  :
                    print(f"{self.my_pkm.nom} utilise {self.nom} !")
                    if choice_tp <= self.precision and self.pkm_foe.etat_ephemere != "DISPARU" :
                        voltige = True
                        if self.nom == "Big Splash" :
                            self.DmgWithDefStat(self.my_pkm)
                        if self.categorie == "Physique" :
                            dgt = self.my_pkm.niv*0.4+2*((self.puissance * self.my_pkm.atk) / (self.pkm_foe.defense * 50) + 2 )
                        elif self.categorie == "Spéciale" :
                            dgt = self.my_pkm.niv*0.4+2*((self.puissance * self.my_pkm.atk_spe) / (self.pkm_foe.def_spe * 50) + 2 )
                        else :
                            dgt = 0
                        if self.pkm_foe.statut != "" and self.categorie == "Statut" :
                            print("Votre attaque a echouer...") 
                            self.fail = True
                        elif self.categorie != "Statut" :
                            if self.nom == "Magie Florale" :
                                choice_crit = 1
                            if choice_crit == 1 :
                                dgt *= 1.95
                                critprint = True
                            if self.type in self.pkm_foe.pkm_faiblesse :
                                dgt *= 1.95
                                print("Super Efficace !")
                            elif self.type in self.pkm_foe.pkm_double :
                                dgt *= 3.9
                                print("Mega Efficace !")
                            elif self.type in self.pkm_foe.pkm_resistance :
                                dgt *= 0.5
                                print("Pas Efficace ...")
                            elif self.type in self.pkm_foe.pkm_double_res :
                                dgt *= 0.25
                                print("Tres Peu Efficace ...")
                            elif self.type in self.pkm_foe.pkm_immune :
                                dgt *= 0
                                print(f"{self.pkm_foe.nom} n'est pas affecté...")
                                self.fail = True
                            else :
                                dgt *= 1    
                            if critprint :
                                print("Coup Critique !")
                                critprint = False   
                        if self.pkm_foe.etat_ephemere == "ABRI" :  
                            print(f"{self.pkm_foe.nom} est protegé.")
                            echouer = True
                            self.fail = True
                            self.pkm_foe.etat_ephemere = ""
                        #if self.my_pkm.etat_ephemere == "ABRI" :
                            #self.my_pkm.etat_ephemere == ""
                        else : 
                            self.pkm_foe.hp -= int(dgt)
                        



                        if self.pkm_foe.hp < 1 :
                            self.pkm_foe.hp = 0
                        if self.nom == "Tunnel" and self.my_pkm.etat_ephemere == "" :
                                print("Le pokemon s'est cache sous la terre.")
                                self.pkm_foe.hp += int(dgt)
                        elif self.nom == "Tunnel" and self.my_pkm.etat_ephemere == "DISPARU" :
                            print(f"{self.my_pkm.nom} sort de terre et attaque {self.pkm_foe.nom} avec {self.nom} : {int(self.pkm_foe.hp)} restant apres l'attaque.")
                        else :
                            print(f"{self.my_pkm.nom} attaque {self.pkm_foe.nom} avec {self.nom} : {int(self.pkm_foe.hp)} restant apres l'attaque.")
                            if self.my_pkm.hp <= 0 :
                                print(f"{self.pkm_foe.nom} a gagné. {self.my_pkm.nom} est KO !")
                            elif self.pkm_foe.hp <= 0 :
                                print(f"{self.my_pkm.nom} a gagné. {self.pkm_foe.nom} est KO !")
                        self.VerifierEffect(dgt, echouer, voltige)
                        
                    else : 
                        voltige = False
                        if self.nom == "Pied Voltige" :
                            self.Voltige(voltige, self.my_pkm)
                        print(f"{self.my_pkm.nom} : Votre attaque a echoué (precision)")   
                        self.fail = True
                                  
                else :
                
                    print(f"{self.my_pkm.nom} : Votre attaque a echoué")  
                    self.fail = True
                    print(f"{self.pkm_foe.hp} restant apres l'attaque.")
                
            elif self.my_pkm.etat_ephemere == "PEUR" :
                print(f"{self.my_pkm.nom} a eu peur. Il n'a pas pu attaquer.")
                self.fail = True
                self.my_pkm.etat_ephemere = ""

            elif self.my_pkm.etat_ephemere == "PAUSE" :
                print(f"{self.my_pkm.nom} a lance une puissante attaque. Il doit prendre une pause.")
                self.my_pkm.etat_ephemere = ""
        
                
            
            print(f"Mon pokemon {self.my_pkm.nom} ===> {self.my_pkm.statut}")
            self.my_pkm.counting_bluff = 1
                                          
        if self.my_pkm.hp == 0 :
            self.my_pkm.statut = ""
            self.my_pkm.alteration = False
            self.my_pkm.count_poison = 0
            self.my_pkm.count_brulure = 0
        elif self.pkm_foe.hp == 0 :
            self.my_pkm.statut = ""
            self.pkm_foe.alteration = False
            self.pkm_foe.count_poison = 0
            self.pkm_foe.count_brulure = 0
        
        if self.nom == "Big Splash" :
            self.my_pkm.atk = self.stock
            
        
    
    def VerifierEffect(self, dgt, echouer, voltige) :
        if isinstance(self.effect, list):
            if not echouer :
                for effect in self.effect :
                    if effect == "GetStatutChance" :
                        if self.nom == "Bombe Beurk" or self.nom == "Direct Toxik" :
                            fonction = eval(f"self.{self.effect}")
                            fonction("PSN")
                        elif self.nom in ["Lance-Flammes", "Déflagration", "Ebullition", "Poing Feu", "Crocs Feu", "Ballon Brulant"] :
                            fonction = eval(f"self.{self.effect}")
                            fonction("BRU")
                        if self.nom in ["Tonnerre", "Electacle", "Poing Eclair", "Crocs Eclair"] and "Sol" not in self.pkm_foe.l_type :
                            fonction = eval(f"self.{self.effect}")
                            fonction("PAR")
                        elif "Sol" in self.pkm_foe.l_type :
                            print("Echouer, le pokemon est immunise")
                        if self.nom in ["Laser Glace", "Poing Glace", "Crocs Givre"] :
                            fonction = eval(f"self.{self.effect}")
                            fonction("GEL")
                    if effect == "SleepEffect" :
                        if self.nom == "Poudre Dodo" and "Plante" not in self.pkm_foe.l_type :
                            fonction = eval(f"self.{self.effect}")
                            fonction(self.pkm_foe)
                        elif "Plante" in self.pkm_foe.l_type :
                            print("Echouer, le pokemon est immunise")
                    if effect == "PoisonedEffect" :
                        if "Acier" not in self.pkm_foe.l_type :
                            fonction = eval(f"self.{self.effect}")
                            fonction(self.pkm_foe)
                        elif "Acier" in self.pkm_foe.l_type :
                            print("Echouer, le pokemon est immunise")
                    if effect == "HealAfterFightEffect" :
                                print(f"{self.my_pkm.nom} se heal")
                                self.HealAfterFightEffect(self.my_pkm, dgt)
                                print(f"{self.my_pkm.nom} recupert {int(dgt)} : hp {self.my_pkm.hp}")
                    elif effect == "HealEffect" :
                        print(f"{self.my_pkm.nom} se heal")
                        self.HealEffect(self.my_pkm)
                        print(f"{self.my_pkm.nom} recupert --->: hp {self.my_pkm.hp}")
                    elif effect == "AtterissageEffect" :
                        print(f"{self.my_pkm.nom} se heal")
                        self.AtterissageEffect(self.my_pkm)
                        print(f"{self.my_pkm.nom} recupert --->: hp {self.my_pkm.hp}")
                    if effect == "MutilerEffect" :
                        self.MutilerEffect(self.my_pkm)
                        print("Le contre-coup de l'attque la blesse")
                    if effect == "BoostDef" :
                        self.BoostDef(self.my_pkm)
                    if effect == "BoostAtkSpe" :
                        self.BoostAtkSpe(self.my_pkm)
                    if effect == "ChanceBoostDef" :
                        self.ChanceBoostDef(self.my_pkm)
                    if effect == "ChanceDiminuerDef" :
                        self.ChanceDiminuerDef(self.pkm_foe)
                    if effect == "ChanceDiminuerDefSpe" :
                        self.ChanceDiminuerDefSpe(self.pkm_foe)
                    if effect == "ChanceDiminuerAtkSpe" :
                        self.ChanceDiminuerAtkSpe(self.pkm_foe)
                    if effect == "ChanceDiminuerAtk" :
                        self.ChanceDiminuerAtk(self.pkm_foe)
                    if effect == "BaisseLaDef_spe" :
                        if self.nom != "Close Combat" :
                            self.BaisseLaDef_spe(self.pkm_foe)
                        else :
                            self.BaisseLaDef_spe(self.my_pkm)
                            
                    if effect == "BaisseLaDef" :
                        if self.nom not in ["Marteau Mastoc", "Close Combat", "Surpuissance"] :
                            self.BaisseLaDef(self.pkm_foe)
                        else :
                            self.BaisseLaDef(self.my_pkm)
                    if effect == "BaisseAtk" :
                        if self.nom not in ["Marteau Mastoc", "Surpuissance"] :
                            self.BaisseAtk(self.pkm_foe)
                        else :
                            self.BaisseAtk(self.my_pkm)
                    if effect == "BaisseAtkSpe" :
                        if self.nom != "Draco-Météore" :
                            self.BaisseAtkSpe(self.pkm_foe)
                        else :
                            self.BaisseAtkSpe(self.my_pkm)
                    if effect == "Peur" :
                        self.Peur(self.pkm_foe)
                    if effect == "Bluff" and "Spectre" not in self.pkm_foe.l_type :
                        self.Bluff(self.pkm_foe)
                    if effect == "PauseEffect" :
                        self.PauseEffect(self.my_pkm)
                    if effect == "Invincible" :
                        self.Invincible(self.my_pkm)
                    if effect == "Colere" :
                        self.Colere(self.my_pkm)
                    if effect == "Abri" :
                        self.Abri(self.my_pkm)
                    if effect == "Voltige" :
                        self.Voltige(voltige, self.my_pkm)
            
        elif self.effect != "None" :
            if not echouer : 
                if self.effect == "GetStatutChance" :
                    if self.nom == "Bombe Beurk" or self.nom == "Direct Toxik" :
                        fonction = eval(f"self.{self.effect}")
                        fonction("PSN")
                    elif self.nom in ["Lance-Flammes", "Déflagration", "Ebullition", "Poing Feu", "Crocs Feu", "Ballon Brulant"] :
                        fonction = eval(f"self.{self.effect}")
                        fonction("BRU")
                    if self.nom in ["Tonnerre", "Electacle", "Poing Eclair", "Crocs Eclair"] and "Sol" not in self.pkm_foe.l_type :
                        fonction = eval(f"self.{self.effect}")
                        fonction("PAR")
                    elif "Sol" in self.pkm_foe.l_type :
                        print("Echouer, le pokemon est immunise")
                    if self.nom in ["Laser Glace", "Poing Glace", "Crocs Givre"] :
                        fonction = eval(f"self.{self.effect}")
                        fonction("GEL")
                if self.effect == "SleepEffect" :
                    if self.nom == "Poudre Dodo" and "Plante" not in self.pkm_foe.l_type :
                        fonction = eval(f"self.{self.effect}")
                        fonction(self.pkm_foe)
                    elif "Plante" in self.pkm_foe.l_type :
                        print("Echouer, le pokemon est immunise")
                if self.effect == "PoisonedEffect" :
                    if "Acier" not in self.pkm_foe.l_type :
                        fonction = eval(f"self.{self.effect}")
                        fonction(self.pkm_foe)
                    elif "Acier" in self.pkm_foe.l_type :
                        print("Echouer, le pokemon est immunise")
                if self.effect == "HealAfterFightEffect" :
                            print(f"{self.my_pkm.nom} se heal")
                            self.HealAfterFightEffect(self.my_pkm, dgt)
                            print(f"{self.my_pkm.nom} recupert {int(dgt)} : hp {self.my_pkm.hp}")
                elif self.effect == "HealEffect" :
                    print(f"{self.my_pkm.nom} se heal")
                    self.HealEffect(self.my_pkm)
                    print(f"{self.my_pkm.nom} recupert --->: hp {self.my_pkm.hp}")
                elif self.effect == "AtterissageEffect" :
                    print(f"{self.my_pkm.nom} se heal")
                    self.AtterissageEffect(self.my_pkm)
                    print(f"{self.my_pkm.nom} recupert --->: hp {self.my_pkm.hp}")
                if self.effect == "MutilerEffect" :
                    self.MutilerEffect(self.my_pkm)
                    print("Le contre-coup de l'attque la blesse")
                if self.effect == "BoostDef" :
                    self.BoostDef(self.my_pkm)
                if self.effect == "BoostAtkSpe" :
                    self.BoostAtkSpe(self.my_pkm)
                if self.effect == "ChanceBoostDef" :
                    self.ChanceBoostDef(self.my_pkm)
                if self.effect == "ChanceDiminuerDef" :
                    self.ChanceDiminuerDef(self.pkm_foe)
                if self.effect == "ChanceDiminuerDefSpe" :
                    self.ChanceDiminuerDefSpe(self.pkm_foe)
                if self.effect == "ChanceDiminuerAtkSpe" :
                    self.ChanceDiminuerAtkSpe(self.pkm_foe)
                if self.effect == "ChanceDiminuerAtk" :
                    self.ChanceDiminuerAtk(self.pkm_foe)
                if self.effect == "BaisseLaDef_spe" :
                    if self.nom != "Close Combat" :
                        self.BaisseLaDef_spe(self.pkm_foe)
                    else :
                        self.BaisseLaDef_spe(self.my_pkm)
                        
                if self.effect == "BaisseLaDef" :
                    if self.nom not in ["Marteau Mastoc", "Close Combat", "Surpuissance"] :
                        self.BaisseLaDef(self.pkm_foe)
                    else :
                        self.BaisseLaDef(self.my_pkm)
                if self.effect == "BaisseAtk" :
                    if self.nom not in ["Marteau Mastoc", "Surpuissance"] :
                        self.BaisseAtk(self.pkm_foe)
                    else :
                        self.BaisseAtk(self.my_pkm)
                if self.effect == "BaisseAtkSpe" :
                    if self.nom != "Draco-Météore" :
                        self.BaisseAtkSpe(self.pkm_foe)
                    else :
                        self.BaisseAtkSpe(self.my_pkm)
                if self.effect == "Peur" :
                    self.Peur(self.pkm_foe)
                if self.effect == "Bluff" and "Spectre" not in self.pkm_foe.l_type :
                    self.Bluff(self.pkm_foe)
                if self.effect == "PauseEffect" :
                    self.PauseEffect(self.my_pkm)
                if self.effect == "Invincible" :
                    self.Invincible(self.my_pkm)
                if self.effect == "Colere" :
                    self.Colere(self.my_pkm)
                if self.effect == "Abri" :
                    self.Abri(self.my_pkm)
                if self.effect == "Voltige" :
                    self.Voltige(voltige, self.my_pkm)
                        
    def InfligerDgtFindeTour(self) :
        if self.my_pkm.statut != "" :
                if self.my_pkm.statut == "BRU" :
                    if self.my_pkm.hp != 0 :
                        subis = int((self.my_pkm.hp*7)/100)
                        if subis < 1 :
                            subis = 1 
                        self.my_pkm.hp -= subis
                        print(f"Inflige Brulure... HP restant : {self.my_pkm.hp}")
                self.my_pkm.count_brulure += 1 
                if self.my_pkm.statut == "PSN" and self.my_pkm.count_poison > 0 :
                    self.PoisonedEffect(self.my_pkm)
                    print(f"Inflige Poison sur {self.my_pkm.nom} ... HP restant {self.my_pkm.hp}:")      
                self.my_pkm.count_poison += 1  


class Combat():
# Gestion d'un combat entre deux pokemon
    # Ici j'ai besoin du nom de deux pokemon et je recupere leurs listes d'attaques
    def __init__(self, pkm1, pkm2, l_atk1, l_atk2):
        self.pkm1 = pkm1
        self.pkm2 = pkm2
        self.l_atk1 = l_atk1
        self.l_atk2 = l_atk2
        self.count = 0
        self.turn_me = True
        self.turn_bot = False
    
    # J'ouvre mon Fichier Json ou il y a les infos pour chaque attaques et je les renvois à la fonction qui prepare le combat
    def RecupererInfos(self, name):
        with open("infos_atk.json", "r") as ia :
            file = json.load(ia)
        for attaques in file :
            for k,v in attaques.items() :
                if name == k :
                    pu = v[0]
                    precision = v[1]
                    prio = v[2]
                    t = v[3]
                    cat = v[4]
                    eff = v[5]
        return pu, precision, prio, t, cat, eff
    
    def AttaqueJoueur(self) :
        while True :
            for atq in self.l_atk1 :
                print(f"{self.l_atk1.index(atq)+1}. {atq}")
            try :
                pos_atq = int(input("Choisissez votre attaque :"))
                myatk = self.l_atk1[pos_atq-1]
                break
            except :
                print("Entrez caractère valide")
        if self.pkm1.etat_ephemere == "DISPARU" :
            myatk = "Tunnel"
        elif self.pkm1.etat_ephemere == "ANGRY" :
            myatk = "Colère"
        puissance, precision, prio, type_, categorie, effect = self.RecupererInfos(myatk)
        # J'instancie l'attaque en fonction de celle recuperer
        attaque = Attaque(myatk, puissance, precision, type_, categorie, prio, effect, pokemon1, pokemon2, "player")
        return attaque
        
    
    
    def AttaqueBot(self) :  
        myatk2 = random.choice(self.l_atk2)
        if self.pkm2.etat_ephemere == "DISPARU" :
            myatk2 = "Tunnel"
        elif self.pkm2.etat_ephemere == "ANGRY" :
            myatk2 = "Colère"
        puissance, precision, prio, type_, categorie, effect = self.RecupererInfos(myatk2)
        # J'instancie l'attaque en fonction de celle recuperer
        attaque2 = Attaque(myatk2, puissance, precision, type_, categorie, prio, effect, pokemon2, pokemon1, "bot")  
        return attaque2
    
    #  Voila la fonction qui me retourne tous les attributs lorsque je joue de nouveau un pokemon qui n'est pas K.O  
    def Returned(self, nom, nature, hp, atk, defense, atkspe, defspe, vit, statut, alteration, brulure, poison) :
        if nom in team.used :
            with open("played.json", "r") as played :
                file = json.load(played)
            for data in file :
                for k,v in data.items():
                    if nom == k :
                        nature = v[0]
                        hp = v[1]
                        atk = v[2]
                        defense = v[3]
                        atkspe = v[4]
                        defspe = v[5]
                        vit = v[6]
                        statut = v[7]
                        alteration = v[8]
                        brulure = v[9]
                        poison = v[10]
            return nom, nature, hp, atk, defense, atkspe, defspe, vit, statut, alteration, brulure, poison
        elif nom in team2.used :
            with open("played2.json", "r") as played2 :
                file = json.load(played2)
            for data in file :
                for k,v in data.items():
                    if nom == k :   
                        nature = v[0]
                        hp = v[1]
                        atk = v[2]
                        defense = v[3]
                        atkspe = v[4]
                        defspe = v[5]
                        vit = v[6]
                        statut = v[7]
                        alteration = v[8]
                        brulure = v[9]
                        poison = v[10]
            return nom, nature, hp, atk, defense, atkspe, defspe, vit, statut, alteration, brulure, poison
                    
    def DeroulementCombat(self) :
        global pokemon1, pokemon2
        attaque_player = self.AttaqueJoueur()
        attaque_bot = self.AttaqueBot()
        if attaque_player.nom == "Abri" and attaque_bot.categorie != "Statut":
            attaque_player.priorite = 5
        elif attaque_bot.nom == "Abri" and attaque_player.categorie != "Statut":
            attaque_bot.priorite = 5
        elif attaque_player.nom == "Abri" and attaque_bot.categorie == "Statut" :
            attaque_player.precision = 0
            attaque_player.priorite = 5
        elif attaque_bot.nom == "Abri" and attaque_player.categorie == "Statut":
            attaque_bot.precision = 0
            attaque_bot.priorite = 5
        elif attaque_player.nom == "Coup Bas" and attaque_bot.categorie != "Statut":
            attaque_player.priorite = 5
        elif attaque_bot.nom == "Coup Bas" and attaque_player.categorie != "Statut":
            attaque_bot.priorite = 5
        if (attaque_player.nom == "Bluff" and self.pkm1.counting_bluff == 0) and (attaque_bot.nom == "Bluff" and self.pkm2.counting_bluff == 0) : 
            if self.pkm1.vit >= self.pkm2.vit :
                attaque_player.CalculDegat()
                attaque_bot.CalculDegat()
            else :
                attaque_bot.CalculDegat()
                attaque_player.CalculDegat()
        elif attaque_player.nom == "Bluff" and self.pkm1.counting_bluff == 0 :
            attaque_player.CalculDegat()
            attaque_bot.CalculDegat()
        elif attaque_bot.nom == "Bluff" and self.pkm2.counting_bluff == 0 :
            attaque_bot.CalculDegat()
            attaque_player.CalculDegat()
        elif attaque_player.priorite > attaque_bot.priorite :
            attaque_player.CalculDegat()
            if attaque_bot.nom == "Represailles" :
                attaque_bot.puissance *= 2
            attaque_bot.CalculDegat()
        elif attaque_bot.priorite > attaque_player.priorite : 
            attaque_bot.CalculDegat()
            if attaque_player.nom == "Represailles" :
                attaque_player.puissance *= 2
            attaque_player.CalculDegat()
        elif attaque_bot.priorite == attaque_player.priorite :
            if self.pkm1.vit >= self.pkm2.vit :
                attaque_player.CalculDegat()
                if attaque_bot.nom == "Represailles" :
                    attaque_bot.puissance *= 2
                if attaque_player.effect == "ChangePkm" and not attaque_player.fail :
                    self.pkm1 = attaque_player.ChangePkm("player")  
                    pokemon1 = self.pkm1     
                    attaque_player.my_pkm = self.pkm1
                    attaque_bot.pkm_foe = self.pkm1
                attaque_bot.CalculDegat()
                if attaque_bot.effect == "ChangePkm" and not attaque_bot.fail  :
                    self.pkm2 = attaque_bot.ChangePkm("bot")
                    pokemon2 = self.pkm2
                    attaque_player.pkm_foe = pokemon2
                    attaque_bot.my_pkm = pokemon2
            else :
                attaque_bot.CalculDegat()
                if attaque_player.nom == "Represailles" :
                    attaque_player.puissance *= 2
                if attaque_bot.effect == "ChangePkm" and not attaque_bot.fail :
                    self.pkm2 = attaque_bot.ChangePkm("bot")
                    pokemon2 = self.pkm2
                    attaque_player.pkm_foe = self.pkm2
                    attaque_bot.my_pkm = self.pkm2
                attaque_player.CalculDegat()
                if attaque_player.effect == "ChangePkm" and not attaque_player.fail :
                    self.pkm1 = attaque_player.ChangePkm("player")
                    pokemon1 = self.pkm1    
                    attaque_player.my_pkm = self.pkm1
                    attaque_bot.pkm_foe = self.pkm1
        
        
        attaque_bot.InfligerDgtFindeTour()
        attaque_player.InfligerDgtFindeTour()
        attaque_bot.fail = False 
        attaque_player.fail = False
                   
class Equipe() :
    def __init__(self, no) :
        self.no = no
        self.l_pok = self.ReturnListeEquipe(self.no)
        self.fighting = ""
        self.liste_ko = []
        self.ko_bot = []
        self.used = []
        self.trainer = self.ReturnTrainer(self.no)
             
    def EnCombat(self, cible) :
        self.fighting = cible   
        
    def ReturnListeEquipe(self, no) :
        with open("team.json", "r") as team :
            file = json.load(team)
        for liste in file:
            for k, v in liste.items() :
                if str(no) == k :
                    liste_equipe = v
        return liste_equipe
    
    def ReturnTrainer(self, no) :
        with open("trainer.json", "r") as trainer :
            file = json.load(trainer)
        for name in file:
            for k, v in name.items() :
                if str(no) == k :
                    for x in v :
                        nom_trainer = x
        return nom_trainer
    
    def ChangeStrikerAfterDeath(self, nb) :
        if nb == 1 :
            while True :
                for x in self.l_pok :
                    print(self.l_pok.index(x)+1, x)
                next_ = int(input("Qui choisissez vous ?"))
                new_pokemon = Pokemon(f'{self.l_pok[next_-1]}', 'male') 
                if new_pokemon.nom not in self.liste_ko :
                    print(f"{new_pokemon.nom} est envoye au combat")
                    if new_pokemon.nom not in team2.used :
                        new_pokemon.Stat()
                    new_pokemon.combat = True
                    self.EnCombat(new_pokemon.nom)
                    return new_pokemon
                else :
                    print("Envoie au combat impossible")
        elif nb == 2 :
            while True :
                next = random.choice(self.l_pok)
                if next not in self.ko_bot :
                    break
            index = self.l_pok.index(next)
            new_pokemon = Pokemon(f'{self.l_pok[index]}', 'male')
            print(f"{self.l_pok[index]} est envoye au combat")
            if new_pokemon.nom not in team2.used :
                new_pokemon.Stat()
            new_pokemon.combat = True
            self.EnCombat(new_pokemon.nom)
            return new_pokemon
    
    def Vainqueur(self) :
        if len(team.liste_ko) == 6 :
            print("Le bot a gagne")
            
        elif len(team2.ko_bot) == 6 :
            print("Vous avez gagne")
    
    def DeleteContent(self, playedd) :
        delete = []
        with open(playedd, "w") as p :
            json.dump(delete, p, indent=4)

class Py() :
    def __init__(self, l, L) :
        self.l = l
        self.L = L        
    
    def AfficherEcran(self) :
        self.screen = pygame.display.set_mode((self.L, self.l))
        pygame.display.set_caption("Pokemon")
        ico = pygame.image.load("icone.png")
        pygame.display.set_icon(ico)
        bg = pygame.Color((1,1,1))
        self.screen.fill(bg)
        
    def Overlay(self) :
        img_overlay = pygame.image.load(r"battle/background.png").convert_alpha()
        field1 = pygame.image.load(r"battle/field.png").convert_alpha()
        overlay = pygame.Surface((600, 440))
        overlay.fill((255,244,229))
        x = (self.L - 600) // 2
        y = (self.l - 440) // 2
        overlay.blit(img_overlay, (0,0))
        overlay.blit(field1, (0,300))      
        self.screen.blit(overlay, (x,y))
        
        

pygame.init()
pygame.mixer.init()

p = Py(800,800)
   

            

# (nom, sexe, niv)       
team = Equipe(8)
team2 = Equipe(9)
pokemon1 = Pokemon(team.l_pok[0],"male")
pokemon1.combat = True

team.EnCombat(pokemon1.nom)
pokemon2 = Pokemon(team2.l_pok[0],"male")
team2.EnCombat(pokemon2.nom)

pokemon1.Stat()
pokemon2.Stat()
#pokemon1.AfficherStats()
#pokemon2.AfficherStats()




print(f"Le combat commence!\n{team2.trainer} souhaite vous affronter.\n{team2.trainer} envoie {team2.l_pok[0]}.\n{team.l_pok[0]} je te choisis !")
running = True

while running :

    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
            
    p.AfficherEcran()  
    p.Overlay()
    pygame.display.flip()
    c = 1
    

    
    combat = Combat(pokemon1, pokemon2, pokemon1.liste_atk, pokemon2.liste_atk)
    print(f"\nTOUR {c}")
    print(pokemon1.nom, pokemon1.hp)
    print(pokemon2.nom, pokemon2.hp)
    combat.DeroulementCombat()
        
    c += 1
        
    if pokemon1.hp <= 0 :
        team.liste_ko.append(pokemon1.nom)
        if len(team.liste_ko) == 6 :
            team.Vainqueur()
            team.DeleteContent("played.json")
            team2.DeleteContent("played2.json")
            break
        pokemon1.combat = False
        pokemon1 = team.ChangeStrikerAfterDeath(1)
        print(len(team.liste_ko))
        print(len(team2.ko_bot))


    elif pokemon2.hp <= 0 :
        team2.ko_bot.append(pokemon2.nom)
        team2.l_pok.remove(pokemon2.nom)
        if len(team2.ko_bot) == 6 :
            team.Vainqueur()
            team.DeleteContent("played.json")
            team2.DeleteContent("played2.json")
            break
        pokemon2.combat = False
        pokemon2 = team2.ChangeStrikerAfterDeath(2)
        print(len(team.liste_ko))
        print(len(team2.ko_bot))

pygame.quit()