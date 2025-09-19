# Story Point Estimator

AI-powered user story estimation using DeepSeek API and neural networks.

## Quick Start

```bash
pip install -r requirements.txt
```

## Usage

### 1. Interactive Story Generation
```python
python main.py
# Enter number of stories when prompted
```

### 2. Process 100 Stories
```python
python process_100_stories.py
```

### 3. Custom CSV
```python
from story_estimator import StoryEstimator

estimator = StoryEstimator()  # Uses DEEPSEEK_API_KEY env var
result = estimator.process_stories("input.csv", "output.csv")
```

## CSV Format

```csv
id,story,complexity,priority
1,"As a user I want to login...",Low,High
```

## Output

- **story_points**: Fibonacci (1,2,3,5,8,13,21)
- **hours**: Estimated development time
- **days**: Hours ÷ 8
- **sprints**: Days ÷ 10 (2-week sprints)
- **team_weeks**: Days ÷ 5

## Files

- `main.py` - Interactive story generation
- `story_estimator.py` - Main engine
- `story_generator.py` - Story generator
- `sample_user_stories.csv` - 10 sample stories
- `user_stories_100.csv` - 100 generated stories

## API Key

Edit `.env` file:
```
DEEPSEEK_API_KEY=your-actual-api-key
```