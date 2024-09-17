import requests
from bs4 import BeautifulSoup
import pymongo
import time

# Connexion à MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["business_intelligence"]
produits_collection = db["produits"]

# Fonction pour scraper une page spécifique de produits
def scrape_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie que la requête est réussie
        soup = BeautifulSoup(response.content, 'html.parser')

        # Sélection des éléments contenant les informations des produits
        produits = soup.find_all('div', class_='itm col')

        for produit in produits:
            try:
                # Extraction des informations produit
                nom = produit.find('div', class_='name').text.strip()
                prix = produit.find('div', class_='prc').text.strip()
                image = produit.find('img')['data-src']
                lien = produit.find('a')['href']
                reduction = produit.find('div', class_='bdg _dsct').text.strip() if produit.find('div', class_='bdg _dsct') else None

                # Stockage des données dans MongoDB
                produit_data = {
                    'nom': nom,
                    'prix': prix,
                    'image': image,
                    'lien': f"https://www.jumia.sn{lien}",
                    'reduction': reduction
                }
                
                # Vérification si le produit existe déjà pour éviter les doublons
                if produits_collection.count_documents({'nom': nom}) == 0:
                    produits_collection.insert_one(produit_data)
                    print(f"Produit inséré : {nom}")
                else:
                    print(f"Produit déjà existant : {nom}")

            except Exception as e:
                print(f"Erreur lors de l'extraction d'un produit : {e}")
        
        return True

    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP : {http_err}")
    except Exception as err:
        print(f"Autre erreur : {err}")
    
    return False

# Fonction pour gérer la pagination et scraper plusieurs pages (si applicable)
def scrape_multiple_pages(base_url, max_pages=5):
    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        print(f"Scraping page {page} : {url}")
        success = scrape_page(url)
        
        if not success:
            print(f"Arrêt du scraping à la page {page}")
            break
        
        # Pause pour éviter d'être bloqué par le site
        time.sleep(2)

# URL de la page des produits 
base_url = 'https://www.jumia.sn/mlp-boutiques-officielles/'

# Scraper les premières 5 pages du catalogue (si plusieurs pages sont disponibles)
scrape_multiple_pages(base_url, max_pages=5)

print("Scraping terminé et données insérées dans MongoDB !")