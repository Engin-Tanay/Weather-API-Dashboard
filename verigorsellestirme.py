import pandas as pd
import streamlit as st

# Sayfa ayarları
st.set_page_config(
    page_title="Celebrity Analytics Dashboard",
    layout="wide"
)

# Veri seti
df = pd.read_csv(
    r"C:\Users\engin\Desktop\popular_people.csv"
)

# Gender dönüşümü
gender_map = {
    0: "Unknown",
    1: "Female",
    2: "Male",
    3: "Non-Binary"
}

df["gender_name"] = df["gender"].map(gender_map)

# Başlık
st.title("Celebrity Analytics Dashboard")

# Metrikler
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Toplam Kişi",
        len(df)
    )

with col2:
    st.metric(
        "Departman Sayısı",
        df["known_for_department"].nunique()
    )

with col3:
    st.metric(
        "Ortalama Popülerlik",
        round(df["popularity"].mean(), 2)
    )

st.divider()

# Cinsiyet dağılımı
st.subheader("Cinsiyet Dağılımı")

st.bar_chart(
    df["gender_name"].value_counts()
)

# Bölüm dağılımı
st.subheader("Departman Dağılımı")

st.bar_chart(
    df["known_for_department"].value_counts()
)

# En popüler 10 kişi
st.subheader("En Popüler 10 Kişi")

top10 = df.nlargest(
    10,
    "popularity"
)

st.bar_chart(
    top10[["name", "popularity"]]
    .set_index("name")
)

# Departmanlara göre ortalama popülerlik
st.subheader(
    "Departmanlara Göre Ortalama Popülerlik"
)

dept_popularity = (
    df.groupby("known_for_department")
      ["popularity"]
      .mean()
      .sort_values(ascending=False)
)

st.bar_chart(dept_popularity)

# En popüler kadınlar
st.subheader("En Popüler 10 Kadın")

top_female = (
    df[df["gender"] == 1]
    .nlargest(10, "popularity")
)

st.bar_chart(
    top_female[["name", "popularity"]]
    .set_index("name")
)

# En popüler erkekler
st.subheader("En Popüler 10 Erkek")

top_male = (
    df[df["gender"] == 2]
    .nlargest(10, "popularity")
)

st.bar_chart(
    top_male[["name", "popularity"]]
    .set_index("name")
)

st.divider()

# Departman filtresi
st.subheader("Departmana Göre Kişiler")

department = st.selectbox(
    "Departman Seç",
    sorted(df["known_for_department"].dropna().unique())
)

filtered_df = df[
    df["known_for_department"] == department
]

st.dataframe(
    filtered_df[
        [
            "name",
            "gender_name",
            "popularity"
        ]
    ],
    use_container_width=True
)

st.divider()

# İsim arama
st.subheader("Kişi Ara")

search = st.text_input(
    "İsim Giriniz"
)

if search:

    result = df[
        df["name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        result[
            [
                "name",
                "gender_name",
                "known_for_department",
                "popularity"
            ]
        ],
        use_container_width=True
    )