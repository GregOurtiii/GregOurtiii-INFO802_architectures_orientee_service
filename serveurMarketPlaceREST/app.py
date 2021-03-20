from flask import Flask
from flask import jsonify
from flask import request
from zeep import Client
from flask_cors import CORS

import graphene
import json

urlSOAP = "https://serveursoap.azurewebsites.net/?wsdl"

# Creation de l'instance
app = Flask(__name__)
CORS(app)

class Produit(graphene.ObjectType):
    nomProduit = graphene.String()
    prixProduit = graphene.String()
    poidsProduit = graphene.String()

class Query(graphene.ObjectType):
    produit = graphene.List(Produit)

    def resolve_produit(self, info):
        return[
            Produit(nomProduit = "Dose de Khabatisme", prixProduit = "50", poidsProduit = "10"),
            Produit(nomProduit = "Banane", prixProduit = "10", poidsProduit = "5"),
            ]

@app.route("/", methods=['GET'])
def test():
    return "Hoey World !"

@app.route("/soap/<prixProduit>/<poidsProduit>/<distance>", methods=['GET'])
def getPrixLivraison(prixProduit, poidsProduit,distance):
    client = Client(urlSOAP)
    prixLivraison = client.service.livraison(poidsProduit, distance)
    prixTotal = int(prixProduit) + int(prixLivraison)
    print(prixLivraison)
    res = [prixTotal]
    return str(res) 

@app.route("/verification/<numCarte>", methods = ['GET'])
def verifCarteBancaire(numCarte):
    res = False
    if(len(numCarte) == 16):
        listeDigit = list(numCarte)
        digitFinal = listeDigit.pop()
        listeDigit.reverse()
        luhnTab = []
        for i, digit in enumerate(listeDigit):
            if(i % 2 == 0):
                luhnDigit = int(digit) * 2
                if(luhnDigit > 9):
                    luhnDigit = luhnDigit - 9
                luhnTab.append(luhnDigit)
            else:
                luhnTab.append(int(digit))

        res = ((int(digitFinal) + sum(luhnTab)) % 10 == 0)  
    return jsonify({'result' : res})

@app.route("/produit", methods = ['GET'])
def getProduits():
    schema = graphene.Schema(query=Query)
    query_produit = '{ produit{nomProduit prixProduit poidsProduit} }'
    res = schema.execute(query_produit)
    items = dict(res.data.items())
    print(items)
    return json.dumps(items, indent=4)


if(__name__=="__main__"):
    app.run()