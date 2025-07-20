import streamlit as st
import requests
from bs4 import BeautifulSoup
import praw
from dotenv import load_dotenv
import os
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor

# === Load Reddit credentials ===
load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# === Streamlit UI ===
st.set_page_config(page_title="Trend Radar Plus", layout="wide")
st.title("📊 Trend Radar Plus: Discover & Score Niche Product Ideas")

query_input = st.text_input("🔍 Seed Keyword", "vision board")
do_search = st.button("🔍 Search")
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
        search_url = f"https://www.etsy.com/search?q={keyword.replace(' ', '+')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        count_el = soup.find('span', class_='wt-display-inline-flex-sm')
        count_text = count_el.text.strip() if count_el else "N/A"
        return count_text, search_url
    except:
        return "N/A", f"https://www.etsy.com/search?q={keyword.replace(' ', '+')}"

def search_reddit_posts(keyword, limit=10):
    results = []
    try:
        for post in reddit.subreddit("all").search(keyword, sort="relevance", limit=limit):
            results.append({
                "title": post.title,
                "url": f"https://www.reddit.com{post.permalink}"
            })
    except Exception as e:
        st.error(f"Reddit search error: {e}")
    return results

def count_reddit_mentions(keyword, subreddit="all", limit=100):
    mentions = 0
    try:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        for post in reddit.subreddit(subreddit).search(keyword, limit=limit):
            if pattern.search(post.title):
                mentions += 1
    except Exception as e:
        st.error(f"Reddit mention count error: {e}")
    return mentions

def score_niche(etsy_text, reddit_mentions):
    try:
        digits = re.findall(r"[\\d,]+", etsy_text)
        count = int(digits[0].replace(",", "")) if digits else 100000
    except:
        count = 100000
    return (reddit_mentions * 10) + max(0, 1000 - count)

def suggest_product(keyword):
    k = keyword.lower()
    if any(term in k for term in ["template", "planner", "notion", "spreadsheet"]):
        return "🧾 Create a customizable Notion or Google Sheets template"
    elif any(term in k for term in ["checklist", "routine", "habit"]):
        return "✅ Make a stylish printable checklist or habit tracker"
    elif any(term in k for term in ["prompt", "chatgpt", "ai", "journaling"]):
        return "🧠 Sell a ChatGPT prompt pack or digital journaling workbook"
    elif any(term in k for term in ["manifest", "vision", "goal", "intention"]):
        return "🔮 Offer a manifestation board, vision planner, or goal setting workbook"
    elif any(term in k for term in ["budget", "finance", "savings"]):
        return "💰 Build a budget tracker or financial planning spreadsheet"
    elif any(term in k for term in ["sticker", "icon", "clipart", "keychain"]):
        return "🎨 Create printable clipart, SVGs, or custom physical product mockups"
    elif any(term in k for term in ["calendar", "schedule"]):
        return "🗓️ Build a digital or printable calendar planner"
    elif any(term in k for term in ["study", "notes", "school"]):
        return "📚 Make academic study templates or revision planners"
    else:
        return "🎯 Create a high-converting printable, workbook, or toolkit based on niche interest"

# === MAIN APP LOGIC ===
if query_input:
    st.subheader("📌 Niche Suggestions + Etsy + Reddit + Score")
    suggestions = get_google_autocomplete(query_input)
    selected = suggestions[:max_suggestions]

    results = []



    def process_keyword(s):
        etsy, etsy_url = get_etsy_listings(s)
        reddit_hits = count_reddit_mentions(s)
        niche_score = score_niche(etsy, reddit_hits)
        idea = suggest_product(s)
        return {
            "keyword": s,
            "etsy_listings": etsy,
            "etsy_url": etsy_url,
            "reddit_mentions": reddit_hits,
            "score": niche_score,
            "suggestion": idea
        }


    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(process_keyword, selected))

    df = pd.DataFrame(results)
    for _, row in df.sort_values("score", ascending=False).iterrows():
        st.markdown(f"""
**🔑 {row['keyword']}**

🛒 Etsy Listings: [{row['etsy_listings']}]({row['etsy_url']})  
🗣 Reddit Mentions: {row['reddit_mentions']}  
📈 Niche Score: `{row['score']}`  
🎯 Product Suggestion: {row['suggestion']}

---
""", unsafe_allow_html=True)

    st.download_button("📥 Download as CSV", df.to_csv(index=False), "niche_report.csv", "text/csv")

    st.subheader("🗣 Reddit Posts Matching Your Keyword")
    reddit_posts = search_reddit_posts(query_input)
    for post in reddit_posts:
        st.markdown(f"• [{post['title']}]({post['url']})", unsafe_allow_html=True)
