from story_estimator import StoryEstimator

# Process 100 stories
estimator = StoryEstimator()
result = estimator.process_stories("estimated_stories_100.csv")

print(f"Processed {len(result)} user stories")
print("\nStory Points Distribution:")
print(result['story_points'].value_counts().sort_index())

print(f"\nTotal Project Effort:")
print(f"Total Hours: {result['hours'].sum():.2f}")
print(f"Total Days: {result['days'].sum():.2f}")
print(f"Total Sprints: {result['sprints'].sum():.2f}")
print(f"Total Team Weeks: {result['team_weeks'].sum():.2f}")

print(f"\nAverage per Story:")
print(f"Avg Hours: {result['hours'].mean():.2f}")
print(f"Avg Days: {result['days'].mean():.2f}")
print(f"Avg Story Points: {result['story_points'].mean():.2f}")