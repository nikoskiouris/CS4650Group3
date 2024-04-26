from scraper import load_articles
from sentiment_analysis import load_data, calculate_performance_score, compute_performance_scores

# Load the team data
team_data_2010 = load_data('Data/Atlanta Braves Batting Data 2010.xlsx', 'excel')
team_data_2020 = load_data('Data/Atlanta Braves Batting Data 2020.xlsx', 'excel')

# Calculate initial and final performance scores
initial_score_2010 = calculate_performance_score(team_data_2010, 'r')
final_score_2020 = calculate_performance_score(team_data_2020, 'r')

# Load articles from URLs
article_urls = [
    'https://www.masslive.com/sports/2010/10/errors_cost_atlanta_braves_gam.html',
    # Add more URLs as needed
]
article_data = load_articles(article_urls)

# Adjust performance score based on sentiment analysis of articles
adjusted_df = compute_performance_scores(article_data, 'Article', initial_score_2010)

# Print the results
print("Initial Score 2010:", initial_score_2010)
print("Final Score 2020:", final_score_2020)
print("Adjusted Performance Scores:")
print(adjusted_df[['Title', 'ArticleSentiment', 'AdjustedPerformanceScore']])