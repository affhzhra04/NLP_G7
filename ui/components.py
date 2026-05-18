import streamlit as st
import pandas as pd
import requests

def render_hero_header():
    st.markdown("""
        <div class="brand-container">
            <div class="nav-logo">🔮 <span>PlotPick</span></div>
        </div>
        <h2 style='font-size: 2.4rem; font-weight: 800; color: #ffffff; margin-top: 15px; margin-bottom: 5px;'>
            Describe the plot. Discover your next read.
        </h2>
        <p style='color: #64748b; font-size: 1.05rem; margin-bottom: 25px;'>
            An advanced content engine using deep-semantic transformer vectors alongside metadata constraints.
        </p>
    """, unsafe_allow_html=True)

def render_how_it_works():
    col1, col2, col3 = st.columns(3)
    steps = [
        ("📝 1. Your Input", "Type a short plot summary or select a book you already love."),
        ("⚡ 2. Smart Processing", "PlotPick quickly analyzes themes, descriptions, and story styles together."),
        ("🔮 3. Discover Books", "Get a tailored list of recommendations sorted by what matches best.")
    ]
    for col, (title, desc) in zip([col1, col2, col3], steps):
        col.markdown(f"""
            <div style="background: #0f1524; border: 1px solid #1e293b; padding: 20px; border-radius: 12px; min-height: 120px;">
                <h4 style="margin: 0 0 6px 0; color: #f1f5f9; font-size:1.05rem;">{title}</h4>
                <p style="margin: 0; font-size: 0.85rem; color: #64748b; line-height: 1.45;">{desc}</p>
            </div>
        """, unsafe_allow_html=True)

def get_dynamic_cover_url(title: str, author: str) -> str:
    """Queries OpenLibrary API combining Title and Author for highly accurate book cover matching."""
    clean_title = str(title).replace(" ", "+")
    clean_author = str(author).replace(" ", "+") if pd.notna(author) else ""
    api_url = f"https://openlibrary.org/search.json?title={clean_title}&author={clean_author}"
    fallback = "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=150"
    try:
        response = requests.get(api_url, timeout=0.8).json()
        if response.get("docs") and "cover_i" in response["docs"][0]:
            cover_id = response["docs"][0]["cover_i"]
            if cover_id and cover_id != -1:
                return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    except:
        pass
    return fallback

def render_recommendation_card(count: int, row: dict):
    # Fix 1: Pass both Title and Author to drastically reduce empty fallback images
    cover_url = get_dynamic_cover_url(row["title"], row["author"])
    genre_pills = "".join([f"<span class='pill-metadata'>{g}</span>" for g in row["genres_clean"][:3]])
    
    raw_summary = str(row.get("summary", "No plot description available inside loaded dataset partition."))
    
    # Fix 2: Non-spoiler narrative synopsis generation logic (keeps the first 3 introductory sentences)
    sentences = raw_summary.split(". ")
    if len(sentences) > 3:
        synopsis_snippet = ". ".join(sentences[:3]) + "."
        full_synopsis_view = ". ".join(sentences[:5]) + "... [End of Preview Blurb]"
    else:
        synopsis_snippet = raw_summary
        full_synopsis_view = raw_summary

    card_html = f"""
        <div class="premium-card">
            <div class="cover-frame">
                <img src="{cover_url}" alt="Book Cover">
            </div>
            <div style="flex-grow: 1;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 4px;">
                    <div>
                        <h4 style="margin: 0 0 2px 0; font-size: 1.25rem; color: #f8fafc;">{count}. {row['title']}</h4>
                        <p style="margin: 0 0 8px 0; color: #64748b; font-size: 0.88rem;">By {row['author']}</p>
                    </div>
                    <span class="score-indicator">{row['match_confidence']:.1%} Match</span>
                </div>
                <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.5; margin: 0 0 14px 0; font-style: italic;">
                    "{synopsis_snippet}"
                </p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>{genre_pills}</div>
                    <span style="font-size: 0.78rem; color: #475569;">Tone: <b>{row['tone']}</b> | Pacing: <b>{row['pacing']}</b></span>
                </div>
            </div>
        </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Clean synopsis dropdown positioned entirely outside the HTML template block
    with st.expander(f"📖 Read introductory synopsis blurb for {row['title']}"):
        st.write(full_synopsis_view)
    st.write(" ")