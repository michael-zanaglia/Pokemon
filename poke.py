import json
import random

class Pokemon():
    def __init__(self, nom, sexe, niv, num_pokedex="", nature = "", type = "") :
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
        self.hp, self.atk, self.defense, self.atk_spe, self.def_spe, self.vit = self.GetPkmStat()
        self.liste_atk = self.ListeAttaques()
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
                    hp = int(v[0])
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
    def __init__(self, nom, puissance, precision, type, categorie, priorite, effect):
        self.nom = nom
        self.type = type
        self.puissance = puissance
        self.precision = precision
        self.categorie = categorie
        self.priorite = priorite
        self.effect = effect
        
        
########################################### EFFETS GLOBALS ###########################################

        ### STATUS EFFECT ###
    def GetStatutChance(self, status) :
        liste = []
        for x in range(0,101):
            liste.append(x)
        choice = random.choice(liste)
        if choice < 10 :
            if status == "GEL" :
                self.GelEffect()
            if choice <= 20 :
                if status == "PSN" :
                    self.PoisonedEffect()
                elif status == "BRU" :
                    self.BruleEffect()
                elif status == "PAR" :
                    self.ParalysedEffect()
                elif status == "SLP" :
                    self.SleepEffect()
    
    def PoisonedEffect(self) :
        count = 0
        # Chaque fin de tour code partiellement fait
        if Pokemon.hp != 0 :
            if count == 0 :
                Pokemon.hp -= int((Pokemon.hp*10)/100)
                count += 1
            elif count == 1 :
                Pokemon.hp -= int((Pokemon.hp*12)/100)
                count += 1
            elif count >= 2 :
                Pokemon.hp -= int((Pokemon.hp*16)/100)
                count += 1
                
    def BruleEffect(self) :
        # Chaque fin de tour code partiellement fait
        one_time = 0
        while Pokemon.hp != 0 :
            Pokemon.hp -= int((Pokemon.hp*7)/100)
            if one_time == 0 :
                Pokemon.atk -= int((Pokemon.atk*20)/100)
                Pokemon.atk_spe -= int((Pokemon.atk_spe*20)/100)
    
    def ParalysedEffect(self) :
        count = 0
        liste_play = [1,2,3]
        liste_time = [1,2,3,4,5,6]
        while True :
            if count == 0 :
                Pokemon.vit = int(Pokemon.vit/3)
                choice_play = random.choice(liste_play)
                if choice_play < 3 :
                    # Message pour dire que le pokemon n'a pas pu attaquer
                    self.precision == 0
                count += 1
            choice_time = random.choice(liste_time)
            if choice_time < 5 :
                count = 0
            else :
                # Pokemon n'est plus paralyse... peut etre faire une fonction qui supprime un statut ?
                break
    
    def SleepEffect(self) :
        count = 0
        liste_play = [1,2,3]
        liste_time = [1,2,3,4,5]
        while True :
            if count == 0 :
                choice_play = random.choice(liste_play)
                if choice_play in liste_play :
                    # Message pour dire que le pokemon n'a pas pu attaquer
                    self.precision == 0
                count += 1
            choice_time = random.choice(liste_time)
            if choice_time < 4 :
                count = 0
            else :
                # Pokemon n'est plus endormi... peut etre faire une fonction qui supprime un statut ?
                break
    def GelEffect(self) :
            count = 0
            liste_play = [1,2,3]
            liste_time = [1,2,3,4,5,6]
            while True :
                if count == 0 :
                    choice_play = random.choice(liste_play)
                    if choice_play in liste_play :
                        # Message pour dire que le pokemon n'a pas pu attaquer
                        self.precision == 0
                    count += 1
                choice_time = random.choice(liste_time)
                if choice_time < 4 :
                    count = 0
                else :
                    # Pokemon n'est plus gele... peut etre faire une fonction qui supprime un statut ?
                    break
        ### STATUS EFFECT ###
        
    
