import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonBackButton, IonButton, IonButtons, IonContent, IonHeader, IonIcon, IonSpinner, IonTitle, IonToolbar } from '@ionic/angular';
import { MyArticlesPage } from './my-articles.page';
import { MyArticlesPageRoutingModule } from './my-articles-routing.module';
@NgModule({ imports: [CommonModule, FormsModule, IonBackButton, IonButton, IonButtons, IonContent, IonHeader, IonIcon, IonSpinner, IonTitle, IonToolbar, MyArticlesPageRoutingModule], declarations: [MyArticlesPage] })
export class MyArticlesPageModule {}
