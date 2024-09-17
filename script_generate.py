from faker import Faker
import pymongo
import random

# Initialisation
fake = Faker()
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["business_intelligence"]

# Collections
vendeurs_collection = db["vendeurs"]
clients_collection = db["clients"]
commandes_collection = db["commandes"]

# Fonction pour générer des vendeurs
def generate_vendeurs(num_vendeurs):
    vendeurs = []
    for _ in range(num_vendeurs):
        vendeur = {
            'prenom': fake.first_name(),
            'nom': fake.last_name(),
            'telephone': fake.phone_number(),
            'sexe': random.choice(['M', 'F'])
        }
        vendeurs.append(vendeur)
    vendeurs_collection.insert_many(vendeurs)
    print(f"{num_vendeurs} vendeurs générés et insérés.")

# Fonction pour générer des clients
def generate_clients(num_clients):
    clients = []
    for _ in range(num_clients):
        client = {
            'prenom': fake.first_name(),
            'nom': fake.last_name(),
            'telephone': fake.phone_number(),
            'sexe': random.choice(['M', 'F']),
            'type': random.choice(['A', 'B', 'C'])
        }
        clients.append(client)
    clients_collection.insert_many(clients)
    print(f"{num_clients} clients générés et insérés.")

# Fonction pour générer des commandes
def generate_commandes(num_commandes):
    vendeurs = list(vendeurs_collection.find({}, {'_id': 1}))
    produits = list(db.produits.find({}, {'_id': 1}))  # Utilisation de la collection existante de produits
    clients = list(clients_collection.find({}, {'_id': 1}))
    
    commandes = []
    for _ in range(num_commandes):
        commande = {
            'client': random.choice(clients)['_id'],
            'vendeur': random.choice(vendeurs)['_id'],
            'date': fake.date_time_this_year(),
            'produits': [
                {
                    'produit': random.choice(produits)['_id'],
                    'quantite': random.randint(1, 5)
                } for _ in range(random.randint(1, 3))
            ]
        }
        commandes.append(commande)
    commandes_collection.insert_many(commandes)
    print(f"{num_commandes} commandes générées et insérées.")

# Exécuter les fonctions pour insérer les données
generate_vendeurs(5)
generate_clients(100)
generate_commandes(1500)