#/!\ Verifier si le heal rend plus que les pv max du pokemon, je dois renvoyer la valeur de base
    def HealAfterFightEffect(self) :
        with open("statistic.json", "r") as stat :
            file = json.load(stat)
        for pokemons in file :
            for k,v in pokemons.items() :
                if Pokemon.nom == k :
                    if Pokemon.hp != v[0] :
                        Pokemon.hp += self.CalculDegat() / 2
    
    def HealEffect(self) :
        with open("statistic.json", "r") as stat :
            file = json.load(stat)
        for pokemons in file :
            for k,v in pokemons.items() :
                if Pokemon.nom == k :
                    if Pokemon.hp != v[0] :
                        Pokemon.hp += int(Pokemon.hp*10) / 100
                        
    def AtterissageEffect(self) :
        with open("statistic.json", "r") as stat :
            file = json.load(stat)
        for pokemons in file :
            for k,v in pokemons.items() :
                if Pokemon.nom == k :
                    if Pokemon.hp != v[0] :
                        Pokemon.hp = Pokemon.hp * 2
    
#/!\ Verifier si le pokemon ne s'enleve pas plus de 0 sinon affiche 0    
    def MutilerEffect(self) :
        Pokemon.hp -= int(Pokemon.hp*30) / 100
        
    def BoostDefSpeTeam(self) :
        count = 0
        while count != 5 :
            # Pour chaque Pokemon de l'equipe x2 DefSpe pendant 5 tours
            count += 1
        # Retourne aux stats de base
        with open("statistic.json", "r") as stat :
            file = json.load(stat)
        for pokemons in file :
            for k,v in pokemons.items() :
                if Pokemon.nom == k :
                    Pokemon.def_spe = v[4]
                    
    def BoostDef(self) :
        Pokemon.defense = int(Pokemon.defense*1.5)
        
    def BoostAtkSpe(self) :
        Pokemon.atk_spe = int(Pokemon.atk_spe*1.5)
    
    def ChanceBoostDef(self) :
        liste = []
        for x in range(0,101) :
            liste.append(x)
        choice = random.choice(liste)
        if choice <= 10 :
            Pokemon.defense += int(Pokemon.defense/2)
    
    
    def Bluff(self) :
        #Si c'est ta premiere attaque elle est prioritaire et apeure l'ennemie. Marche qu'une fois
        pass
    
    def PauseEffect(self) :
        #Si attaquer, prochain tour pause 
        pass
    
    def ChanceDiminuerDef(self) :
        liste = []
        for x in range(0,101) :
            liste.append(x)
        choice = random.choice(liste)
        if choice <= 20 :
            Pokemon.defense -= int((Pokemon.defense*25)/100)
            
    def ChanceDiminuerDefSpe(self) :
        liste = []
        for x in range(0,101) :
            liste.append(x)
        choice = random.choice(liste)
        if choice <= 20 :
            Pokemon.def_spe -= int((Pokemon.def_spe*25)/100)
            
    def ChanceDiminuerAtkSpe(self) :
        liste = []
        for x in range(0,101) :
            liste.append(x)
        choice = random.choice(liste)
        if choice <= 20 :
            Pokemon.atk_spe -= int((Pokemon.atk_spe*25)/100)
            
    def ChanceDiminuerAtk(self) :
        liste = []
        for x in range(0,101) :
            liste.append(x)
        choice = random.choice(liste)
        if choice <= 20 :
            Pokemon.atk -= int((Pokemon.atk*25)/100)
    
    def BaisseLaDef_spe(self) :
        Pokemon.def_spe -= int((Pokemon.def_spe*30)/100)
    
    def BaisseLaDef(self) :
        Pokemon.defense -= int((Pokemon.defense*30)/100)
        
    def BaisseAtk(self) :
        Pokemon.atk -= int((Pokemon.atk*30)/100)
    
    def Requiem(self) :
        count = 0
        if count == 3 :
            # if pokemon 1 est toujours le meme :
                # hp du pokemon en combat meurt
            # if pokemon 2 est toujours le meme :
                # hp du pokemon en combat meurt
            pass
        count += 1
        
    def Abri(self):
        # Si pokemon adverse attaque et que abri renvoie True le pokemon est proteger
        pass
        
    def ChangePkm(self) :
        # Fonction qui permettera d'envoye un pokemon dont le type et plus fort ou neutre face a nous
        pass
    
    def Colere(self) :
        #Si variable de colere True et count != 3 alors la prochaine attaque sera tjrs colere sinon renvoie false
        pass
    
    def Invincible(self) :
        # Tour sans atk mais a la prochaine il atk en contre partie si l'adversaire lance une atk il la rate.
        pass
    
    def CoupBas(self) :
        #Si l'adversaire atq je frappe en premier mais si la priorite et == le pokemon avec la plus grand rapidite atq en premier
        pass
    
    def Represailles(self) :
        # Si le pokemon frappe en deuxieme x2 la puissance de l'attaque
        pass
    
    def Voltige(self) :
        # Si attaque echoue :
            self.MutilerEffect()
            pass
    
    def DmgWithDefStat(self):
        Pokemon.atk = Pokemon.defense
        #Trouver un moyen de recuperer ensuite atk apres l'attaque
        pass
    
    def CalculDegat(self, my_pkm, pkm_foe) :
        # Verifie la precision, si precision est true on passe a la verification suivante sinon renvoie atk echouer
        # Lorsque atk, verifie la categorie et en fonction effectue le calcule de dommage.
        # Lors du calcule de dommage verifie si taux crit si c'est le cas effectue le double des degats 
        # Et si le type de l'attaque et efficace ou non mettre a jour les degat
        test_precision = []
        crit = []
        if my_pkm.hp != 0 and pkm_foe.hp != 0 :
            critprint = False
            for x in range(1,101) :
                test_precision.append(x)
            for y in range(1,25) :
                crit.append(y)
            choice_crit = random.choice(crit)
            choice_tp = random.choice(test_precision)
            if choice_tp <= self.precision :
                if self.categorie == "Physique" :
                    dgt = my_pkm.niv*0.4+2*((self.puissance * my_pkm.atk) / (pkm_foe.defense * 50) + 2 )
                elif self.categorie == "Spéciale" :
                    dgt = my_pkm.niv*0.4+2*((self.puissance * my_pkm.atk_spe) / (pkm_foe.def_spe * 50) + 2 )
                if choice_crit == 1 :
                    dgt *= 1.95
                    critprint = True
                if self.type in pkm_foe.pkm_faiblesse :
                    dgt *= 1.95
                    print("Super Efficace !")
                elif self.type in pkm_foe.pkm_double :
                    dgt *= 3.9
                    print("Mega Efficace !")
                elif self.type in pkm_foe.pkm_resistance :
                    dgt *= 0.5
                    print("Pas Efficace ...")
                elif self.type in pkm_foe.pkm_double_res :
                    dgt *= 0.25
                    print("Tres Peu Efficace ...")
                elif self.type in pkm_foe.pkm_immune :
                    dgt *= 0
                    print(f"{pkm_foe.nom} n'est pas affecté...")
                else :
                    dgt *= 1       
                pkm_foe.hp -= int(dgt)
                
                self.VerifierEffect()
                
                if pkm_foe.hp < 0 :
                    pkm_foe.hp = 0
                print(f"{my_pkm.nom} attaque {pkm_foe.nom} avec {self.nom} : {pkm_foe.hp} restant apres l'attaque.")
                if critprint :
                    print("Coup Critique !")
                    critprint = False 
            else : 
                print(f"{my_pkm.nom} : Votre attaque a echoué")                
                        
        if my_pkm.hp == 0 :
            print(f"{pkm_foe.nom} a gagné. {my_pkm.nom} est KO !")
        elif pkm_foe.hp == 0 :
            print(f"{my_pkm.nom} a gagné. {pkm_foe.nom} est KO !")
    
    
    def VerifierEffect(self) :
        if self.effect != "None" :
            if self.categorie == "Statut" :
                if self.effect == "GetStatutChance" :
                    if self.nom == "Bombe Beurk" or self.nom == "Direct Toxik" :
                        print(self.nom)
                        self.effect("PSN")
                    elif self.nom == "Lance-Flammes" or self.nom == "Déflagration" or self.nom == "Ebullition" or self.nom == "Poing Feu" or self.nom == "Crocs Feu" or self.nom == "Ballon Brulant":
                        print(self.nom)
                        self.effect("BRU")
                    elif self.nom == "Tonnerre" or self.nom == "Electacle" or self.nom == "Poing Eclair" or self.nom == "Crocs Eclair" :
                        print(self.nom)
                        self.effect("PAR")
                    elif self.nom == "Laser Glace" or self.nom == "Poing Glace" or self.nom == "Crocs Givre" :
                        print(self.nom)
                        self.effect("GEL")
                    else :
                        print(self.nom)
                        self.effect("SLP")
            
    def Affiche(self) :
        print(self.nom)


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
    
    def MyTurn(self) :
        self.turn_me = True
        self.turn_bot = False
        
    def BotTurn(self) :
        self.turn_me = False
        self.turn_bot = True
    
    # J'ouvre mon Fichier Json ou il y a les infos pour chaque attaques et je les renvois a la fonction qui prepare le combat
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
    
    def ChoisirAttaque(self, l_atk) :
        # Pour un test je demande une atk aléatoire mais ici on fera en sorte de recuperer le nom de l'atk selectionnée
        myatk = random.choice(l_atk)
        puissance, precision, prio, type_, categorie, effect = self.RecupererInfos(myatk)
        # J'instancie l'attaque en fonction de celle recuperer
        attaque = Attaque(myatk, puissance, precision, type_, categorie, prio, effect)
        return attaque
    
    def AttaqueJoueur(self) :
        attaque = self.ChoisirAttaque(self.l_atk1)
        # J'appelle la fonction qui calcul les degats
        return attaque
        
    
    
    def AttaqueBot(self) :    
        attaque2 = self.ChoisirAttaque(self.l_atk2)
        return attaque2
        

    
    def DeroulementCombat(self) :
        attaque_player = self.AttaqueJoueur()
        attaque_bot = self.AttaqueBot()
        if attaque_player.priorite > attaque_bot.priorite :
            attaque_player.CalculDegat(pokemon1,pokemon2)
            attaque_bot.CalculDegat(pokemon2,pokemon1)
        elif attaque_bot.priorite > attaque_player.priorite : 
            attaque_bot.CalculDegat(pokemon2,pokemon1)
            attaque_player.CalculDegat(pokemon1,pokemon2)
        elif attaque_bot.priorite == attaque_player.priorite :
            if self.pkm1.vit >= self.pkm2.vit :
                attaque_player.CalculDegat(pokemon1,pokemon2)
                attaque_bot.CalculDegat(pokemon2,pokemon1)
            else :
                attaque_bot.CalculDegat(pokemon2,pokemon1)
                attaque_player.CalculDegat(pokemon1,pokemon2)
        
    
            
            
    
        
        

# (nom, sexe, niv)       
pokemon1 = Pokemon("Suicune","male",50)
pokemon2 = Pokemon("Florizarre","femelle",50)
pokemon1.Stat()
pokemon2.Stat()
#pokemon1.AfficherStats()
#pokemon2.AfficherStats()


combat = Combat(pokemon1, pokemon2, pokemon1.liste_atk, pokemon2.liste_atk)
combat.DeroulementCombat()
combat.DeroulementCombat()
combat.DeroulementCombat()





# (nom, type, puissance, taux_crit, precision, categorie, effet)
#attaque = Attaque(test.liste_atk[0], 80, 80, 100, "Feu", "Physique")
#attaque.Affiche()
########## Faire heriter Pokemon a 54 classes enfants ?? ##############