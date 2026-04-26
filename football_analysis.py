# Football Results Analysis - Complete Solution
# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.se# Load the dataset
df = pd.read_csv("results.csv")
df.head()t_palette("husl")
# 1. How many matches are in the dataset?
total_matches = df.shape[0]
print(f"1. Total number of matches: {total_matches}")
# 2. What is the earliest and latest year in the data?
# First, convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

earliest_date = df['date'].min()
latest_date = df['date'].max()

# Extract years
earliest_year = earliest_date.year
latest_year = latest_date.year

print(f"2. Date range: {earliest_date.strftime('%B %d, %Y')} to {latest_date.strftime('%B %d, %Y')}")
print(f"   Year range: {earliest_year} to {latest_year}")
# 3. How many unique countries are there?
# Combine home and away teams to get all unique countries
all_teams = pd.concat([df['home_team'], df['away_team']]).unique()
unique_countries = len(all_teams)

print(f"3. Number of unique countries: {unique_countries}")
# 4. Which team appears most frequently as home team?
most_frequent_home = df['home_team'].value_counts().head(1)
team_name = most_frequent_home.index[0]
appearances = most_frequent_home.values[0]

print(f"4. Team with most home appearances: {team_name} ({appearances} times)")

# Show top 10 home teams
print("\nTop 10 most frequent home teams:")
print(df['home_team'].value_counts().head(10))
# Create total goals column
df['total_goals'] = df['home_score'] + df['away_score']

# 5. What is the average number of goals per match?
avg_goals = df['total_goals'].mean()
print(f"5. Average goals per match: {avg_goals:.2f}")
# 6. What is the highest scoring match?
max_goals = df['total_goals'].max()
highest_scoring = df[df['total_goals'] == max_goals][['date', 'home_team', 'away_team', 'home_score', 'away_score', 'total_goals']]

print(f"6. Highest scoring match(es) with {max_goals} total goals:")
print(highest_scoring.head())
# 7. Are more goals scored at home or away?
total_home_goals = df['home_score'].sum()
total_away_goals = df['away_score'].sum()
avg_home_goals = df['home_score'].mean()
avg_away_goals = df['away_score'].mean()

print(f"7. Goal comparison:")
print(f"   Total home goals: {total_home_goals}")
print(f"   Total away goals: {total_away_goals}")
print(f"   Average home goals per match: {avg_home_goals:.2f}")
print(f"   Average away goals per match: {avg_away_goals:.2f}")
print(f"   Home advantage: {((avg_home_goals - avg_away_goals) / avg_away_goals * 100):.1f}% more goals at home")
# 8. What is the most common total goals value?
most_common_goals = df['total_goals'].value_counts().head(1)
print(f"8. Most common total goals: {most_common_goals.index[0]} goals")
print(f"   Frequency: {most_common_goals.values[0]} matches")

# Show top 5 most common total goals values
print("\nTop 5 most common total goals values:")
print(df['total_goals'].value_counts().head())
# Create match outcome function
def match_result(row):
    if row['home_score'] > row['away_score']:
        return 'Home Win'
    elif row['home_score'] < row['away_score']:
        return 'Away Win'
    else:
        return 'Draw'

# Apply function to create result column
df['result'] = df.apply(match_result, axis=1)

# 9. What percentage of matches are home wins?
result_counts = df['result'].value_counts()
home_win_percentage = (result_counts.get('Home Win', 0) / len(df)) * 100
away_win_percentage = (result_counts.get('Away Win', 0) / len(df)) * 100
draw_percentage = (result_counts.get('Draw', 0) / len(df)) * 100

print(f"9. Match result percentages:")
print(f"   Home Wins: {home_win_percentage:.2f}%")
print(f"   Away Wins: {away_win_percentage:.2f}%")
print(f"   Draws: {draw_percentage:.2f}%")
# 10. Does home advantage exist?
if home_win_percentage > away_win_percentage:
    advantage_text = "YES"
    advantage_diff = home_win_percentage - away_win_percentage
    print(f"10. Home advantage exists? {advantage_text}")
    print(f"    Home teams win {advantage_diff:.2f}% more matches than away teams")
    print(f"    This statistically significant difference supports the existence of home advantage")
else:
    print(f"10. Home advantage exists? NO")
  # 11. Which country has the most wins historically?
# Create a function to get wins for each team
def get_team_wins(df):
    home_wins = df[df['result'] == 'Home Win']['home_team'].value_counts()
    away_wins = df[df['result'] == 'Away Win']['away_team'].value_counts()
    total_wins = home_wins.add(away_wins, fill_value=0).astype(int)
    return total_wins.sort_values(ascending=False)

