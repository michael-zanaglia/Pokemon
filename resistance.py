import json

class CreerTableType():
    def __init__(self):
        self.load = None
        self.list_nom_type = []
        self.nom = self.AskType()
        self.liste_resis = self.AskList()
        
        
    def AskType(self) :
        with open("weak.json", "r") as weak :
            self.load = json.load(weak)
        for contents in self.load :
            for k,v in contents.items() :
                self.list_nom_type.append(k)
        return self.list_nom_type
    
    def AskList(self) :
        L = []
        for x in self.nom :
            sub_L = []
            while True :
                w = input(f"Les Resistances de {x} :\n").capitalize()
                sub_L.append(w)
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
        with open("res.json", "w") as res :
            json.dump(liste, res, indent=4)
            print("done")


liste = []

while True :
    creer = CreerTableType()
    creer.PutInJson(liste)
    yn = ("continuer ?").lower()
    if yn == "n" :
        break
    