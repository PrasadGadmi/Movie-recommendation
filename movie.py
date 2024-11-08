import pandas as pd

# Specify the path to your CSV file
csv_file_path = r'D:\033\Watched.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Select only the desired columns to display
desired_columns = ['Name', 'Tags', 'Rating']

# Display all movies with selected columns
print("All Movies:")
print(df[desired_columns].to_string(index=False))
print("=" * 50)  # Separator

# Function to recommend top movies from a specific genre
def recommend_top_movies_by_genre(df, genre):
    # Filter movies by the specified genre
    genre_movies = df[df['Tags'].str.contains(genre, case=False, na=False)]

    # Check if there are any movies in the specified genre
    if genre_movies.empty:
        explore_other_genres = input(f"No movies found for the genre '{genre}'. Do you want to explore other genres? (yes/no): ").strip().lower()
        if explore_other_genres == 'yes':
            user_genre = input("\nEnter the genre you are interested in (e.g., Action, Comedy, Drama): ")
            recommend_top_movies_by_genre(df, user_genre)
        return

    # Separate movies with and without ratings
    rated_genre_movies = genre_movies.dropna(subset=['Rating'])
    unrated_genre_movies = genre_movies[pd.isna(genre_movies['Rating'])]

    # Sort rated movies within the genre by rating in descending order
    sorted_rated_genre_movies = rated_genre_movies.sort_values(by='Rating', ascending=False)

    # Print top rated movies for the specified genre
    if not sorted_rated_genre_movies.empty:
        print(f"Top Watched Movies Recommended in the Genre '{genre}':")
        print(sorted_rated_genre_movies.head(10)[desired_columns].to_string(index=False))  # Display top 10 rated movies
    else:
        print(f"No top rated movies found for the genre '{genre}'.")

    print("\n" + "-" * 50 + "\n")  # Separator

    # Print unrated movies for the specified genre
    if not unrated_genre_movies.empty:
        print(f"Unwatched Movies that are Recommended in the Genre '{genre}':")
        print(unrated_genre_movies[desired_columns].drop(columns=['Rating']).to_string(index=False))  # Display unrated movies
        print("\n" + "-" * 50 + "\n")  # Separator

        # Prompt user to choose a movie from the unrated list
        while True:
            movie_choice = input("Enter the name of the movie you want to watch (or type 'exit' to stop): ").strip()

            if movie_choice.lower() == 'exit':
                break

            # Find the movie in the genre movies list (both rated and unrated)
            selected_movie = genre_movies[genre_movies['Name'].str.contains(movie_choice, case=False, na=False)]

            if selected_movie.empty:
                print(f"Movie '{movie_choice}' not found in the list.")
                continue

            # Check if the selected movie has a rating
            if pd.notna(selected_movie.iloc[0]['Rating']):
                rewatch_choice = input(f"Do you want to rewatch the movie '{selected_movie.iloc[0]['Name']}'? (yes/no): ").strip().lower()

                if rewatch_choice == 'yes':
                    print(f"Enjoy rewatching '{selected_movie.iloc[0]['Name']}'!")
                    update_rating_choice = input(f"Do you want to update the rating for '{selected_movie.iloc[0]['Name']}'? (yes/no): ").strip().lower()

                    if update_rating_choice == 'yes':
                        new_rating = input(f"Enter new rating for '{selected_movie.iloc[0]['Name']}': ").strip()
                        df.loc[selected_movie.index[0], 'Rating'] = new_rating
                        df.to_csv(csv_file_path, index=False)
                        print(f"Rating for '{selected_movie.iloc[0]['Name']}' updated successfully to '{new_rating}' in the CSV file.")
                elif rewatch_choice == 'no':
                    print(f"Okay, moving on.")
                else:
                    print("Invalid choice. Please enter 'yes' or 'no'.")
            else:
                # Prompt user to enter a rating for the unrated movie
                new_rating = input(f"Enter rating for the movie '{selected_movie.iloc[0]['Name']}': ").strip()
                # Update the DataFrame and CSV file with the new rating
                df.loc[selected_movie.index[0], 'Rating'] = new_rating
                df.to_csv(csv_file_path, index=False)
                print(f"Rating for '{selected_movie.iloc[0]['Name']}' updated successfully to '{new_rating}' in the CSV file.")
    else:
        print(f"No unrated movies found for the genre '{genre}'.")

# Prompt the user for a genre input
user_genre = input("\nEnter the genre you are interested in (e.g., Action, Comedy, Drama): ")

# Recommend top movies for the specified genre and handle movie selection
recommend_top_movies_by_genre(df, user_genre)
