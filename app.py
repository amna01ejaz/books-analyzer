import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Setup
st.set_page_config(page_title="Codédex Book Analyzer", layout="wide")
st.title("📚 Best-Selling Books Analytics Console")
st.write("Filter, search, and analyze historical best-selling book metrics dynamically.")

# 2. Mock Dataset Generation (Self-contained, cloud-safe)
@st.cache_data
def load_book_data():
    data = {
        "Title": [
            "The Hobbit", "Harry Potter and the Philosopher's Stone", 
            "The Da Vinci Code", "The Catcher in the Rye", 
            "The Great Gatsby", "To Kill a Mockingbird",
            "1984", "Animal Farm", "The Little Prince"
        ],
        "Author": [
            "J.R.R. Tolkien", "J.K. Rowling", "Dan Brown", 
            "J.D. Salinger", "F. Scott Fitzgerald", "Harper Lee",
            "George Orwell", "George Orwell", "Antoine de Saint-Exupéry"
        ],
        "Genre": ["Fantasy", "Fantasy", "Mystery", "Classic", "Classic", "Classic", "Dystopian", "Dystopian", "Children's"],
        "Year Published": [1937, 1997, 2003, 1951, 1925, 1960, 1949, 1945, 1943],
        "Approximate Sales (Millions)": [100, 120, 80, 65, 30, 40, 30, 20, 140],
        "User Rating": [4.7, 4.8, 3.9, 4.0, 4.4, 4.5, 4.6, 4.3, 4.8]
    }
    return pd.DataFrame(data)

df = load_book_data()

# 3. Sidebar Controls for Searching and Filtering
st.sidebar.header("Search & Filters")

# Text search tool
search_query = st.sidebar.text_input("🔍 Search by Title or Author:", "").strip().lower()

# Year range slider tool
min_year, max_year = int(df["Year Published"].min()), int(df["Year Published"].max())
year_range = st.sidebar.slider(
    "📆 Select Publication Year Range:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# 4. Applying Filter Logic
filtered_df = df[
    (df["Year Published"] >= year_range[0]) & 
    (df["Year Published"] <= year_range[1])
]

if search_query:
    filtered_df = filtered_df[
        filtered_df["Title"].str.lower().str.contains(search_query) | 
        filtered_df["Author"].str.lower().str.contains(search_query)
    ]

# 5. Summary KPI Cards
if not filtered_df.empty:
    total_books = len(filtered_df)
    total_sales = filtered_df["Approximate Sales (Millions)"].sum()
    avg_rating = filtered_df["User Rating"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Books Found", value=total_books)
    col2.metric(label="Combined Sales", value=f"{total_sales}M copies")
    col3.metric(label="Average User Rating", value=f"{avg_rating:.2f} / 5.0")
    
    st.write("---")

    # 6. Interactive Visualizations Grid
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("📊 Copies Sold vs. User Rating")
        fig_scatter = px.scatter(
            filtered_df,
            x="Approximate Sales (Millions)",
            y="User Rating",
            color="Genre",
            hover_name="Title",
            size="Approximate Sales (Millions)",
            template="plotly_dark",
            labels={"Approximate Sales (Millions)": "Sales (Millions)", "User Rating": "Rating"}
        )
        st.plotly_chart(fig_scatter, width="stretch")

    with chart_col2:
        st.subheader("⏳ Publication Timeline Visual")
        fig_line = px.bar(
            filtered_df.sort_values("Year Published"),
            x="Year Published",
            y="Approximate Sales (Millions)",
            hover_data=["Title", "Author"],
            color="Genre",
            template="plotly_dark"
        )
        st.plotly_chart(fig_line, width="stretch")

    # 7. Structured Data Output View
    st.subheader("📋 Filtered Books Catalog")
    st.dataframe(filtered_df, width="stretch")
else:
    st.warning("No books match your current search queries or filter settings. Try adjusting the sidebar parameters!")