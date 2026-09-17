import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, catchError, switchMap, tap, throwError } from 'rxjs';
import { environment } from '../../environments/environment';

export interface UserProfile {
  id_utilisateur: string;
  email: string;
  prenom: string;
  nom: string;
  biographie?: string;
  photo_profil?: string;
  est_actif: boolean;
  is_staff: boolean;
  date_creation: string;
  date_modification: string;
  roles: string[];
  role_names: string[];
  token?: string;
  refresh?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl;
  private currentUserSubject = new BehaviorSubject<UserProfile | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadUserFromStorage();
  }

  public get currentUserValue(): UserProfile | null {
    return this.currentUserSubject.value;
  }

  private loadUserFromStorage(): void {
    const stored = localStorage.getItem('currentUser');
    if (stored) {
      try {
        const user = JSON.parse(stored);
        this.currentUserSubject.next(user);
      } catch (e) {
        localStorage.removeItem('currentUser');
      }
    }
  }

  register(userData: { email: string; password: string; prenom: string; nom: string; biographie?: string }): Observable<UserProfile> {
    return this.http.post<UserProfile>(`${this.apiUrl}/utilisateurs/`, userData);
  }

  login(email: string, password: string): Observable<UserProfile> {
    return this.http.post<{ access: string; refresh: string }>(`${this.apiUrl}/token/`, { email, password }).pipe(
      tap(tokens => {
        // Enregistrer temporairement le token pour que le JwtInterceptor puisse l'inclure dans la requête me/
        const tempUser: any = { token: tokens.access, refresh: tokens.refresh, email };
        localStorage.setItem('currentUser', JSON.stringify(tempUser));
        this.currentUserSubject.next(tempUser);
      }),
      switchMap(tokens =>
        this.http.get<UserProfile>(`${this.apiUrl}/utilisateurs/me/`, {
          headers: { Authorization: `Bearer ${tokens.access}` }
        }).pipe(
          tap(profile => {
            const completeUser: UserProfile = {
              ...profile,
              token: tokens.access,
              refresh: tokens.refresh
            };
            localStorage.setItem('currentUser', JSON.stringify(completeUser));
            this.currentUserSubject.next(completeUser);
          })
        )
      )
    );
  }

  getProfile(): Observable<UserProfile> {
    return this.http.get<UserProfile>(`${this.apiUrl}/utilisateurs/me/`).pipe(
      tap(profile => {
        const current = this.currentUserValue;
        if (current) {
          const updated = { ...current, ...profile };
          localStorage.setItem('currentUser', JSON.stringify(updated));
          this.currentUserSubject.next(updated);
        }
      }),
      catchError(error => {
        if (error.status === 401) {
          this.logout();
        }
        return throwError(() => error);
      })
    );
  }

  updateProfile(data: Partial<Pick<UserProfile, 'prenom' | 'nom' | 'biographie' | 'photo_profil'>> | FormData): Observable<UserProfile> {
    return this.http.patch<UserProfile>(`${this.apiUrl}/utilisateurs/me/`, data).pipe(
      tap(profile => {
        const updated = { ...this.currentUserValue, ...profile } as UserProfile;
        localStorage.setItem('currentUser', JSON.stringify(updated));
        this.currentUserSubject.next(updated);
      })
    );
  }

  logout(): void {
    localStorage.removeItem('currentUser');
    this.currentUserSubject.next(null);
  }

  getToken(): string | null {
    const user = this.currentUserValue;
    return user ? (user.token || null) : null;
  }

  isAuthenticated(): boolean {
    const user = this.currentUserValue;
    return !!(user && user.token);
  }

  hasRole(roleName: string): boolean {
    const user = this.currentUserValue;
    if (!user) return false;
    if (user.is_staff) return true;
    return user.role_names ? user.role_names.includes(roleName) : false;
  }
}
