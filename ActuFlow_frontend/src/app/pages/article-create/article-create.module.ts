import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonBackButton, IonButton, IonButtons, IonContent, IonHeader, IonIcon, IonInput, IonSelect, IonSelectOption, IonTextarea, IonTitle, IonToolbar } from '@ionic/angular';
import { ArticleCreatePage } from './article-create.page';
import { ArticleCreatePageRoutingModule } from './article-create-routing.module';
@NgModule({ imports: [CommonModule, FormsModule, IonBackButton, IonButton, IonButtons, IonContent, IonHeader, IonIcon, IonInput, IonSelect, IonSelectOption, IonTextarea, IonTitle, IonToolbar, ArticleCreatePageRoutingModule], declarations: [ArticleCreatePage] })
export class ArticleCreatePageModule {}
