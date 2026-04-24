'''
analyze_data.py - analysis

1. Rating Analysis:
    What's the correlation between TMDB and IMDb ratings?
    Distribution of ratings on each platform
2. Genre Analysis:
    Most common genres
    Average ratings by genre
3. Temporal Analysis:
    Rating trends over time
    Most productive years

Generate at least 3 visualizations and a summary report with interesting insights or patterns.
'''

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import logging
from typing import Dict

class DataAnalyzer:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        os.makedirs('outputs', exist_ok=True)

        logging.basicConfig(
            filename='logs/analyze_data.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def load_processed_data(self) -> pd.DataFrame:
        """Load processed movie data from CSV"""
        filepath = os.path.join('data', 'processed_movies.csv')
        try:
            df = pd.read_csv(filepath)
            logging.info(f'Loaded processed data: {len(df)} records')
            return df
        except Exception as e:
            logging.error(f'Error loading processed data: {e}')
            return pd.DataFrame()
        
    def rating_analysis(self, df):
        """Analyze correlation and distribution between TMDB and IMDb ratings"""
        results = {}

        if 'tmdb_rating' not in df.columns or 'imdb_rating' not in df.columns:
            logging.warning('Rating columns missing, skipping rating analysis')
            return results
        
        dist_df = df.copy()
        try:
            #Analyze correlation
            corr = dist_df['tmdb_rating'].corr(dist_df['imdb_rating'])
            results['correlation'] = round(corr,3)

            #Analyze distribution by statistical values 
            stat_labels = dist_df['tmdb_rating'].describe().index.tolist()
            tmdb_stats = dist_df['tmdb_rating'].describe().values.tolist()
            imdb_stats = dist_df['imdb_rating'].describe().values.tolist()
            for i, stat in enumerate(stat_labels):
                results[f'tmdb_{stat}'] = round(tmdb_stats[i],3)
                results[f'imdb_{stat}'] = round(imdb_stats[i],3)
            logging.info(f'Successfully analyzed TMDB vs IMDb distributions: r={corr:.3f}.')
            return results
        except Exception as e:
            logging.error(f'Error analyzing ratings: {e}')
            return results
    
    def genre_analysis(self, df):
        """Analyze most common genres and average ratings by genre"""
        results = {}

        if 'genres' not in df.columns:
            logging.warning('Genre column missing, skipping genre analysis')
            return results
        
        genre_df = df.copy()

        #Clean genres column for genre analysis
        try:
            #Convert comma-separated string to list for explode                                                                                                                           
            genre_df['genres'] = genre_df['genres'].apply(            
                lambda x: x.split(', ') if isinstance(x, str) else x                                                                                                                      
            )
            #Explode genre list to rows of subset columns -> one row per movie-genre pair
            genre_df = genre_df.explode('genres') 

            #Extract genre name from each genre dictionary
            genre_df['genre_name'] = genre_df['genres'].apply(
                lambda x: x.get('name') if isinstance(x,dict) else x
            )

            #Drop rows with missing/empty genres
            genre_df = genre_df.dropna(subset=['genre_name'])
        except Exception as e:
            logging.error(f'Error cleaning genres column for genre analysis: {e}')
            return results

        #Genre analysis

        #Analyze most common genres
        try:
            genre_counts = genre_df['genre_name'].value_counts()
            results['top_genres'] = genre_counts.head(10).to_dict()
            logging.info(f'Successfully analyzed top genres')
        except Exception as e:
            logging.error(f'Error analyzing top genres: {e}')
            return results
        
        #Analyze average ratings by genre
        if 'tmdb_rating' not in df.columns or 'imdb_rating' not in df.columns:
            logging.warning('Rating columns missing, skipping average ratings by genre analysis')
            return results
        try:
            tmdb_ave = genre_df.groupby('genre_name')['tmdb_rating'].mean().sort_values(ascending=False)
            imdb_ave = genre_df.groupby('genre_name')['imdb_rating'].mean().sort_values(ascending=False)
            results['avg_tmdb_by_genre'] = tmdb_ave.round(3).to_dict()
            results['avg_imdb_by_genre'] = imdb_ave.round(3).to_dict()
            logging.info(f'Successfully analyzed average ratings by genre')
            return results
        except Exception as e:
            logging.error(f'Error analyzing average rating by genre: {e}')
            return results

    def temporal_analysis(self, df):
        """Analyze rating trends over time and most productive years"""
        results = {}

        if 'release_date' not in df.columns:
            logging.warning('Release date column missing, skipping temporal analysis')
            return results
        
        temp_df = df.copy()

        #Clean release_date column
        try:
            temp_df['release_date'] = pd.to_datetime(temp_df['release_date'], errors='coerce')
            temp_df['year'] = temp_df['release_date'].dt.year
            temp_df = temp_df[temp_df['year'].notna()]
        except Exception as e:
            logging.error(f'Error cleaning release_date column for temporal analysis: {e}')
            return results
        
        #Start temporal analysis
        movies_per_yr = temp_df['year'].value_counts().sort_index()
        if 'tmdb_rating' not in df.columns or 'imdb_rating' not in df.columns:
            logging.warning('Rating columns missing, skipping average rating trends analysis')
            return results
        try:
            tmdb_by_yr = temp_df.groupby('year')['tmdb_rating'].mean().round(3)
            imdb_by_yr = temp_df.groupby('year')['imdb_rating'].mean().round(3)
            results['tmdb_rating_by_year'] = tmdb_by_yr.to_dict()
            results['imdb_rating_by_year'] = imdb_by_yr.to_dict()
            results['most_productive_year'] = int(movies_per_yr.idxmax())
            logging.info(f'Temporal analysis: {len(movies_per_yr)} years covered')
            return results
        except Exception as e:
            logging.error(f'Error analyzing temporal trends: {e}')
            return results
        
    def generate_visualizations(self, df: pd.DataFrame):
        """Generate visualizations"""

        #Visualization 1: rating distributions side by side
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        if 'tmdb_rating' in df.columns:
            df['tmdb_rating'].dropna().hist(bins=20, ax=axes[0], color='steelblue', edgecolor='white')
            axes[0].set_title('TMDB Rating Distribution')
            axes[0].set_xlabel('Rating')
            axes[0].set_ylabel('Count')

        if 'imdb_rating' in df.columns:
            df['imdb_rating'].dropna().hist(bins=20, ax=axes[1], color='goldenrod', edgecolor='white')
            axes[1].set_title('IMDb Rating Distribution')
            axes[1].set_xlabel('Rating')
            axes[1].set_ylabel('Count')

        plt.tight_layout()
        path = os.path.join('outputs', 'rating_distributions.png')
        try:
            plt.savefig(path)
            logging.info(f'Saved rating distribution visualization: {path}')
        except Exception as e:
            logging.error(f'Error saving {path}: {e}')
        plt.close()

        #Visualization 2: TMDB vs IMDb rating correlation
        if 'tmdb_rating' in df.columns and 'imdb_rating' in df.columns:
            scatter_df = df[['tmdb_rating','imdb_rating']].dropna()
            plt.figure(figsize=(8, 6))
            plt.scatter(scatter_df['tmdb_rating'], scatter_df['imdb_rating'], alpha=0.5, color='steelblue')
            plt.xlabel('TMDB Rating')
            plt.ylabel('IMDb Rating')
            plt.title('TMDB vs IMDb Rating Correlation')
            path = os.path.join('outputs', 'rating_correlation.png')
            try:
                plt.savefig(path)
                logging.info(f'Saved visualization: {path}')
            except Exception as e:
                logging.error(f'Error saving {path}: {e}')
            plt.close()
        
        #Visualization 3: most common genres bar plot
        genre_results = self.genre_analysis(df)
        top_genres = genre_results.get('top_genres', {})
        if top_genres:
            plt.figure(figsize=(10, 6))
            plt.bar(top_genres.keys(), top_genres.values(), color='steelblue', edgecolor='white')
            plt.title('Most Common Genres')
            plt.xlabel('Genre')
            plt.ylabel('Number of Movies')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            path = os.path.join('outputs', 'genre_distribution.png')
            try:
                plt.savefig(path)
                logging.info(f'Saved visualization: {path}')
            except Exception as e:
                logging.error(f'Error saving {path}: {e}')
            plt.close()

        #Visualization 4: average TMDB and IMDb ratings by year
        temporal_results = self.temporal_analysis(df)
        tmdb_by_yr = temporal_results.get('tmdb_rating_by_year', {})
        imdb_by_yr = temporal_results.get('imdb_rating_by_year', {})
        if tmdb_by_yr or imdb_by_yr:
            plt.figure(figsize=(12, 5))
            if tmdb_by_yr:
                plt.plot(list(tmdb_by_yr.keys()), list(tmdb_by_yr.values()), color='steelblue', marker='o', markersize=4, label='TMDB')
            if imdb_by_yr:
                plt.plot(list(imdb_by_yr.keys()), list(imdb_by_yr.values()), color='goldenrod', marker='o', markersize=4, label='IMDb')
            plt.title('Average Ratings by Year')
            plt.xlabel('Year')
            plt.ylabel('Average Rating')
            plt.legend()
            plt.tight_layout()
            path = os.path.join('outputs', 'ratings_by_year.png')
            try:
                plt.savefig(path)
                logging.info(f'Saved visualization: {path}')
            except Exception as e:
                logging.error(f'Error saving {path}: {e}')
            plt.close()

    
    def generate_summary(self, rating_results: Dict, genre_results: Dict, temporal_results: Dict):
        """Generate summary report"""
        lines = [
            'Movie Data Analysis - Summary Report',
            '=' * 40,
            '',
            '--- Rating Analysis ---',
        ]

        if rating_results:
            lines += [
                f"TMDB mean rating:      {rating_results.get('tmdb_mean', 'N/A')}",
                f"IMDb mean rating:      {rating_results.get('imdb_mean', 'N/A')}",
                f"TMDB std deviation:    {rating_results.get('tmdb_std', 'N/A')}",
                f"IMDb std deviation:    {rating_results.get('imdb_std', 'N/A')}",
                f"TMDB-IMDb correlation: {rating_results.get('correlation', 'N/A')}",
            ]
            corr = rating_results.get('correlation')
            if corr is not None:
                if corr > 0.7:
                    lines.append('TMDB and IMDb ratings are strongly correlated — both platforms rate movies similarly.')
                elif corr > 0.4:
                    lines.append('TMDB and IMDb ratings show moderate correlation — some divergence exists between platforms.')
                else:
                    lines.append('TMDB and IMDb ratings are weakly correlated — the platforms differ significantly in their ratings.')

        lines += ['', '--- Genre Analysis ---']

        if genre_results:
            top_genres = genre_results.get('top_genres', {})
            if top_genres:
                top_genre = list(top_genres.keys())[0]
                lines.append(f"Most common genre: {top_genre} ({top_genres[top_genre]} movies)")
                lines.append('Top 5 genres by count:')
                for genre, count in list(top_genres.items())[:5]:
                    lines.append(f"  {genre}: {count}")
            avg_tmdb = genre_results.get('avg_tmdb_by_genre', {})
            if avg_tmdb:
                top_rated = list(avg_tmdb.keys())[0]
                lines.append(f"Highest rated genre (TMDB avg): {top_rated} ({avg_tmdb[top_rated]})")
            avg_imdb = genre_results.get('avg_imdb_by_genre', {})
            if avg_imdb:
                top_rated_imdb = list(avg_imdb.keys())[0]
                lines.append(f"Highest rated genre (IMDb avg): {top_rated_imdb} ({avg_imdb[top_rated_imdb]})")

        lines += ['', '--- Temporal Analysis ---']

        if temporal_results:
            most_productive = temporal_results.get('most_productive_year')
            if most_productive:
                lines.append(f"Most productive year: {most_productive}")
            tmdb_by_yr = temporal_results.get('tmdb_rating_by_year', {})
            if tmdb_by_yr:
                best_yr = max(tmdb_by_yr, key=tmdb_by_yr.get)
                lines.append(f"Highest rated year (TMDB avg): {best_yr} ({tmdb_by_yr[best_yr]})")
            imdb_by_yr = temporal_results.get('imdb_rating_by_year', {})
            if imdb_by_yr:
                best_yr_imdb = max(imdb_by_yr, key=imdb_by_yr.get)
                lines.append(f"Highest rated year (IMDb avg): {best_yr_imdb} ({imdb_by_yr[best_yr_imdb]})")

        report_path = os.path.join('outputs', 'summary_report.txt')
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            logging.info(f'Saved summary report to {report_path}')
        except Exception as e:
            logging.error(f'Error saving summary report: {e}')

    def run_pipeline(self):
        """Run full data analysis pipeline"""
        df = self.load_processed_data() #load processed data
        if df.empty:
            logging.error('No data loaded to analyze, interrupting pipeline run')
            return
        
        rating_results = self.rating_analysis(df)
        genre_results = self.genre_analysis(df)
        temporal_results = self.temporal_analysis(df)

        self.generate_visualizations(df)
        self.generate_summary(rating_results,genre_results,temporal_results)

        logging.info('Analysis completed successfully')

