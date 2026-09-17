import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonBackButton, IonButton, IonButtons, IonContent, IonHeader, IonIcon, IonSpinner, IonTextarea, IonTitle, IonToolbar } from '@ionic/angular';
import { ArticleDetailPageRoutingModule } from './article-detail-routing.module';
import { ArticleDetailPage } from './article-detail.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonBackButton,
    IonButton,
    IonButtons,
    IonContent,
    IonHeader,
    IonIcon,
    IonSpinner,
    IonTextarea,
    IonTitle,
    IonToolbar,
    ArticleDetailPageRoutingModule
  ],
  declarations: [ArticleDetailPage]
})
export class ArticleDetailPageModule {}
