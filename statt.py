import json

class CreerPokeStat():
    def __init__(self):
        self.load = None
        self.list_nom_pkm = []
        self.nom = self.AskName()
        self.liste_resis = self.AskList()
        
        
    def AskName(self) :
        with open("pokedex.json", "r") as pdx :
            self.load = json.load(pdx)
        for contents in self.load :
            for k,v in contents.items() :
                self.list_nom_pkm.append(v[0][0])
        return self.list_nom_pkm
    
    def AskList(self) :
        L = []
        for x in self.nom :
            sub_L = []
            while True :
                stat = input(f"Les Atk de {x} :\n")
                sub_L = stat.split()
                yn = input("Continuer ?(y/n)\n").lower()
                if yn == "y" :
                    continue
                else :
                    L.append(sub_L)
                    break
        print(L)        
        return L
            
    def PutInJson(self, liste) :
        for x in self.nom :
            index = self.nom.index(x)
            dico = {x : self.liste_resis[index]}
            liste.append(dico)
        with open("atk_pokemon.json", "w") as stat :
            json.dump(liste, stat, indent=4)
            print("done")


liste = []

while True :
    creer = CreerPokeStat()
    creer.PutInJson(liste)
    yn = ("continuer ?").lower()
    if yn == "n" :
        break