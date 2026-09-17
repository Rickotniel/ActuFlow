import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AlertController, LoadingController } from '@ionic/angular';
import { Article, ArticleService, Comment } from '../../services/article.service';
import { AuthService } from '../../services/auth.service';
import { finalize, timeout } from 'rxjs';

@Component({
  selector: 'app-article-detail',
  templateUrl: './article-detail.page.html',
  styleUrls: ['./article-detail.page.scss'],
  standalone: false
})
export class ArticleDetailPage implements OnInit {
  article?: Article;
  comments: Comment[] = [];
  commentText = '';
  likesCount = 0;
  currentLikeId?: string;
  isLoading = true;
  errorMessage = '';

  constructor(
    private route: ActivatedRoute,
    private articleService: ArticleService,
    private authService: AuthService,
    private loadingController: LoadingController,
    private alertController: AlertController
  ) {}

  get isAuthenticated(): boolean { return this.authService.isAuthenticated(); }
  get currentUserId(): string | undefined { return this.authService.currentUserValue?.id_utilisateur; }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) { this.errorMessage = 'Article introuvable.'; this.isLoading = false; return; }
    this.articleService.getArticle(id).pipe(
      timeout(10000),
      finalize(() => this.isLoading = false)
    ).subscribe({
      next: article => { this.article = article; this.loadInteractions(id); },
      error: error => this.errorMessage = error.name === 'TimeoutError'
        ? 'Le serveur met trop de temps à répondre. Réessayez.'
        : 'Cet article est indisponible.'
    });
  }

  loadInteractions(articleId: string): void {
    this.articleService.getComments(articleId).subscribe({ next: comments => this.comments = comments });
    this.articleService.getLikes(articleId).subscribe({
      next: likes => { this.likesCount = likes.length; this.currentLikeId = likes.find(like => like.id_utilisateur === this.currentUserId)?.id; }
    });
  }

  toggleLike(): void {
    if (!this.article || !this.isAuthenticated) { this.showLoginMessage(); return; }
    const request = this.currentLikeId
      ? this.articleService.removeLike(this.currentLikeId)
      : this.articleService.addLike(this.article.id_article);
    request.subscribe({ next: () => this.loadInteractions(this.article!.id_article) });
  }

  async addComment(): Promise<void> {
    if (!this.article || !this.isAuthenticated) { this.showLoginMessage(); return; }
    const contenu = this.commentText.trim();
    if (!contenu) return;
    const loading = await this.loadingController.create({ message: 'Publication du commentaire...', spinner: 'crescent' });
    await loading.present();
    this.articleService.addComment(this.article.id_article, contenu).subscribe({
      next: comment => { this.comments = [comment, ...this.comments]; this.commentText = ''; loading.dismiss(); },
      error: async () => { loading.dismiss(); const alert = await this.alertController.create({ header: 'Commentaire non publié', message: 'Veuillez réessayer dans un instant.', buttons: ['OK'] }); await alert.present(); }
    });
  }

  showLoginMessage(): void {
    this.alertController.create({ header: 'Connexion requise', message: 'Connectez-vous pour aimer un article ou écrire un commentaire.', buttons: ['OK'] }).then(alert => alert.present());
  }
}
