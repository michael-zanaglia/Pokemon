import json

class CreerTableType():
    def __init__(self):
        self.nom = self.AskType()
        self.liste_faiblesse = self.AskList()
        
        
    def AskType(self) :
        ask = input("Le type :\n").capitalize()
        return ask
    
    def AskList(self) :
        L = []
        while True :
            w = input("Les Faiblesses :\n").capitalize()
            L.append(w)
            yn = input("Continuer ?(y/n)\n").lower()
            if yn == "y" :
                continue
            else :
                return L
            
    def PutInJson(self, liste) :
        dico = {self.nom : self.liste_faiblesse}
        liste.append(dico)
        with open("weak.json", "w") as weak :
            json.dump(liste, weak, indent=4)
            print("done")


liste = []

while True :
    creer = CreerTableType()
    creer.PutInJson(liste)
    yn = ("continuer ?").lower()
    if yn == "n" :
        break
    
    
