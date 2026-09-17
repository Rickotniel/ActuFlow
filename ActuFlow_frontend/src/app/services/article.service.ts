import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Category {
  id_categorie: string;
  nom: string;
  slug: string;
  couleur?: string;
}

export interface Article {
  id_article: string;
  titre: string;
  slug: string;
  resume?: string;
  contenu: string;
  image_une?: string;
  statut: string;
  nombre_vues: number;
  date_publication?: string;
  date_creation: string;
  date_modification: string;
  id_utilisateur: string;
  id_categorie?: string;
}

export interface Comment {
  id_commentaire: string;
  contenu: string;
  date_creation: string;
  id_utilisateur: string;
  id_article: string;
}

export interface ArticlePage {
  count: number;
  page: number;
  num_pages: number;
  results: Article[];
}

@Injectable({ providedIn: 'root' })
export class ArticleService {
  private readonly apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getArticles(page = 1, search = '', categoryId = ''): Observable<ArticlePage> {
    let params = new HttpParams().set('page', page).set('page_size', 9);
    if (search.trim()) params = params.set('search', search.trim());
    if (categoryId) params = params.set('id_categorie', categoryId);
    return this.http.get<ArticlePage>(`${this.apiUrl}/articles/`, { params });
  }

  getCategories(): Observable<Category[]> {
    return this.http.get<Category[] | { results: Category[] }>(`${this.apiUrl}/categories/`)
      .pipe(mapResponse);
  }

  getArticle(id: string): Observable<Article> {
    return this.http.get<Article>(`${this.apiUrl}/articles/${id}/`);
  }

  getMyArticles(): Observable<Article[]> {
    return this.http.get<Article[] | { results: Article[] }>(`${this.apiUrl}/articles/mine/`)
      .pipe(mapResponse);
  }

  createArticle(data: FormData | Partial<Article>): Observable<Article> {
    return this.http.post<Article>(`${this.apiUrl}/articles/`, data);
  }

  updateArticle(id: string, data: FormData | Partial<Article>): Observable<Article> {
    return this.http.patch<Article>(`${this.apiUrl}/articles/${id}/`, data);
  }

  deleteArticle(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/articles/${id}/`);
  }

  getComments(articleId: string): Observable<Comment[]> {
    const params = new HttpParams().set('id_article', articleId).set('ordering', '-date_creation');
    return this.http.get<Comment[] | { results: Comment[] }>(`${this.apiUrl}/commentaires/`, { params })
      .pipe(mapResponse);
  }

  addComment(articleId: string, contenu: string): Observable<Comment> {
    return this.http.post<Comment>(`${this.apiUrl}/commentaires/`, { id_article: articleId, contenu });
  }

  getLikes(articleId: string): Observable<{ id: string; id_utilisateur: string; id_article: string }[]> {
    const params = new HttpParams().set('id_article', articleId);
    return this.http.get<{ id: string; id_utilisateur: string; id_article: string }[]>(`${this.apiUrl}/likes/`, { params })
      .pipe(mapResponse);
  }

  addLike(articleId: string): Observable<unknown> {
    return this.http.post(`${this.apiUrl}/likes/`, { id_article: articleId });
  }

  removeLike(likeId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/likes/${likeId}/`);
  }
}

import { map } from 'rxjs';

const mapResponse = map((response: any) => Array.isArray(response) ? response : response.results);
