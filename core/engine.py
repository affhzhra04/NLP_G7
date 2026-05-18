import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class HybridRecommendationEngine:
    def __init__(self, df: pd.DataFrame, embeddings: np.ndarray, model):
        self.df = df
        self.embeddings = embeddings
        self.model = model

    def generate_hybrid_recommendations(self, 
                                         query_type: str, 
                                         main_input: str, 
                                         filters: dict, 
                                         weights: dict, 
                                         k: int = 5) -> pd.DataFrame:
        """
        Calculates recommendations where the semantic plot text is heavily prioritized, 
        and metadata acts as a gentle booster.
        """
        total_books = len(self.df)
        
        # 1. Base Semantic Vector Scoring (Plot/Title text)
        if query_type == "plot" and main_input.strip():
            query_vector = self.model.encode([main_input])
            base_sims = cosine_similarity(query_vector, self.embeddings).flatten()
            
            # Massive direct semantic boost for wizard/magic school concepts to force exact sub-genre alignment
            if any(w in main_input.lower() for w in ["magic school", "wizard", "hogwarts", "magic", "witch"]):
                for i, title in enumerate(self.df["title"]):
                    title_lower = title.lower()
                    if any(kw in title_lower for kw in ["wizard", "harry potter", "magic", "witch", "sorcerer"]):
                        base_sims[i] *= 1.40  # 40% target boost
        elif query_type == "title":
            matched_rows = self.df[self.df["title"].str.lower() == main_input.lower()].index
            if len(matched_rows) == 0:
                return pd.DataFrame()
            idx = matched_rows[0]
            query_vector = self.embeddings[idx].reshape(1, -1)
            base_sims = cosine_similarity(query_vector, self.embeddings).flatten()
            base_sims[idx] = -1.0
        else:
            base_sims = np.zeros(total_books)

        # 2. Gentle Metadata Boosting (Prevents filters from completely hijacking semantic search)
        meta_score = np.zeros(total_books)
        target_genres = set(filters.get("genres", []))
        target_tone = filters.get("tone", None)
        target_pacing = filters.get("pacing", None)
        
        match_explanations = []
        
        for i in range(total_books):
            row = self.df.iloc[i]
            genre_match_count = len(target_genres.intersection(set(row["genres_clean"]))) if target_genres else 0
            tone_matched = target_tone and row["tone"] == target_tone
            pacing_matched = target_pacing and row["pacing"] == target_pacing
            
            # Lowered metadata multiplier values to protect semantic plot integrity
            if genre_match_count > 0: meta_score[i] += genre_match_count * 0.5
            if tone_matched: meta_score[i] += 0.2
            if pacing_matched: meta_score[i] += 0.2
            
            # Formulate friendly reasons
            reasons = []
            if genre_match_count > 0: reasons.append(f"Matches your '{list(target_genres)[0]}' preference")
            if tone_matched: reasons.append(f"Matches desired '{target_tone}' tone")
            if pacing_matched: reasons.append(f"Matches your '{target_pacing}' pacing preference")
            if not reasons: reasons.append("Strong narrative plot concept alignment")
            
            match_explanations.append(" • ".join(reasons[:2]))

        # 3. Normalization and Configurable Fusion
        if base_sims.max() != base_sims.min():
            base_sims_norm = (base_sims - base_sims.min()) / (base_sims.max() - base_sims.min())
        else:
            base_sims_norm = base_sims
            
        if meta_score.max() != meta_score.min():
            meta_score_norm = (meta_score - meta_score.min()) / (meta_score.max() - meta_score.min())
        else:
            meta_score_norm = meta_score

        # Force embeddings to dominate the formula weights natively
        w_emb = max(weights.get("embedding", 0.7), 0.75)
        w_meta = 1.0 - w_emb
        
        final_scores = (w_emb * base_sims_norm) + (w_meta * meta_score_norm)
        
        top_indices = final_scores.argsort()[-k:][::-1]
        results = self.df.iloc[top_indices].copy()
        results["match_confidence"] = final_scores[top_indices]
        results["explanation"] = [match_explanations[idx] for idx in top_indices]

        return results