import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonButton, IonCard, IonCardContent, IonCardHeader, IonCardTitle, IonChip, IonContent, IonHeader, IonIcon, IonSearchbar, IonSpinner, IonTitle, IonToolbar } from '@ionic/angular';
import { FormsModule } from '@angular/forms';
import { HomePage } from './home.page';

import { HomePageRoutingModule } from './home-routing.module';


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonContent,
    IonHeader,
    IonButton,
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardTitle,
    IonChip,
    IonIcon,
    IonSearchbar,
    IonSpinner,
    IonTitle,
    IonToolbar,
    HomePageRoutingModule
  ],
  declarations: [HomePage]
})
export class HomePageModule {}
