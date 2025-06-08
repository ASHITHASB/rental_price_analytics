
# Rental Price Analytics + Smart Rent Advisor

This project is a Streamlit-based MVP that:
- Scrapes rental listings (NoBroker)
- Visualizes rent trends and amenities
- Uses Hugging Face's `flan-t5-base` to give AI-backed rent fairness suggestions

## How to Run

1. Clone the repo
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Scrape listings:
   ```bash
   python scraper.py
   ```
4. Run app:
   ```bash
   streamlit run app.py
   ```

## Sample Output
- Price bands
- Seasonality trend
- Smart explanation of rent pricing (LLM)

