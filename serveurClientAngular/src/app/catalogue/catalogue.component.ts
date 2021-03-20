import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable, throwError} from 'rxjs';
import { Injectable } from '@angular/core';

@Component({
  selector: 'app-catalogue',
  templateUrl: './catalogue.component.html',
  styleUrls: ['./catalogue.component.scss']
})
export class CatalogueComponent implements OnInit {

  posts: Observable<any>|undefined

  urlAPI = "https://serveurmarketplacerest.azurewebsites.net/";

  isLoading = true;

  produits: any[]|undefined;
    /*{
      nomProduit: "Dose de khabatisme",
      prixProduit: "50",
      poidsProduit: "10"
    },
    {
      nomProduit: "Banane",
      prixProduit: "10",
      poidsProduit: "5"
    }*/

  constructor(private http: HttpClient) { 
  }

  ngOnInit(): void {
    console.log("uiii produit");
    var liste;
    var url = this.urlAPI;
    url = url.concat('produit');
    this.posts = this.http.get(url);
    this.posts.forEach(async (value) => {
       this.produits = await value["produit"];
       this.isLoading = false;
       //console.log(liste);
    });
  }

}
