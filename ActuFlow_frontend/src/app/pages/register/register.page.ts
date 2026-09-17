import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AlertController, LoadingController } from '@ionic/angular';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
  standalone: false,
})
export class RegisterPage {
  registerForm: FormGroup;
  isSubmitted = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private alertController: AlertController,
    private loadingController: LoadingController
  ) {
    this.registerForm = this.fb.group(
      {
        first_name: ['', [Validators.required]],
        last_name: ['', [Validators.required]],
        email: ['', [Validators.required, Validators.email]],
        password: ['', [Validators.required, Validators.minLength(6)]],
        confirmPassword: ['', [Validators.required]],
        terms: [false, [Validators.requiredTrue]]
      },
      {
        validators: this.passwordMatchValidator
      }
    );
  }

  passwordMatchValidator(form: FormGroup) {
    const password = form.get('password');
    const confirmPassword = form.get('confirmPassword');

    if (password && confirmPassword && password.value !== confirmPassword.value) {
      confirmPassword.setErrors({ passwordMismatch: true });
      return { passwordMismatch: true };
    }
    return null;
  }

  get f() {
    return this.registerForm.controls;
  }

  async onSubmit(): Promise<void> {
    this.isSubmitted = true;

    if (this.registerForm.invalid) {
      return;
    }

    const loading = await this.loadingController.create({
      message: 'Création du compte en cours...',
      spinner: 'crescent'
    });
    await loading.present();

    const formData = this.registerForm.value;

    const userData = {
      email: formData.email,
      password: formData.password,
      prenom: formData.first_name,
      nom: formData.last_name
    };

    this.authService.register(userData).subscribe({
      next: () => {
        loading.dismiss();
        this.showSuccessAlert();
      },
      error: async (err) => {
        loading.dismiss();
        let errorMessage = 'Erreur lors de l\'inscription. Veuillez réessayer.';

        if (err.status === 400) {
          if (err.error?.email) {
            errorMessage = Array.isArray(err.error.email) ? err.error.email[0] : 'Cet email est déjà utilisé.';
          } else if (err.error?.password) {
            errorMessage = Array.isArray(err.error.password) ? err.error.password[0] : 'Mot de passe invalide.';
          } else {
            errorMessage = 'Veuillez vérifier les informations saisies.';
          }
        } else if (err.status === 0) {
          errorMessage = 'Impossible de contacter le serveur. Vérifiez votre connexion.';
        }

        const alert = await this.alertController.create({
          header: 'Erreur d\'inscription',
          message: errorMessage,
          buttons: ['OK'],
          cssClass: 'alert-danger'
        });
        await alert.present();
      }
    });
  }

  async showSuccessAlert(): Promise<void> {
    const alert = await this.alertController.create({
      header: 'Inscription réussie !',
      message: 'Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.',
      buttons: [
        {
          text: 'Se connecter',
          handler: () => {
            this.router.navigate(['/login']);
          }
        }
      ],
      backdropDismiss: false,
      cssClass: 'alert-success'
    });
    await alert.present();
  }
}