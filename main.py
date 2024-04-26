from scraper import load_articles
from sentiment_analysis import load_data, calculate_performance_score, compute_performance_scores
from mlb_api import get_braves_runs, get_next_game_runs

# Load the team data
team_data_2010 = load_data('Data/Atlanta Falcons Batting Data 2010.xlsx', 'excel')
team_data_2020 = load_data('Data/Atlanta Falcons Batting Data 2020.xlsx', 'excel')

# Calculate initial and final performance scores
initial_score_2010 = calculate_performance_score(team_data_2010, 'r')
final_score_2020 = calculate_performance_score(team_data_2020, 'r')

# Load articles from URLs
article_urls = [
    'https://www.masslive.com/sports/2010/10/errors_cost_atlanta_braves_gam.html',
    'https://sabr.org/gamesproj/game/august-6-2010-giants-beat-braves-3-2-in-extra-innings-on-tom-glavine-night/',
    'https://www.denverpost.com/2010/08/25/rockies-rally-from-9-run-deficit-to-beat-the-braves-12-10/',
    'https://www.baseball-reference.com/boxes/ATL/ATL201008280.shtml',
    'https://www.cbsnews.com/losangeles/news/fading-dodgers-fall-to-1st-place-braves-1-0/',
    
    # Add more URLs as needed
]
article_data = load_articles(article_urls)

# Adjust performance score based on sentiment analysis of articles
adjusted_df = compute_performance_scores(article_data, 'Article', initial_score_2010)

# Print the results
print("Adjusted Performance Scores:")
print(adjusted_df[['Title', 'ArticleSentiment', 'AdjustedPerformanceScore']])

#  Get the number of runs scored by the Braves from October 1st, 2010, to October 31st, 2010
start_date = "2010-08-01"
end_date = "2010-08-31"
api_key = "d188ff5e56msh3d1ada84cbbc849p1c6eccjsn0183e27eb227"
braves_games, total_runs = get_braves_runs(start_date, end_date, api_key)

# Calculate the average runs scored by the Braves during the given time period
avg_runs = total_runs / len(braves_games)

# Predict the number of runs for the Braves' next game after the end date
adjusted_score = adjusted_df['AdjustedPerformanceScore'].mean()
predicted_runs = max(0, round(avg_runs * (1 + adjusted_score / 100)))
print(f"\nPredicted Runs for the Next Game: {predicted_runs}")

# Get the actual number of runs scored by the Braves in their next game after the end date
actual_runs, next_game_date = get_next_game_runs(end_date, api_key)
if actual_runs is not None:
    print(f"Actual Runs Scored in the Next Game ({next_game_date}): {actual_runs}")
else:
    print("No game found for the Braves.")