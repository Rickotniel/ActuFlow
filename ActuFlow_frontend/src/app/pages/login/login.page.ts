import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertController, LoadingController } from '@ionic/angular';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: false,
})
export class LoginPage implements OnInit {
  loginForm: FormGroup;
  isSubmitted = false;
  returnUrl = '/home';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute,
    private alertController: AlertController,
    private loadingController: LoadingController
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      rememberMe: [false]
    });
  }

  ngOnInit(): void {
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/home';
    if (this.authService.isAuthenticated()) {
      this.router.navigateByUrl(this.returnUrl);
    }
  }

  get f() {
    return this.loginForm.controls;
  }

  async onSubmit(): Promise<void> {
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
        this.router.navigateByUrl(this.returnUrl);
      },
      error: async (err) => {
        loading.dismiss();
        let errorMessage = 'Identifiants invalides ou problème de connexion.';

        if (err.status === 401) {
          errorMessage = 'Email ou mot de passe incorrect.';
        } else if (err.status === 0) {
          errorMessage = 'Impossible de joindre le serveur. Vérifiez votre connexion.';
        } else if (err.error?.detail) {
          errorMessage = err.error.detail;
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
}
