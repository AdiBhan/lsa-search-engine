import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import matplotlib
import os
matplotlib.use('agg')

# Load the full 20 newsgroups dataset
newsgroups = fetch_20newsgroups(subset='all')
documents = newsgroups.data

vect = TfidfVectorizer(stop_words='english', max_features=5000)
X = vect.fit_transform(documents)

svd = TruncatedSVD(n_components=100)
X_reduced = svd.fit_transform(X)

def lsa_search(query: str, top_n: int = 5, max_chars:int=1000):

    ''' lsa_search performs Latent Semantic Analysis and returns top 5 documents with similarity rating
    and first max_words words'''

    query_vec = vect.transform([query])
    query_reduced = svd.transform(query_vec)
    doc_similarities = cosine_similarity(query_reduced, X_reduced)[0]
    
    top_indices = doc_similarities.argsort()[::-1][:top_n]
    top_similarities = doc_similarities[top_indices]
    
    results = []
    for idx, sim in zip(top_indices, top_similarities):
        results.append({
            'index': int(idx),
            'similarity': float(sim),
            'content': documents[idx][:max_chars] 
        })
    
    return results




def generate_sim_plot(search_results, filename='similarity_graph.png'):

    '''generate_sim_plot generates plot comparing similarity ratings across 5 different documents'''

    indices = [result['index'] for result in search_results]
    similarities = [result['similarity'] for result in search_results]
    
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(indices)), similarities, align='center')
    plt.title('Document Similarity to Query')
    plt.xlabel('Document Index')
    plt.ylabel('Cosine Similarity')
    plt.xticks(range(len(indices)), indices)
    plt.ylim(0, 1)  
    
    # Save the file to FastAPI's 'static' folder
    static_path = os.path.join('static')
    os.makedirs(static_path, exist_ok=True)
    
    filepath = os.path.join(static_path, filename)
    plt.savefig(filepath)
    plt.close()
    
    return filepath

    