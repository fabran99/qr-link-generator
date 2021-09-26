import qrcode
from PIL import Image
import firebase_admin
from firebase_admin import credentials, firestore
import uuid
import pandas as pd
from constants import default_figure, default_url, default_collection, databaseURL, email, password, url_base

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':databaseURL
})
# ref = db.reference("/{}/OaYJJhlrqSwGPEsug2EI".format(default_collection))
db = firestore.client()
def generate_qr_image(link):
    """
    Devuelve una imagen qr
    """

    img = qrcode.make(link)
    img.thumbnail((150,150), Image.ANTIALIAS)
    return img


def upload_random_links(n):
    """
    Sube links a firebase y luego devuelve los 
    ids autogenerados
    """
    data = {
        "url": default_url,
        "figura":default_figure
    }
    response_ids = []
    ref = db.collection(default_collection)
    for x in range(n):
        random_id = str(uuid.uuid4())
        result = ref.document(random_id).set(data)
        response_ids.append(random_id)

    return response_ids


def generate_all_qrs(n):
    id_list = upload_random_links(n)
    url_list = []
    for x in id_list:
        url = url_base + x
        qr_image = generate_qr_image(url)
        qr_image.save("./qr_result/{}.png".format(x))
        url_list.append({
            "url": url_base + x,
            "figura":default_figure
        })
    
    df = pd.DataFrame(url_list)
    df.to_excel("./result.xlsx")


def set_data_to_id(id, link, figure):
    ref = db.collection(default_collection)
    ref.document(id).set({"url":link, "figura":figure})


def start():
    """
    Inicia el programa
    """
    option_text = """Selecciona una opcion:
    1- Generar QRS
    2- Asignar QR \n"""
    option = input(option_text)

    try:
        option = int(option)
    except:
        print("Opcion no valida")
        return

    if option == 1:
        n = input("Ingrese la cantidad de qrs a generar:\n")
        generate_all_qrs(int(n))
    elif option == 2:
        current_uuid = input("Ingrese el identificador: \n")
        current_link = input("Ingrese el link a asignar: \n")
        current_figure = input("Ingrese nombre de la figura: \n")
        set_data_to_id(current_uuid, current_link, current_figure)
    else:
        print("Opcion invalida")
    

start()

