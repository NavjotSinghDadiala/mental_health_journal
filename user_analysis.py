import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import seaborn as sns
from collections import Counter
import os
from sqlalchemy import func
from models import db, User, Post

def generate_user_analysis():
    # Get all users and their posts
    users = User.query.all()
    posts = Post.query.all()
    
    # Convert to DataFrame for easier analysis
    posts_data = []
    for post in posts:
        posts_data.append({
            'user_id': post.user_id,
            'username': post.user.username,
            'content': post.content,
            'emotion': post.emotion,
            'confidence': post.confidence,
            'timestamp': post.timestamp
        })
    
    df = pd.DataFrame(posts_data)
    
    # Create analysis directory if it doesn't exist
    if not os.path.exists('static/analysis'):
        os.makedirs('static/analysis')
    
    # Generate plots
    plots = {}
    
    # 1. Emotion Distribution
    plt.figure(figsize=(10, 6))
    emotion_counts = df['emotion'].value_counts()
    sns.barplot(x=emotion_counts.index, y=emotion_counts.values)
    plt.title('Emotion Distribution Across All Posts')
    plt.xlabel('Emotion')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/analysis/emotion_distribution.png')
    plt.close()
    plots['emotion_distribution'] = 'emotion_distribution.png'
    
    # 2. Posts Over Time
    plt.figure(figsize=(12, 6))
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_posts = df.groupby('date').size()
    daily_posts.plot(kind='line', marker='o')
    plt.title('Posts Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Posts')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('static/analysis/posts_over_time.png')
    plt.close()
    plots['posts_over_time'] = 'posts_over_time.png'
    
    # 3. User Activity
    plt.figure(figsize=(10, 6))
    user_activity = df['username'].value_counts().head(10)
    sns.barplot(x=user_activity.values, y=user_activity.index)
    plt.title('Top 10 Most Active Users')
    plt.xlabel('Number of Posts')
    plt.ylabel('Username')
    plt.tight_layout()
    plt.savefig('static/analysis/user_activity.png')
    plt.close()
    plots['user_activity'] = 'user_activity.png'
    
    # 4. Emotion by User
    plt.figure(figsize=(12, 8))
    user_emotions = df.groupby(['username', 'emotion']).size().unstack(fill_value=0)
    user_emotions.plot(kind='bar', stacked=True, figsize=(12, 8))
    plt.title('Emotion Distribution by User')
    plt.xlabel('Username')
    plt.ylabel('Number of Posts')
    plt.xticks(rotation=45)
    plt.legend(title='Emotion')
    plt.tight_layout()
    plt.savefig('static/analysis/emotion_by_user.png')
    plt.close()
    plots['emotion_by_user'] = 'emotion_by_user.png'
    
    # 5. Confidence Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['confidence'], bins=20)
    plt.title('Confidence Score Distribution')
    plt.xlabel('Confidence Score')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('static/analysis/confidence_distribution.png')
    plt.close()
    plots['confidence_distribution'] = 'confidence_distribution.png'
    
    # Calculate statistics
    stats = {
        'total_users': len(users),
        'total_posts': len(posts),
        'avg_posts_per_user': len(posts) / len(users) if users else 0,
        'most_common_emotion': df['emotion'].mode().iloc[0] if not df.empty else 'N/A',
        'avg_confidence': df['confidence'].mean() if not df.empty else 0,
        'active_users_last_week': len(df[df['timestamp'] > datetime.now() - timedelta(days=7)]['username'].unique()),
        'posts_last_week': len(df[df['timestamp'] > datetime.now() - timedelta(days=7)])
    }
    
    return plots, stats 