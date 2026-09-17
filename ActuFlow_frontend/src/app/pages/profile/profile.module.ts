import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonBackButton, IonButton, IonButtons, IonChip, IonContent, IonHeader, IonIcon, IonInput, IonItem, IonLabel, IonSpinner, IonTextarea, IonTitle, IonToolbar } from '@ionic/angular';
import { ProfilePage } from './profile.page';
import { ProfilePageRoutingModule } from './profile-routing.module';
@NgModule({ imports: [CommonModule, FormsModule, IonBackButton, IonButton, IonButtons, IonChip, IonContent, IonHeader, IonIcon, IonInput, IonItem, IonLabel, IonSpinner, IonTextarea, IonTitle, IonToolbar, ProfilePageRoutingModule], declarations: [ProfilePage] })
export class ProfilePageModule {}
