from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)
similarity_df = pickle.load(open('similarity.pkl', 'rb'))
df_filtered = pickle.load(open('df_filtered.pkl', 'rb'))
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    book_title = request.form['book_title']
    isbn = df_filtered[df_filtered['title'] == book_title]['isbn'].values[0]
    similar_books = similarity_df[isbn].sort_values(ascending=False)
    similar_books = similar_books[similar_books.index != isbn].head(5)
    recommended = df_filtered[df_filtered['isbn'].isin(similar_books.index)][['title']].drop_duplicates()
    books_list = recommended['title'].tolist()
    return render_template('index.html', books=books_list)

if __name__ == '__main__':
    app.run(debug=True)