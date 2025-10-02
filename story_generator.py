import pandas as pd
import random

class StoryGenerator:
    def __init__(self):
        self.templates = [
            "As a user I want to {} so that I can {}",
            "As an admin I want to {} so that I can {}",
            "As a customer I want to {} so that I can {}"
        ]
        
        self.actions = [
            "login", "logout", "reset password", "view profile", "edit profile",
            "upload files", "download files", "search content", "filter results",
            "create reports", "export data", "manage users", "set permissions",
            "receive notifications", "customize dashboard", "backup data",
            "integrate API", "configure settings", "monitor performance",
            "send messages", "schedule meetings", "create projects", "assign tasks"
        ]
        
        self.purposes = [
            "access my account", "secure my session", "regain access", "see my info",
            "update my data", "share documents", "save files", "find information",
            "narrow results", "analyze usage", "share insights", "control access",
            "stay informed", "personalize experience", "protect data",
            "automate workflows", "optimize performance", "track metrics",
            "communicate", "coordinate work", "organize tasks", "delegate work"
        ]
        
        self.complexities = ["Low", "Medium", "High"]
        self.priorities = ["Low", "Medium", "High"]
    
    def generate_stories(self, n, output_file):
        stories = []
        for i in range(1, n + 1):
            template = random.choice(self.templates)
            action = random.choice(self.actions)
            purpose = random.choice(self.purposes)
            
            story = template.format(action, purpose)
            
            stories.append({
                "id": i,
                "story": story,
                "complexity": random.choice(self.complexities),
                "priority": random.choice(self.priorities)
            })
        
        df = pd.DataFrame(stories)
        df.to_csv(output_file, index=False)
        print(f"Generated {n} stories in {output_file}")
        return df