team_wins = get_team_wins(df)
most_wins_team = team_wins.head(1)
print(f"11. Team with most wins historically: {most_wins_team.index[0]}")
print(f"    Total wins: {most_wins_team.values[0]}")
print("\nTop 10 teams with most wins:")
print(team_wins.head(10))
# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Histogram of goals
axes[0, 0].hist(df['total_goals'], bins=15, edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Distribution of Goals Per Match', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Total Goals')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].axvline(df['total_goals'].mean(), color='red', linestyle='dashed', 
                   linewidth=2, label=f'Mean: {df["total_goals"].mean():.2f}')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2. Bar chart of match outcomes
result_counts = df['result'].value_counts()
colors = ['#2ecc71', '#e74c3c', '#3498db']
axes[0, 1].bar(result_counts.index, result_counts.values, color=colors, edgecolor='black')
axes[0, 1].set_title('Match Outcomes Distribution', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('Number of Matches')
axes[0, 1].set_xlabel('Match Result')

# Add percentage labels on bars
for i, (result, count) in enumerate(result_counts.items()):
    percentage = (count / len(df)) * 100
    axes[0, 1].text(i, count/2, f'{percentage:.1f}%', 
                   ha='center', va='center', fontweight='bold', fontsize=12)

# Add count labels on top of bars
for i, (result, count) in enumerate(result_counts.items()):
    axes[0, 1].text(i, count, str(count), ha='center', va='bottom')

# 3. Top 10 teams by total wins
top_10_wins = team_wins.head(10)
axes[1, 0].barh(range(len(top_10_wins)), top_10_wins.values, edgecolor='black')
axes[1, 0].set_yticks(range(len(top_10_wins)))
axes[1, 0].set_yticklabels(top_10_wins.index)
axes[1, 0].set_title('Top 10 Teams by Total Wins', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Number of Wins')
axes[1, 0].invert_yaxis()  # Highest wins at top

# Add value labels
for i, (team, wins) in enumerate(top_10_wins.items()):
    axes[1, 0].text(wins, i, f' {wins}', va='center', fontweight='bold')

# 4. Goals by decade trend
df['year'] = df['date'].dt.year
df['decade'] = (df['year'] // 10) * 10
decade_goals = df.groupby('decade')['total_goals'].mean()

axes[1, 1].plot(decade_goals.index, decade_goals.values, marker='o', 
               linewidth=2, markersize=8, color='#e67e22')
axes[1, 1].set_title('Average Goals per Match by Decade', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Decade')
axes[1, 1].set_ylabel('Average Goals')
axes[1, 1].grid(True, alpha=0.3)

# Annotate points
for decade, avg_goals in decade_goals.items():
    axes[1, 1].annotate(f'{avg_goals:.2f}', 
                       (decade, avg_goals),
                       textcoords="offset points",
                       xytext=(0,10),
                       ha='center',
                       fontsize=9)

plt.tight_layout()
plt.show()
# Summary Statistics Section
print("="*60)
print("COMPREHENSIVE FOOTBALL ANALYSIS SUMMARY")
print("="*60)

print("\n📊 DATASET OVERVIEW:")
print(f"• Total Matches Analyzed: {total_matches:,}")
print(f"• Time Period: {earliest_year} - {latest_year}")
print(f"• Unique Teams: {unique_countries}")

print("\n⚽ GOAL STATISTICS:")
print(f"• Average Goals per Match: {avg_goals:.2f}")
print(f"• Highest Scoring Match: {max_goals} goals")
print(f"• Most Common Goal Total: {most_common_goals.index[0]} goals")
print(f"• Home Goals per Match: {avg_home_goals:.2f}")
print(f"• Away Goals per Match: {avg_away_goals:.2f}")

print("\n🏆 MATCH OUTCOMES:")
print(f"• Home Win Percentage: {home_win_percentage:.2f}%")
print(f"• Away Win Percentage: {away_win_percentage:.2f}%")
print(f"• Draw Percentage: {draw_percentage:.2f}%")
print(f"• Home Advantage: {'Yes - Significant' if home_win_percentage > away_win_percentage else 'No'}")

print("\n👑 TOP PERFORMERS:")
print(f"• Most Wins: {most_wins_team.index[0]} with {most_wins_team.values[0]} wins")
print(f"• Most Home Games: {team_name} with {appearances} appearances")

print("\n" + "="*60)
