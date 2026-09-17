import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AlertController, LoadingController } from '@ionic/angular';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {
  loginForm: FormGroup;
  isSubmitted = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private alertController: AlertController,
    private loadingController: LoadingController
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  ngOnInit() {}

  async onSubmit() {
    this.isSubmitted = true;

    if (this.loginForm.invalid) {
      return;
    }

    const loading = await this.loadingController.create({
      message: 'Connexion en cours...',
      spinner: 'crescent'
    });
    await loading.present();

    const { email, password } = this.loginForm.value;

    this.authService.login(email, password).subscribe({
      next: () => {
        loading.dismiss();
        this.router.navigate(['/home'], { replaceUrl: true });
      },
      error: async (err) => {
        loading.dismiss();
        let errorMessage = 'Erreur de connexion. Veuillez réessayer.';
        
        if (err.status === 401) {
          errorMessage = 'Email ou mot de passe incorrect.';
        } else if (err.status === 400) {
          errorMessage = 'Veuillez vérifier vos identifiants.';
        } else if (err.status === 0) {
          errorMessage = 'Impossible de contacter le serveur. Vérifiez votre connexion.';
        }

        const alert = await this.alertController.create({
          header: 'Erreur de connexion',
          message: errorMessage,
          buttons: ['OK'],
          cssClass: 'alert-danger'
        });
        await alert.present();
      }
    });
  }

  // Getter pour faciliter l'accès aux champs dans le template
  get f() {
    return this.loginForm.controls;
  }
}