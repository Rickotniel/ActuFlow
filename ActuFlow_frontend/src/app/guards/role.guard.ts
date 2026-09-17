import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class RoleGuard implements CanActivate {

  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
      return false;
    }

    const expectedRoles: string[] = route.data['roles'];
    if (!expectedRoles || expectedRoles.length === 0) {
      return true;
    }

    const hasPermission = expectedRoles.some(role => this.authService.hasRole(role));
    if (!hasPermission) {
      this.router.navigate(['/home']);
      return false;
    }

    return true;
  }
}
