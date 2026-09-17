import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AlertController, LoadingController } from '@ionic/angular';
import { AuthService, UserProfile } from '../../services/auth.service';
import { finalize, timeout } from 'rxjs';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.page.html',
  styleUrls: ['./profile.page.scss'],
  standalone: false
})
export class ProfilePage implements OnInit {
  profile?: UserProfile;
  form = { prenom: '', nom: '', biographie: '' };
  selectedPhoto?: File;
  isLoading = true;

  constructor(private authService: AuthService, private router: Router, private loadingController: LoadingController, private alertController: AlertController) {}

  ngOnInit(): void {
    const storedProfile = this.authService.currentUserValue;
    if (storedProfile?.prenom && storedProfile?.nom) {
      this.profile = storedProfile;
      this.form = { prenom: storedProfile.prenom, nom: storedProfile.nom, biographie: storedProfile.biographie || '' };
    }
    this.authService.getProfile().pipe(timeout(8000), finalize(() => this.isLoading = false)).subscribe({
      next: profile => { this.profile = profile; this.form = { prenom: profile.prenom, nom: profile.nom, biographie: profile.biographie || '' }; },
      error: () => { if (!this.profile) this.router.navigate(['/login'], { queryParams: { returnUrl: '/profile' } }); }
    });
  }

  selectPhoto(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.selectedPhoto = input.files?.[0];
  }

  async save(): Promise<void> {
    const loading = await this.loadingController.create({ message: 'Enregistrement...', spinner: 'crescent' });
    await loading.present();
    const data = this.selectedPhoto ? new FormData() : this.form;
    if (data instanceof FormData) {
      data.append('prenom', this.form.prenom); data.append('nom', this.form.nom); data.append('biographie', this.form.biographie); data.append('photo_profil', this.selectedPhoto!);
    }
    this.authService.updateProfile(data).subscribe({
      next: profile => { this.profile = profile; loading.dismiss(); this.showSaved(); },
      error: async () => { loading.dismiss(); const alert = await this.alertController.create({ header: 'Enregistrement impossible', message: 'Vérifiez les informations puis réessayez.', buttons: ['OK'] }); await alert.present(); }
    });
  }

  logout(): void { this.authService.logout(); this.router.navigate(['/login']); }

  private async showSaved(): Promise<void> { const alert = await this.alertController.create({ header: 'Profil mis à jour', message: 'Vos informations ont été enregistrées.', buttons: ['OK'] }); await alert.present(); }
}
