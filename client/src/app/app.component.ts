import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';

interface Document {
  index: number;
  content: string;
  similarity: number;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule],
  template: `
    <div class="container">
      <div class="search-wrapper">
        <h1 class="title">Latent Semantic Analysis (LSA) Search Engine</h1>
        <div class="search-container">
          <input
            type="text"
            class="search-input"
            placeholder="Enter your search query"
            id="inputQuery"
          />
          <button class="search-button" (click)="handleClick()">
            Search
          </button>
        </div>
        
        <div *ngIf="isSearched" class="results-container">
          <h2>Search Results</h2>
          
          <div *ngIf="documents.length > 0" class="documents-list">
            <div *ngFor="let doc of documents" class="document-item">
              <p><strong>Document ID:</strong> {{ doc.index }}</p>
              <p><strong>Content:</strong> {{ doc.content }}</p>
              <p><strong>Similarity:</strong> {{ doc.similarity }}</p>
            </div>
          </div>

          <div *ngIf="graphUrl" class="graph-container">
            <img [src]="'http://127.0.0.1:8000' + graphUrl" alt="Graph Result" />
          </div>
          
          <div *ngIf="documents.length === 0" class="no-results">
            <p>No results found.</p>
          </div>
        </div>
      </div>
    </div>
  `,
  styleUrls: ['./app.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppController {
  searchQuery: string;
  isSearched: boolean;
  documents: Array<Document>;
  graphUrl: string | null;

  constructor() {
    this.searchQuery = '';
    this.isSearched = false;
    this.documents = [];
    this.graphUrl = null;
  }

  handleClick() {
    const inputElement = document.getElementById(
      'inputQuery'
    ) as HTMLInputElement;
    
    if (inputElement) {
      this.searchQuery = inputElement.value;
    }
    
    this.isSearched = true;
    
    async function getData(searchQuery: string) {
      const response = await fetch('http://127.0.0.1:8000/api/process_query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: searchQuery }),
      });
      
      const data = await response.json();
      
      return data;
    }
    
    getData(this.searchQuery).then((data) => {
      this.documents = data.results || [];
      this.graphUrl = data.graph_url || null;
    });
  }
}