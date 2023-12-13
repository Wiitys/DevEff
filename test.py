import string
from collections import deque

# Définition d'une classe nommée Produit pour la gestion des produits et leur stockage
#Les fonctions de la classe Product sont __init__, AddProduct, DelProduct, CountProduct, PrintProducts, GenerateStorage
class Product:
    def __init__(self):
        self.Storage = {} #Dictionnaire pour stocker les produits en clé et leur quantité en valeurs
      
    # Méthode pour ajouter un produit au stockage qui prend en paramètre une liste de produits, exemple("A1","B6","Z2","F5")
    def AddProduct(self, listOfProducts):
        """
        :param List<String> listOfProducts : La liste des produits à ajouté dans le stockage 
        """
        listOfProducts = listOfProducts.replace(" ", "")
        productsMeetings = []
        print("Produit Commande :",listOfProducts)
        for product in listOfProducts.split(","):
            if product in self.Storage:  # Si le produit valide
                if product not in productsMeetings:
                    productsMeetings.append(product)
                    self.Storage[product].append(1)  # On ajoute une occurence si le produit n'a pas été ajouté
                else:
                    self.Storage[product][-1] += 1  # On incrémente de 1 si le produit a déjà été ajouté dans cette ajout
            else:  # Si le produit n'est pas valide
                print("Produit non valide",product)


    # Méthode pour enlever un produit donné en paramètre au Storage selon une quantité donnée en paramètre
    def DelProduct(self, product, quantity):
        """
        :param String product : clé du dictionnaire qui contient le type du produit et son volume
        :param Int quantity: valeur attribué à la clé dans le dictionnaire qui indique la quantité de produit en stock
        """
        counter = 0
        while quantity != 0 and counter < len(self.Storage[product]):
            if self.Storage[product][counter] - quantity == 0:  # Si la quantité à soustraire correspond à la quantité présente
                quantity = 0
                del self.Storage[product][counter]
            elif self.Storage[product][counter] - quantity < 0:  # Si la quantité à soustraire excède la quantité présente
                quantity -= self.Storage[product][counter]
                del self.Storage[product][counter]
            else:  # Si la quantité à soustraire est inférieure à la quantité présente
                self.Storage[product][counter] -= quantity
                quantity = 0  # La quantité à soustraire devient 0 car elle est entièrement déduite
            counter += 1  # Passage à l'élément suivant dans le stock
        if counter == len(self.Storage[product]) and quantity > 0:
            print("La quantité demandée à supprimer excède la quantité disponible.")

        
    # Méthode pour compter la quantité de produits dans le Storage
    def CountProduct(self):
        productQuantities = {}
        for product in self.Storage:
            productQuantities[product] = sum(self.Storage[product])
        return productQuantities

    def PrintProducts(self):
        print(self.Storage)
    
    # Méthode pour générer automatiquement les produits et les ajouter au Storage
    def GenerateStorage(self):
        for productType in list(string.ascii_uppercase): # Génération des produits de A à Z dans la variable product_type
            for volume in list('123456789'): # Génération des volumes de 1 à 9 dans la variable volume
                product = productType + volume # Concaténation des variables product_type et volume pour générer la clé product
                if productType <= 'M':
                    quantity = 15
                elif productType <= 'S':  #génération des quantités de produits en fonction du type du produit
                    quantity = 20
                else:
                    quantity = 25
                self.Storage[product] = [quantity] # Ajout du produit et de sa quantité au Storage
        print(self.Storage) # Affichage du Storage pour vérifier son contenu

# Définition d'une classe nommée Alert pour la gestion des alertes sur les produits et leur réapprovisionnement au bout d'une certaine quantité dans le stockage
#Les fonctions de la classe Alert sont __init__, PrintAlert, PopAlert, AddAlert, AlertQueueOverflow, CheckAlertConditions, AlertGenerator
class Alert:
    def __init__(self):
        self.log = [None, None, None] # File des alertes
        self.listProductDiscountThreshold = {} 
        self.listQuantityProductToBeDelivered = {}
        lettres = string.ascii_uppercase 

        for lettre in lettres: # Génération des seuils de réapprovisionnement en fonction du type du produit
            if lettre <= 'M':
                self.listProductDiscountThreshold[lettre] = 10
                self.listQuantityProductToBeDelivered[lettre] = 15      
            elif lettre <= 'S':
                self.listProductDiscountThreshold[lettre] = 15
                self.listQuantityProductToBeDelivered[lettre] = 20
            else:
                self.listProductDiscountThreshold[lettre] = 20
                self.listQuantityProductToBeDelivered[lettre] = 25
        
    # Méthode pour afficher le contenu de la file des alertes
    def PrintAlert(self):
        print("Contenu de la file :")
        for alert in self.log:
            print(alert)        

    # Méthode pour mettre la file en statique et afficher les alertes par ordre de priorité
    def PopAlert(self):
        outPutValue=self.log[0] 
        self.log[0]=self.log[1] 
        self.log[1]=self.log[2]
        self.log[2]=None
        return outPutValue
    
    # Méthode pour ajouter une alerte à la file sur un produit en faible quantité
    def AddAlert(self,productAlert):
        """
        :param String productAlert: Clé du dictionnaire de stockage venant de la classe alertes
        """
        for i in range(len(self.log)): 
            if self.log[i] is None: 
                self.log[i] = productAlert
                print('Alerte sur :' ,productAlert)
                break
    
    # Méthode pour gérer le débordement de la file des alertes, on vide la file et on commande les produits manquants
    def AlertQueueOverflow(self,productInstance):
        """
        :param Product productInstance: Instance de la classe produit
        """
        for alert in self.log:
            productToBeDelivered=self.PopAlert()
            typeProductToBeDeliverder=productToBeDelivered[0]
            productToBeDelivered=((productToBeDelivered+", " )* int (self.listQuantityProductToBeDelivered[typeProductToBeDeliverder] - 1)) + productToBeDelivered
            productInstance.AddProduct(productToBeDelivered)

    # Vérifie les conditions pour modifier le log
    def CheckAlertConditions(self, product, dictQuantityProduct,productInstance):
        """
        """
        logIsFull = True
        productIsNotInLog = True  # Réinitialisation de productIsNotInLog pour chaque produit
        for alert in self.log:
            if alert == product:
                productIsNotInLog = False
                break  # Arrêter la boucle une fois que le produit est trouvé dans la file des alertes

        if (
            dictQuantityProduct[product] <= self.listProductDiscountThreshold[product[0]]
            and productIsNotInLog
        ):
            for alert in self.log:
                if alert is None:
                    logIsFull = False
            if logIsFull:
                self.AlertQueueOverflow(productInstance)
            self.AddAlert(product)

    # Rafraichis la variable dictQuantityProduct avec pour instance la dernière instance
    def AlertGenerator(self, productInstance):
        dictQuantityProduct = productInstance.CountProduct()
        for product in productInstance.Storage:
            dictQuantityProduct = productInstance.CountProduct()
            self.CheckAlertConditions(product, dictQuantityProduct,productInstance)
            
