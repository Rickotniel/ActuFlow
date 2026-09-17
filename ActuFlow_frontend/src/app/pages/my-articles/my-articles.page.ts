import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { Router } from '@angular/router';
import { Article, ArticleService } from '../../services/article.service';
import { AuthService } from '../../services/auth.service';

@Component({ selector: 'app-my-articles', templateUrl: './my-articles.page.html', styleUrls: ['./my-articles.page.scss'], standalone: false })
export class MyArticlesPage implements OnInit {
  articles: Article[] = [];
  activeTab: 'drafts' | 'published' = 'drafts';
  isLoading = true;
  errorMessage = '';

  constructor(private articleService: ArticleService, private authService: AuthService, private router: Router, private alertController: AlertController) {}

  get visibleArticles(): Article[] {
    return this.articles.filter(article => this.activeTab === 'published' ? article.statut === 'Publie' : article.statut !== 'Publie');
  }

  ngOnInit(): void { this.loadArticles(); }

  loadArticles(): void {
    this.articleService.getMyArticles().subscribe({
      next: articles => { this.articles = articles; this.isLoading = false; },
      error: () => { this.errorMessage = 'Impossible de charger vos articles.'; this.isLoading = false; }
    });
  }

  edit(article: Article): void { this.router.navigate(['/article-create'], { queryParams: { id: article.id_article } }); }

  async remove(article: Article): Promise<void> {
    const alert = await this.alertController.create({ header: 'Supprimer cet article ?', message: 'Cette action est définitive.', buttons: [{ text: 'Annuler', role: 'cancel' }, { text: 'Supprimer', role: 'destructive', handler: () => this.delete(article) }] });
    await alert.present();
  }

  private delete(article: Article): void {
    this.articleService.deleteArticle(article.id_article).subscribe({ next: () => this.articles = this.articles.filter(item => item.id_article !== article.id_article) });
  }

  logout(): void { this.authService.logout(); this.router.navigate(['/login']); }
}
