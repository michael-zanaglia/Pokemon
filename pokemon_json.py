import json

class CreerPokedex() :
    def __init__(self, description="", numero=0, nom="") :
        self.file = self.Reload()
        if numero == 0 :
            self.numero = self.AskNumber()
            self.Modifier()
        if len(self.file) == 0 :
            if description == "" :
                self.description = self.AskDescription()
            if nom == "" :
                self.nom = self.AskName()
            
    def Reload(self) :
        with open("pokedex.json", "r") as pokedex :
            return json.load(pokedex)
            
            
        
    def AskDescription(self) :
        d = input("Description votre Pokemon :\n")
        return d
        
    def AskNumber(self) :
        num = input("Numero Pokedex de votre Pokemon :\n")  
        return num
    
    def AskName(self) :
        name = input("Nom de votre Pokemon :\n")
        return name
    
    def AskType(self) :
        liste_type = []
        while True :
            type_ = input("Entrez un type\n")
            liste_type.append(type_)
            yn = input("Continuer ?").lower()
            if yn == "n" : 
                return liste_type
            else :
                continue
    
    def EntrerDonnee(self) :
        dico = {self.numero : (self.nom, self.description) }
        liste.append(dico)
        with open("pokedex.json", "w") as pokedex :
            json.dump(liste, pokedex, indent=4)
            print("done")
    
    def Modifier(self) :
        for x in self.file :
            for k,v in x.items() :
                self.nom = k
                self.description = v
                if self.numero == k :
                    print(x[self.numero])
                    yn = input("Souhaitez-vous modifier ?").lower()
                    if yn == "y" :
                        types = self.AskType()
                        x[k] = (self.nom, self.description, types)
                        with open("pokedex.json", "w") as pokedex :
                            json.dump(self.file, pokedex, indent=4)
                            print("done")
                    else :
                        pass


                
    
liste = []

while True :
    creer = CreerPokedex()
    #creer.EntrerDonnee()
    yn = input("Continuer?(y/n)\n").lower()
    if yn == "n" :
        break
    else :
        continue
