import { Component, OnInit, Input} from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable, throwError} from 'rxjs';
import { Injectable } from '@angular/core'; 

@Component({
  selector: 'app-produit',
  templateUrl: './produit.component.html',
  styleUrls: ['./produit.component.scss']
})
export class ProduitComponent implements OnInit {

  @Input() nomProduit: string|undefined;
  @Input() prixProduit: string|undefined;
  @Input() poidsProduit: string|undefined;
  distance = 0;
  prixTotal = 0;
  numeroCarte: number|undefined;
  posts: Observable<any>|undefined
  etatPayement = "";

  urlAPI = "https://serveurmarketplacerest.azurewebsites.net/";


  constructor(private http: HttpClient) {
  }

  onTotalClicked(){
    //this.prixTotal = 0;
    console.log("uiii total");
    var url = this.urlAPI;
    url = url.concat('soap/' + this.prixProduit?.toString() + "/" + this.poidsProduit?.toString() + "/" + this.distance.toString());
    this.posts = this.http.get(url);
    this.posts.forEach(async (value) => {
      this.prixTotal = await value[0];
      console.log(this.prixTotal);
      this.etatPayement = "";
    });
  }

  onCommandClicked(){
    console.log("uiii command");
    var numAValider = this.numeroCarte?.toString();
    var url = this.urlAPI;
    url = url.concat('/verification' + "/" + this.numeroCarte?.toString());
    this.posts = this.http.get(url);
    this.posts.forEach(async (value) => {
      var res = await value["res"];
      console.log(res);
      if(res == true){
        this.etatPayement = "Paiement accepte !";
      }
      else{
        this.etatPayement = "Paiement refuse..."
      }
    })
  }

  ngOnInit(): void {
  }

}
