# 🔮 PlotPick - Book Recommender System

## 🚀 Setup Instructions
1. Clone this repository to your local machine.
2. Download the required dataset and embedding matrix assets from our shared storage link:
   👉 **https://drive.google.com/drive/folders/1GISfA9h0ODeWYvAFtPi5R3oMFclrHXKv?usp=sharing**
3. Create a `data/` folder in the root directory and drop `cmu_books_cleaned.csv` inside it.
4. Create an `embeddings/` folder in the root directory and drop `sbert_embeddings.npy` inside it.
5. Install required dependencies:
```bash
pip install -r requirements.txt
```
6. **Configure Explainable AI (Optional but Recommended):**
   - We use the Google Gemini API to dynamically generate conversational explanations for book recommendations. 
   - Create a `.env` file in the root directory.
   - Open `.env` and add your free Google AI Studio key: `GEMINI_API_KEY=your_key_here`
   - *(If no key is provided, the app will safely fall back to default rule-based explanations).*
7.  Run `streamlit run app.py` to start the dashboard!
