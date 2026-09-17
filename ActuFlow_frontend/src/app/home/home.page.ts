import { Component, OnInit } from '@angular/core';
import { Article, ArticleService, Category } from '../services/article.service';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { Subject, debounceTime, distinctUntilChanged, finalize, timeout } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: false,
})
export class HomePage implements OnInit {
  articles: Article[] = [];
  categories: Category[] = [];
  search = '';
  selectedCategory = '';
  page = 1;
  totalPages = 1;
  isLoading = true;
  errorMessage = '';
  categoriesError = '';
  private searchSubject = new Subject<string>();

  constructor(private articleService: ArticleService, private authService: AuthService, private router: Router) {}

  get currentUser() { return this.authService.currentUserValue; }
  get canWrite(): boolean {
    return this.authService.hasRole('Redacteur') || this.authService.hasRole('Administrateur');
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  ngOnInit(): void {
    this.searchSubject.pipe(
      debounceTime(350),
      distinctUntilChanged()
    ).subscribe(() => this.loadArticles(1));
    this.loadCategories();
    this.loadArticles();
  }

  loadCategories(): void {
    this.articleService.getCategories().pipe(timeout(8000)).subscribe({
      next: categories => this.categories = categories,
      error: () => this.categoriesError = 'Les catégories sont momentanément indisponibles.'
    });
  }

  loadArticles(page = 1): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.articleService.getArticles(page, this.search, this.selectedCategory).pipe(
      timeout(10000),
      finalize(() => this.isLoading = false)
    ).subscribe({
      next: response => {
        this.articles = response.results;
        this.page = response.page;
        this.totalPages = response.num_pages;
      },
      error: error => this.errorMessage = error.name === 'TimeoutError'
        ? 'Le serveur met trop de temps à répondre. Réessayez.'
        : 'Les articles ne peuvent pas être chargés pour le moment.'
    });
  }

  searchArticles(): void { this.searchSubject.next(this.search); }
  selectCategory(categoryId: string): void { this.selectedCategory = categoryId; this.loadArticles(1); }
  previousPage(): void { if (this.page > 1) this.loadArticles(this.page - 1); }
  nextPage(): void { if (this.page < this.totalPages) this.loadArticles(this.page + 1); }
}