# Définition d'une classe nommée Packaging pour la gestion des colis et leur contenu
#Les fonctions de la classe Packaging sont __init__, SetContent, CountProductPackage, ProductStacking, RemoveProduct, CheckProduct
class Packaging:
    def __init__(self):
        self.colis = deque() # File des colis

    # Méthode pour demander à l'utilisateur de saisir le contenu du colis
    def SetContent(self,productInstance):
        content = input("Entrez les produits à mettre dans le colis : ")
        if(True) :
            contentSplit = content.split(', ')
            productQuantities = self.CountProductPackage(contentSplit)  # Utiliser CountProductColis de la classe Packaging
            validContent = self.CheckProduct(contentSplit, productQuantities, productInstance)
            if validContent:
                print("Contenu du colis valide.")
                return contentSplit
            else:
                print("La saisie du colis est invalide. Produit insuffisant.")
                return []


    # Méthode pour compter la quantité de produits dans le colis
    def CountProductPackage(self, content):
        productQuantities = {}
        for product in content:
            productQuantities[product] = productQuantities.get(product, 0) + 1
        return productQuantities

    # Méthode pour retirer les colis du stockage
    def RemoveProduct(self, contentSplit,productInstance):
            for product in contentSplit:
                quantityToRemove = 1
                productInstance.DelProduct(product, quantityToRemove)
    
    
    # Méthode pour empiler les produits dans le colis suivant leur volume
    def ProductStacking(self,productInstance):
        contentSplit=self.SetContent(productInstance)
        self.RemoveProduct(contentSplit,productInstance)    #En premier lieu nous allons supprimer les produits du stockage qui seront mis dans le colis
        while len(contentSplit) > 0:    #Itère jusqu'à la liste contentSplit soit vide 
            max="A0"
            indexMax=0
            for i in range(len(contentSplit)):  #Détermine le volume le plus gros à mettre dans le colis
                if contentSplit[i][1] > max[1]:
                    max = contentSplit[i]
                    indexMax = i
            print(max)  #Affiche le produit avant de le mettre dans le colis l'ordre d'affichage est donc dans l'ordre inverse du colis
            self.colis.appendleft(max)
            del contentSplit[indexMax]

    # Méthode pour vérifier si le contenu du colis est valide (présent dans le stockage en quantité suffisante)
    def CheckProduct(self, contentSplit, productQuantities,productInstance):
        productQuantitiesStorage = productInstance.CountProduct() #On compte les produits dans le stockage et on les mets dans productQuantitiesStorage

        for product in contentSplit: #On parcourt les produits du colis
            if product not in productInstance.Storage: #Si le produit n'est pas présent dans le stockage, on affiche qu'il n'est pas présent
                print(f"Le produit {product} n'est pas présent dans le stockage.")
                return False
            elif productQuantities[product] > productQuantitiesStorage[product]: #Si la quantité demandée pour le produit excède la quantité disponible dans le stockage, on affiche qu'il n'y a pas assez de produit
                print(f"La quantité demandée pour {product} excède la quantité disponible dans le stockage.")
                return False

        return True

if __name__ == "__main__":
        productInstance = Product()
        alertInstance = Alert()
        productInstance.GenerateStorage()
        while True:
            alertInstance.AlertGenerator(productInstance)
            print("\nMenu:\n1. Ajouter un produit\n2. Afficher les produits en stocks \n3. Afficher les alertes \n4. Mettre en colis\n5. Quitter\n")
            choice = input("Choisissez une action (1-5) : ")

            if choice == '1':
                listOfProducts = input("Entrez les produits a ajouter au stockage : ")
                productInstance.AddProduct(listOfProducts)
            elif choice == '2':
                productInstance.PrintProducts()
            elif choice == '3':
                alertInstance.PrintAlert()
            elif choice == '4':
                packageInstance = Packaging()            
                packageInstance.ProductStacking(productInstance)
                alertInstance.AlertGenerator(productInstance)
            elif choice == '5':
                print("Programme terminé. Au revoir!")
                break
            else:
                print("Choix non valide. Veuillez réessayer.")