import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';
import { RoleGuard } from './guards/role.guard';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    loadChildren: () => import('./home/home.module').then(m => m.HomePageModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'login',
    loadChildren: () => import('./pages/login/login.module').then(m => m.LoginPageModule)
  },
  {
    path: 'register',
    loadChildren: () => import('./pages/register/register.module').then(m => m.RegisterPageModule)
  },
  {
    path: 'article/:id',
    loadChildren: () => import('./pages/article-detail/article-detail.module').then(m => m.ArticleDetailPageModule)
  },
  {
    path: 'profile',
    canActivate: [AuthGuard],
    loadChildren: () => import('./pages/profile/profile.module').then(m => m.ProfilePageModule)
  },
  {
    path: 'my-articles',
    canActivate: [RoleGuard],
    data: { roles: ['Redacteur', 'Administrateur'] },
    loadChildren: () => import('./pages/my-articles/my-articles.module').then(m => m.MyArticlesPageModule)
  },
  {
    path: 'article-create',
    canActivate: [RoleGuard],
    data: { roles: ['Redacteur', 'Administrateur'] },
    loadChildren: () => import('./pages/article-create/article-create.module').then(m => m.ArticleCreatePageModule)
  },
  {
    path: '**',
    redirectTo: 'home',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      // enableTracing: true   // Décommentez pour déboguer les routes
    })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }