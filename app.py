import streamlit as st
from core.data_loader import load_clean_dataframe, load_vector_space
from core.query_parser import QueryParser
from core.engine import HybridRecommendationEngine
from ui.styles import inject_premium_css
from ui.components import render_hero_header, render_how_it_works, render_recommendation_card

# Apply global custom CSS stylesheet overrides
inject_premium_css()

# Render Landing Layout Elements
render_hero_header()

# FIX (Blue Box Removal): Removed st.write(" ") from directly underneath the header blocks
render_how_it_works()

# Ingest and cache pipeline assets
try:
    df = load_clean_dataframe("data/cmu_books_cleaned.csv")
    embeddings = load_vector_space("embeddings/sbert_embeddings.npy")
    
    from sentence_transformers import SentenceTransformer
    @st.cache_resource
    def init_transformer():
        return SentenceTransformer('all-MiniLM-L6-v2')
        
    model = init_transformer()
    engine = HybridRecommendationEngine(df, embeddings, model)
    parser = QueryParser(
        tone_options=["Dark", "Whimsical", "Tense", "Lighthearted", "Melancholic"],
        pacing_options=["Fast-paced", "Moderate", "Slow-burn"]
    )
except Exception as e:
    st.error(f"Initialization Error: Ensure database files exist inside data/ and embeddings/ directories. Log: {e}")
    st.stop()

# Responsive Workspace Layout Generation
col_dashboard, col_sidebar = st.columns([2.2, 0.8], gap="large")

with col_dashboard:
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.write("### 🛠️ Search Options")
    
    search_mode = st.radio("Choose search method:", ["Search by Story Idea / Plot Summary", "Search by Book Title"], horizontal=True)
    
    main_input = ""
    if search_mode == "Search by Story Idea / Plot Summary":
        main_input = st.text_area("Describe what kind of story you are looking for:", placeholder="e.g., A fantasy story about an orphaned boy who discovers his lineage at a school for magic...", height=100)
    else:
        main_input = st.selectbox("Select a book title you like:", options=df["title"].tolist())
        
    # (Point 4): Friendly simplified options terminology for normal readers
    with st.expander("🎨 Personalize your search criteria"):
        all_genres = sorted(list(set([g for sublist in df["genres_clean"] for g in sublist])))
        selected_genres = st.multiselect("Match specific genres:", options=all_genres)
        
        c1, c2, c3 = st.columns(3)
        sel_tone = c1.selectbox("Story Tone:", options=[None, "Dark", "Whimsical", "Tense", "Lighthearted", "Melancholic"])
        sel_pacing = c2.selectbox("Story Pacing:", options=[None, "Fast-paced", "Moderate", "Slow-burn"])
        max_suggestions = c3.slider("How many books to show:", min_value=3, max_value=10, value=5)
        
        st.write("---")
        emb_w = st.slider("Focus more on the written plot description:", 0.5, 1.0, 0.8, step=0.05)
        meta_w = 1.0 - emb_w

    st.markdown('</div>', unsafe_allow_html=True)
    execute_search = st.button("Find Books ✨")

with col_sidebar:
    st.write("### 🔥 Suggestion from PlotPick")
    popular_mock = [
        {"title": "The Lies of Locke Lamora", "author": "Scott Lynch", "rating": "⭐ 4.5"},
        {"title": "Project Hail Mary", "author": "Andy Weir", "rating": "⭐ 4.6"},
        {"title": "The Night Circus", "author": "Erin Morgenstern", "rating": "⭐ 4.3"}
    ]
    for b in popular_mock:
        st.markdown(f"""
            <div style="background: #0f1524; border: 1px solid #1e293b; padding: 14px; border-radius: 10px; margin-bottom: 12px;">
                <span style="float: right; color: #fbbf24; font-size: 0.82rem; font-weight: bold;">{b['rating']}</span>
                <strong style="color: #f1f5f9; display: block; font-size: 0.9rem;">{b['title']}</strong>
                <span style="color: #64748b; font-size: 0.8rem;">By {b['author']}</span>
            </div>
        """, unsafe_allow_html=True)

# Pipeline Computation Execution Trigger
if execute_search:
    st.write("---")
    
    parsed_filters = {
        "genres": selected_genres,
        "tone": sel_tone,
        "pacing": sel_pacing
    }
    
    if search_mode == "Search by Story Idea / Plot Summary" and main_input.strip():
        extracted_meta = parser.parse_prompt(main_input)
        if not parsed_filters["tone"] and extracted_meta["tones"]:
            parsed_filters["tone"] = extracted_meta["tones"][0]
        if not parsed_filters["pacing"] and extracted_meta["pacing"]:
            parsed_filters["pacing"] = extracted_meta["pacing"][0]
            
    with st.spinner("Searching database..."):
        # Diversity score metric display logic has been cleanly stripped away here
        results = engine.generate_hybrid_recommendations(
            query_type="plot" if search_mode == "Search by Story Idea / Plot Summary" else "title",
            main_input=main_input,
            filters=parsed_filters,
            weights={"embedding": emb_w, "metadata": meta_w},
            k=max_suggestions
        )
        
    if results.empty:
        st.warning("No records matched the defined criteria matrices.")
    else:
        st.write("### ✨ Recommended for you")
        
        # Loop over recommendations and utilize Streamlit expanders to handle the "Read More" functionality smoothly
        for idx, (_, row) in enumerate(results.iterrows(), start=1):
            render_recommendation_card(idx, row)