import os
import requests


CAT_API = os.getenv("CAT_API_URL") # "https://api.thecatapi.com/v1/breeds"


def validateBreed(breed: str) -> bool:
    breedsData = requests.get(CAT_API).json()
    
    for breedData in breedsData:
        if breedData["name"] == breed:
            return True
    
    return False