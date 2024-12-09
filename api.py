# Escriba (o pegue) aquí su solución
import re
import requests
from bs4 import BeautifulSoup

def extraer_info(theme = "", search = "", limit = -1):
    url = f"https://elpais.com/{theme}"
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    
    # Noticias de la portada (parte de arriba)
    main = soup.find("main")
    noticias = main.find_all(name = "article")
    
    saved = []
    for noticia in noticias:
        titulo = noticia.find("h2", "c_t").text.strip()
        
        # Puede no aparecer la información del resumen
        try:
            resumen = noticia.find("p", "c_d").text.strip()
        except:
            resumen = ""
        
        # Puede no aparecer la información del autor
        try:
            autor = noticia.find("a", "c_a_a").text.strip()
        except:
            autor = ""
        
        # Si contiene search se guarda (search = "" siempre lo encuentra)
        if re.search(search.lower(), titulo.lower()):
            saved.append({"title": titulo, "author": autor, "summary": resumen})
        
        # Número de noticias limitado por limit
        # Por defecto es -1 para no terminar hasta que se lean todas las noticias
        if len(saved) == limit:
            return saved
    return saved
    

import hug

# En general, si algo no sale bien te avisa
api = hug.get(on_invalid=hug.redirect.not_found)

# Ponemos una tras otra, porque hug lo permite
@api.urls("/")
def portada(search = "", limit: hug.types.number = -1):
    return extraer_info("", search, limit)

@api.urls("/internacional/")
def internacional(search = "", limit: hug.types.number = -1):
    return extraer_info("internacional/", search, limit)

@api.urls("/opinion/")
def opinion(search = "", limit: hug.types.number = -1):
    return extraer_info("opinion/", search, limit)

@api.urls("/politica/")
def politica(search = "", limit: hug.types.number = -1):
    return extraer_info("espana/", search, limit)

@api.urls("/sociedad/")
def sociedad(search = "", limit: hug.types.number = -1):
    return extraer_info("sociedad/", search, limit)

@api.urls("/economia/")
def economia(search = "", limit: hug.types.number = -1):
    return extraer_info("economia/", search, limit)

@api.urls("/ciencia/")
def ciencia(search = "", limit: hug.types.number = -1):
    return extraer_info("ciencia/", search, limit)

@api.urls("/tecnologia/")
def tecnologia(search = "", limit: hug.types.number = -1):
    return extraer_info("tecnologia/", search, limit)

@api.urls("/cultura/")
def cultura(search = "", limit: hug.types.number = -1):
    return extraer_info("cultura/", search, limit)

@api.urls("/gente/")
def gente(search = "", limit: hug.types.number = -1):
    return extraer_info("gente/", search, limit)

@api.urls("/deportes/")
def deportes(search = "", limit: hug.types.number = -1):
    return extraer_info("deportes/", search, limit)
