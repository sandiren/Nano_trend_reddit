import streamlit as st
import requests
from bs4 import BeautifulSoup
import praw
from dotenv import load_dotenv
import os
import pandas as pd
import re

# === Load Reddit credentials from .env ===
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# === Streamlit UI ===
st.set_page_config(page_title="Trend Radar Plus", layout="wide")
st.title("📊 Trend Radar Plus: Niche Discovery with Scoring")

query_input = st.text_input("🔍 Seed Keyword", "vision board")
max_suggestions = st.slider("Google Suggestions to Check", 3, 20, 10)

# === Functions ===
def get_google_autocomplete(seed):
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={seed}"
    try:
        r = requests.get(url)
        return r.json()[1]
    except:
        return []

def get_etsy_listings(keyword):
    try:
        url = f"https://www.etsy.com/search?q={keyword.replace(' ', '+')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        count_el = soup.find('span', class_='wt-display-inline-flex-sm')
        return count_el.text.strip() if count_el else "N/A"
    except:
        return "N/A"

def search_reddit_posts(keyword, limit=10):
    titles = []
    try:
        for post in reddit.subreddit("all").search(keyword, sort="relevance", limit=limit):
            titles.append(post.title)
    except Exception as e:
        st.error(f"Reddit search error: {e}")
    return titles

def count_reddit_mentions(keyword, subreddit="all", limit=100):
    mentions = 0
    try:
        for post in reddit.subreddit(subreddit).search(keyword, limit=limit):
            if keyword.lower() in post.title.lower():
                mentions += 1
    except Exception as e:
        st.error(f"Reddit mention count error: {e}")
    return mentions

def score_niche(etsy_text, reddit_mentions):
    try:
        count = int(re.sub(r'[^\\d]', '', etsy_text.split()[0]))
    except:
        count = 100000
    return (reddit_mentions * 10) + max(0, 1000 - count)

def suggest_product(keyword):
    k = keyword.lower()
    if "template" in k or "planner" in k:
        return "🧾 Create a Notion or Canva template"
    elif "checklist" in k:
        return "✅ Make a printable checklist"
    elif "prompt" in k:
        return "🧠 Bundle AI or ChatGPT prompts"
    else:
        return "🎯 Create a niche digital download or workbook"

# === MAIN APP LOGIC ===
if query_input:
    st.subheader("📌 Autocomplete Suggestions + Niche Scores")
    suggestions = get_google_autocomplete(query_input)
    selected = suggestions[:max_suggestions]

    results = []
    for s in selected:
        etsy = get_etsy_listings(s)
        reddit_hits = count_reddit_mentions(s)
        niche_score = score_niche(etsy, reddit_hits)
        idea = suggest_product(s)
        results.append({
            "keyword": s,
            "etsy_listings": etsy,
            "reddit_mentions": reddit_hits,
            "score": niche_score,
            "suggestion": idea
        })

    df = pd.DataFrame(results)
    st.dataframe(df.sort_values("score", ascending=False))

    st.download_button("📥 Download as CSV", df.to_csv(index=False), "niche_report.csv", "text/csv")

    st.subheader("🗣 Reddit Posts Matching Your Keyword")
    reddit_posts = search_reddit_posts(query_input)
    for t in reddit_posts:
        st.write("•", t)