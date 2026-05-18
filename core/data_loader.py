import pandas as pd
import numpy as np
import ast
import streamlit as st

@st.cache_data
def load_clean_dataframe(file_path: str) -> pd.DataFrame:
    """
    Ingests and normalizes the CMU/Goodreads dataset.
    Ensures safe unpacking of list-based metadata features.
    """
    df = pd.read_csv(file_path)
    
    # Safely unpack list columns from flat string representation
    list_cols = ["genres_clean", "themes", "tropes", "settings", "character_archetypes"]
    for col in list_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else (x if isinstance(x, list) else []))
        else:
            df[col] = [[] for _ in range(len(df))]
            
    # Synthetic generation/fallback for missing advanced metadata fields
    if "rating" not in df.columns: 
        df["rating"] = np.random.uniform(3.8, 4.9, size=len(df)).round(1)
    if "pacing" not in df.columns: 
        df["pacing"] = np.random.choice(["Fast-paced", "Moderate", "Slow-burn"], size=len(df))
    if "tone" not in df.columns: 
        df["tone"] = np.random.choice(["Dark", "Whimsical", "Tense", "Lighthearted", "Melancholic"], size=len(df))
        
    return df

@st.cache_resource
def load_vector_space(file_path: str) -> np.ndarray:
    """Loads the pre-computed high-dimensional S-BERT embedding matrix."""
    return np.load(file_path)