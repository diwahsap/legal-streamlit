from st_pages import Page, show_pages

"## Declaring the pages in your app:"

show_pages(
    [
        Page("pages/home.py", "Dasbor", "🏠"),
        Page("pages/show.py", "Tampilkan Data Sekarang", ":books:"),
        Page("pages/pdf_text.py", "Tambahkan Data", "📝 "),
        Page("pages/antar_tingkat.py", "Analisis Keselarasan", "🧐"),
        Page("pages/viz.py", "Visualisasi Graf", "🔢")
        Page("pages/selection.py", "Visualisasi Berdasarkan Topik", "🔢")
    ]
)