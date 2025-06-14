# 🔧 Step 0: Import required libraries
import pandas as pd
import re
from textblob import TextBlob
from collections import Counter

# 📂 Step 1: Load dataset
df = pd.read_csv('sentimentdataset.csv')  # Replace with your actual CSV file name

# 👀 View column names (for debugging)
print("Columns in dataset:", df.columns.tolist())

# 🧹 Step 2: Clean text column
def clean_text(text):
    text = re.sub(r"http\S+|@\w+|#\w+", "", str(text))  # Remove URLs, mentions, hashtags
    text = re.sub(r"[^A-Za-z0-9 ]+", "", text)          # Remove punctuation
    return text.lower()

df['Cleaned_Text'] = df['Text'].apply(clean_text)

# 😊 Step 3: Recalculate sentiment using TextBlob
def get_sentiment(text):
    score = TextBlob(text).sentiment.polarity
    if score > 0:
        return 'Positive'
    elif score < 0:
        return 'Negative'
    else:
        return 'Neutral'

df['Calculated_Sentiment'] = df['Cleaned_Text'].apply(get_sentiment)

# 🔎 Step 4: Extract trending hashtags (if the column exists)
if 'Hashtags' in df.columns:
    all_hashtags = sum(df['Hashtags'].dropna().astype(str).str.lower().str.split(), [])
    hashtag_counts = Counter(all_hashtags).most_common(20)
    df_hashtags = pd.DataFrame(hashtag_counts, columns=['Hashtag', 'Frequency'])
else:
    print("⚠️ 'Hashtags' column not found. Skipping hashtag analysis.")
    df_hashtags = pd.DataFrame(columns=['Hashtag', 'Frequency'])

# ⏰ Step 5: Time-based features
if 'Timestamp' in df.columns:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df['Date'] = df['Timestamp'].dt.date
    df['Hour'] = df['Timestamp'].dt.hour
else:
    print("⚠️ 'Timestamp' column not found. Skipping time features.")

# 💾 Step 6: Export for Power BI dashboard
df.to_excel('cleaned_social_data.xlsx', index=False)
df_hashtags.to_excel('top_hashtags.xlsx', index=False)

print("✅ Data exported for dashboarding.")
