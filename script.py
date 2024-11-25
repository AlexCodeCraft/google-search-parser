import requests
from bs4 import BeautifulSoup

# Demander l'intitulé de recherche
search_term = input("Entrez un terme de recherche Google : ")

# Construire l'URL de recherche
url = f"https://www.google.fr/search?q={search_term.replace(' ', '+')}"

# Ajouter un User-Agent pour imiter un navigateur
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

# Envoyer la requête
response = requests.get(url, headers=headers)

# Vérifier si la requête a réussi
if response.status_code != 200:
    print(f"Erreur de requête, statut : {response.status_code}")
    exit()

# Parser le HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Collecter les résultats sponsorisés et naturels
all_results = []

# Résultats sponsorisés
sponsored = soup.find_all('div', class_='mnr-c c3mZkd pla-unit')
for item in sponsored[:2]:
    link = item.find('a', class_='plantl')['href']
    title = item.find('a', class_='plantl').get('aria-label', 'Pas de titre disponible')
    all_results.append({'type': 'Sponsorisé', 'title': title, 'link': link})

# Résultats naturels
natural = soup.find_all('div', class_='tF2Cxc')
for item in natural[:2]:
    link = item.find('a')['href']
    title = item.find('h3').get_text() if item.find('h3') else 'Pas de titre disponible'
    all_results.append({'type': 'Naturel', 'title': title, 'link': link})

# Afficher les résultats combinés
if not all_results:
    print("Aucun résultat trouvé.")
else:
    print("\n=== Résultats de recherche ===")
    for idx, result in enumerate(all_results, start=1):
        print(f"Résultat {idx} ({result['type']}):")
        print(f"  Titre : {result['title']}")
        print(f"  URL : {result['link']}\n")

