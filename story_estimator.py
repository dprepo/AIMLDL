import pandas as pd
import numpy as np
import requests
import json
import os
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import pickle
from load_env import load_env

load_env()

class StoryEstimator:
    def __init__(self, deepseek_api_key=None):
        self.api_key = deepseek_api_key or os.getenv('DEEPSEEK_API_KEY', 'demo-key')
        self.fibonacci = [1, 2, 3, 5, 8, 13, 21]
        self.scaler = StandardScaler()
        self.ann_model = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42)
        
    def load_stories(self, csv_path):
        """Load user stories from CSV"""
        return pd.read_csv(csv_path)
    
    def estimate_story_points(self, story_text, complexity, priority):
        """Estimate story points using DeepSeek API"""
        prompt = f"""
        Estimate story points for this user story using Fibonacci sequence (1,2,3,5,8,13,21):
        Story: {story_text}
        Complexity: {complexity}
        Priority: {priority}
        
        Consider:
        - 1-2: Simple tasks
        - 3-5: Medium complexity
        - 8-13: Complex tasks
        - 21: Very complex/uncertain
        
        Return only the number.
        """
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 10
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                estimated_points = int(result['choices'][0]['message']['content'].strip())
                return estimated_points if estimated_points in self.fibonacci else 5
            else:
                return 5  # Default fallback
        except:
            return 5  # Default fallback
    
    def train_effort_model(self, training_data):
        """Train ANN model for effort estimation"""
        X = training_data[['story_points', 'complexity_score', 'priority_score']].values
        y = training_data['hours'].values
        
        X_scaled = self.scaler.fit_transform(X)
        self.ann_model.fit(X_scaled, y)
    
    def calculate_effort(self, story_points, complexity, priority):
        """Calculate effort using trained ANN model"""
        complexity_map = {'Low': 1, 'Medium': 2, 'High': 3}
        priority_map = {'Low': 1, 'Medium': 2, 'High': 3}
        
        features = np.array([[
            story_points,
            complexity_map.get(complexity, 2),
            priority_map.get(priority, 2)
        ]])
        
        features_scaled = self.scaler.transform(features)
        hours = self.ann_model.predict(features_scaled)[0]
        
        days = hours / 8
        sprints = days / 10  # 2-week sprints
        team_weeks = days / 5  # 5-day work week
        
        return {
            'hours': round(hours, 2),
            'days': round(days, 2),
            'sprints': round(sprints, 2),
            'team_weeks': round(team_weeks, 2)
        }
    
    def process_stories(self, input_csv, output_csv):
        """Main processing function"""
        # Load stories
        df = self.load_stories(input_csv)
        
        # Create training data for ANN (synthetic for demo)
        training_data = pd.DataFrame({
            'story_points': [1, 2, 3, 5, 8, 13, 21] * 10,
            'complexity_score': np.random.randint(1, 4, 70),
            'priority_score': np.random.randint(1, 4, 70),
            'hours': [2, 4, 8, 16, 32, 52, 84] * 10 + np.random.normal(0, 5, 70)
        })
        
        # Train effort model
        self.train_effort_model(training_data)
        
        # Process each story
        results = []
        for _, row in df.iterrows():
            # Estimate story points
            story_points = self.estimate_story_points(
                row.get('story', ''), 
                row.get('complexity', 'Medium'), 
                row.get('priority', 'Medium')
            )
            
            # Calculate effort
            effort = self.calculate_effort(
                story_points, 
                row.get('complexity', 'Medium'), 
                row.get('priority', 'Medium')
            )
            
            results.append({
                **row.to_dict(),
                'story_points': story_points,
                **effort
            })
        
        # Save results
        result_df = pd.DataFrame(results)
        result_df.to_csv(output_csv, index=False)
        return result_df

# Usage
if __name__ == "__main__":
    estimator = StoryEstimator("APIKEY")
    result = estimator.process_stories("user_stories.csv", "estimated_stories.csv")
    print(f"Processed {len(result)} stories")