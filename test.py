import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

# Load CSV file
csv_file_path = r'D:\4 ARCHIVES\HBO Workbook - College\SIT\Academics\Semester 4\AI\AI ABL\Watched.csv'
df = pd.read_csv(csv_file_path)
desired_columns = ['Name', 'Tags', 'Rating']

def recommend_top_movies_by_genre(df, genre):
    genre_movies = df[df['Tags'].str.contains(genre, case=False, na=False)]

    if genre_movies.empty:
        explore_other_genres = messagebox.askyesno("No Movies Found", f"No movies found for the genre '{genre}'. Do you want to explore other genres?")
        if explore_other_genres:
            user_genre = simpledialog.askstring("Input", "Enter the genre you are interested in (e.g., Action, Comedy, Drama):")
            if user_genre:
                recommend_top_movies_by_genre(df, user_genre)
        return

    rated_genre_movies = genre_movies.dropna(subset=['Rating'])
    unrated_genre_movies = genre_movies[pd.isna(genre_movies['Rating'])]

    sorted_rated_genre_movies = rated_genre_movies.sort_values(by='Rating', ascending=False)

    result_text = ""
    if not sorted_rated_genre_movies.empty:
        result_text += f"Top Watched Movies Recommended in the Genre '{genre}':\n"
        result_text += sorted_rated_genre_movies.head(10)[desired_columns].to_string(index=False) + "\n\n"
    else:
        result_text += f"No top rated movies found for the genre '{genre}'.\n\n"

    if not unrated_genre_movies.empty:
        result_text += f"Unwatched Movies that are Recommended in the Genre '{genre}':\n"
        result_text += unrated_genre_movies[desired_columns].drop(columns=['Rating']).to_string(index=False) + "\n\n"

    result_box.delete('1.0', tk.END)
    result_box.insert(tk.END, result_text)

    if not unrated_genre_movies.empty:
        while True:
            movie_choice = simpledialog.askstring("Input", "Enter the name of the movie you want to watch (or type 'exit' to stop):")
            if movie_choice is None or movie_choice.lower() == 'exit':
                break

            selected_movie = genre_movies[genre_movies['Name'].str.contains(movie_choice, case=False, na=False)]

            if selected_movie.empty:
                messagebox.showinfo("Movie Not Found", f"Movie '{movie_choice}' not found in the list.")
                continue

            if pd.notna(selected_movie.iloc[0]['Rating']):
                rewatch_choice = messagebox.askyesno("Rewatch", f"Do you want to rewatch the movie '{selected_movie.iloc[0]['Name']}'?")
                if rewatch_choice:
                    new_rating = simpledialog.askstring("Update Rating", f"Enter new rating for '{selected_movie.iloc[0]['Name']}':")
                    if new_rating:
                        df.loc[selected_movie.index[0], 'Rating'] = new_rating
                        df.to_csv(csv_file_path, index=False)
                        messagebox.showinfo("Success", f"Rating for '{selected_movie.iloc[0]['Name']}' updated successfully to '{new_rating}' in the CSV file.")
                else:
                    messagebox.showinfo("Skip", "Okay, moving on.")
            else:
                new_rating = simpledialog.askstring("Rate Movie", f"Enter rating for the movie '{selected_movie.iloc[0]['Name']}':")
                if new_rating:
                    df.loc[selected_movie.index[0], 'Rating'] = new_rating
                    df.to_csv(csv_file_path, index=False)
                    messagebox.showinfo("Success", f"Rating for '{selected_movie.iloc[0]['Name']}' updated successfully to '{new_rating}' in the CSV file.")

def on_genre_submit():
    user_genre = genre_entry.get()
    if user_genre:
        recommend_top_movies_by_genre(df, user_genre)

app = tk.Tk()
app.title("Movie Recommendation System")

genre_label = tk.Label(app, text="Enter the genre you are interested in (e.g., Action, Comedy, Drama):")
genre_label.pack(pady=10)

genre_entry = tk.Entry(app, width=50)
genre_entry.pack(pady=5)

submit_button = tk.Button(app, text="Submit", command=on_genre_submit)
submit_button.pack(pady=10)

result_box = scrolledtext.ScrolledText(app, width=80, height=20)
result_box.pack(pady=20)

# Run the application
app.mainloop()
