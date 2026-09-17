import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertController, LoadingController } from '@ionic/angular';
import { Article, ArticleService, Category } from '../../services/article.service';

@Component({ selector: 'app-article-create', templateUrl: './article-create.page.html', styleUrls: ['./article-create.page.scss'], standalone: false })
export class ArticleCreatePage implements OnInit {
  articleId?: string;
  categories: Category[] = [];
  form = { titre: '', resume: '', contenu: '', id_categorie: '' };
  image?: File;
  isSaving = false;

  constructor(private route: ActivatedRoute, private router: Router, private articleService: ArticleService, private loadingController: LoadingController, private alertController: AlertController) {}

  ngOnInit(): void {
    this.articleService.getCategories().subscribe({ next: categories => this.categories = categories });
    this.articleId = this.route.snapshot.queryParamMap.get('id') || undefined;
    if (this.articleId) this.articleService.getArticle(this.articleId).subscribe({ next: article => this.form = { titre: article.titre, resume: article.resume || '', contenu: article.contenu, id_categorie: article.id_categorie || '' } });
  }

  selectImage(event: Event): void { this.image = (event.target as HTMLInputElement).files?.[0]; }

  save(status: 'Brouillon' | 'En attente'): void {
    if (!this.form.titre.trim() || !this.form.contenu.trim()) return;
    this.isSaving = true;
    const data = this.image ? new FormData() : { ...this.form, statut: status };
    if (data instanceof FormData) { data.append('titre', this.form.titre); data.append('resume', this.form.resume); data.append('contenu', this.form.contenu); data.append('statut', status); if (this.form.id_categorie) data.append('id_categorie', this.form.id_categorie); data.append('image_une', this.image!); }
    const request = this.articleId ? this.articleService.updateArticle(this.articleId, data) : this.articleService.createArticle(data);
    request.subscribe({ next: () => { this.isSaving = false; this.router.navigate(['/my-articles']); }, error: () => { this.isSaving = false; this.showError(); } });
  }

  async showError(): Promise<void> { const alert = await this.alertController.create({ header: 'Enregistrement impossible', message: 'Vérifiez les champs puis réessayez.', buttons: ['OK'] }); await alert.present(); }
  cancel(): void { this.router.navigate(['/my-articles']); }
}
