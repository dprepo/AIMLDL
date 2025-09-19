from story_generator import StoryGenerator
from story_estimator import StoryEstimator
from load_env import load_env

load_env()

def main():
    # Step 1: Get user input for number of stories
    try:
        n = int(input("Enter number of user stories to generate: "))
    except ValueError:
        print("Invalid input. Using default: 50")
        n = 50
    
    # Step 2: Generate N user stories
    generator = StoryGenerator()
    stories_file = f"generated_stories_{n}.csv"
    generator.generate_stories(n, stories_file)
    
    # Step 3: Estimate story points and calculate effort
    estimator = StoryEstimator()
    output_file = f"estimated_stories_{n}.csv"
    result = estimator.process_stories(stories_file, output_file)
    
    # Step 4: Display results
    print(f"\nProcessing Complete!")
    print(f"Generated: {stories_file}")
    print(f"Estimated: {output_file}")
    
    print(f"\nSummary for {n} stories:")
    print(f"Total Hours: {result['hours'].sum():.1f}")
    print(f"Total Days: {result['days'].sum():.1f}")
    print(f"Total Sprints: {result['sprints'].sum():.1f}")
    print(f"Total Team Weeks: {result['team_weeks'].sum():.1f}")
    
    print(f"\nStory Points Distribution:")
    print(result['story_points'].value_counts().sort_index())

if __name__ == "__main__":
    main()