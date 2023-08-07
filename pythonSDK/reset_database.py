import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, auth
from datetime import datetime
import json 
from dotenv import load_dotenv
from random import randint
import os


load_dotenv()

cred = credentials.Certificate(os.getenv("firebase_secret"))
app = firebase_admin.initialize_app(cred)


db = firestore.client()

COLLECTIONS_MAP = [
    ('ambientes', 'json/ambientes.json', 'ambiente_codigo', False), 
    ('items', 'json/permanentes.json', 'key', True)
]


def load_json_file(filename):
    with open(filename) as fp:
        content = json.load(fp)
    return content


def batch_write(collection: str, dictarray: list[dict], key_id: str | None = None):
    batch = db.batch()
    collection_ref = db.collection(collection)
    k = 1
    for i in range(0, len(dictarray), 500):
        chunk = dictarray[i:i+500]
        for document in chunk:
            if key_id:
                doc_ref = collection_ref.document(document[key_id])
                batch.set(doc_ref, document)
        print(f"{collection}: chunk {k} ({len(chunk)} documents)")
        k += 1
        batch.commit()

DATE_MAP = {
    'detalhes': [ ('transf_local', '%d/%m/%Y'), ('incorporacao', '%d/%m/%Y') ],
    'meta': [ ('updated', '%d/%m/%Y %H:%M:%S')]
}
 
def process_datetime(registro: dict): 
    for main in DATE_MAP:
        for key, fmt in DATE_MAP[main]: 
            if key in registro[main]:
                try: 
                    registro[main][key] = datetime.strptime(registro[main][key], fmt)
                except:
                    registro[main][key] = None
    return registro
    

if __name__ == "__main__":
    for col, file, key, process in COLLECTIONS_MAP:
        dados = load_json_file(file) 
        if process:
            dados = [ process_datetime(x) for x in dados ]
        N = len(dados)
        k = randint(0, N-1)
        print(col, N, key, dados[k])
        #batch_write(col, dados, key)