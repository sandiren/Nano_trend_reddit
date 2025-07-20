# 📊 Trend Radar Plus

**Find profitable micro-niches using Reddit + Google Autocomplete + Etsy — no Google Trends required.**

This is a Streamlit-based app designed to help digital product creators, marketers, and solopreneurs identify under-served keyword opportunities and fast-launch ideas like templates, printables, and prompt packs.

---

## 🚀 What It Does

- 🔍 Expands a seed keyword using **Google Autocomplete**
- 🛒 Fetches **Etsy listing counts** to gauge competition
- 🗣️ Searches **Reddit** for discussion volume and relevance
- 🧠 Suggests a product idea per keyword
- 📈 Ranks results with a **niche score**: high Reddit buzz + low Etsy competition
- 📥 Exports results to CSV

---

## 📦 Requirements

```
streamlit
requests
beautifulsoup4
praw
python-dotenv
pandas
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## 🔐 Reddit API Setup

To access Reddit data, you need API credentials:

1. Go to: https://www.reddit.com/prefs/apps
2. Click **Create Another App**
3. Set:
   - **Name**: trendradar_app
   - **Type**: Script
   - **Redirect URI**: `http://localhost:8080`
4. After saving, copy your credentials into a `.env` file:

```env
REDDIT_CLIENT_ID=your_id_here
REDDIT_CLIENT_SECRET=your_secret_here
REDDIT_USER_AGENT=trendradar_app
```

Make sure `.env` is listed in `.gitignore` if pushing to GitHub.

---

## ▶️ How to Run Locally

```bash
streamlit run trend_radar_plus.py
```

---

## 💻 Deploy to Streamlit Cloud

1. Push this repo to GitHub (public repo recommended)
2. Go to https://streamlit.io/cloud
3. Click **“Deploy an app”**
4. Select your repo + `trend_radar_plus.py`
5. Add 3 **Secrets** in Streamlit Cloud Settings:
   - `REDDIT_CLIENT_ID`
   - `REDDIT_CLIENT_SECRET`
   - `REDDIT_USER_AGENT`

Your app will be live at: `https://<your-username>.streamlit.app`

---

## 🧠 Example: Vision Board Niches

| Keyword                 | Etsy Listings | Reddit Mentions | Niche Score | Product Idea                          |
|-------------------------|---------------|------------------|-------------|---------------------------------------|
| vision board prompts    | 254           | 11               | 1156        | 🧠 Bundle AI or ChatGPT prompts       |
| digital vision planner  | 1,021         | 5                | 979         | ✅ Make a printable PDF planner       |
| vision board template   | 3,212         | 9                | 890         | 🧾 Create a Notion or Canva template  |

---

## 📌 Future Enhancements

- ✅ GPT-generated product title + description
- ✅ Etsy product tag extraction
- ✅ Trend tracking over time
- ✅ Daily trend alert + email
