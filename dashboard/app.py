import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Segmenlytics - Customer Segmentation",
    layout="wide",
    page_icon="📊"
)

# CUSTOM CSS
page_css = """
<style>

html, body, [data-testid="stAppViewContainer"] {
    font-family: "Segoe UI", sans-serif;
}

/* Background gradient */
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(145deg, #002B5B 0%, #034078 40%, #1282A2 100%);
    padding-top: 0rem !important;
}

/* ===== HEADER BIRU FULL WIDTH ===== */
.full-header {
    width: 100%;
    background: #002B5B;
    padding: 32px 50px;
    border-bottom: 3px solid #1B3C68;
    box-shadow: 0 4px 25px rgba(0,0,0,0.25);
    margin-bottom: 28px;
    text-align: center;
    border-radius: 25px;
}

.header-title {
    font-size: 46px;
    font-weight: 800;
    color: #ffffff !important;
    margin: 0;
}

.header-sub {
    font-size: 18px;
    margin-top: 6px;
    color: #e0ecff;
}

/* Sidebar collapsible effect */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E8F1FF, #ffffff);
    border-right: 2px solid #d0def7;
    transition: all 0.3s ease;
}

[data-testid="stSidebar"][aria-expanded="false"] {
    width: 0 !important;
    opacity: 0;
}

/* Card putih */
.card {
    background: #ffffffee;
    padding: 22px 26px;
    border-radius: 16px;
    box-shadow: 0 8px 26px rgba(0,0,0,0.18);
    margin-bottom: 22px;
    backdrop-filter: blur(5px);
}

/* Section Title */
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #002B5B;
    margin-bottom: 14px;
}

.persona {
    background: #f3f8ff;
    padding: 18px;
    border-radius: 14px;
    border-left: 6px solid #00509D;
    margin-bottom: 18px;
    box-shadow: 0 5px 14px rgba(0,0,0,0.08);
}

</style>
"""
st.markdown(page_css, unsafe_allow_html=True)

# LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("rfm_with_cluster.csv")
    df.columns = df.columns.str.lower()
    df["cluster"] = df["cluster"].astype(int)
    return df

df = load_data()

# Column check
required = ["recency", "frequency", "monetary", "cluster"]
if any(col not in df.columns for col in required):
    st.error("Dataset tidak memiliki kolom lengkap RFM.")
    st.stop()

cluster_map = {
    0: "active customer",
    1: "at-risk customer",
    2: "active big spender",
    3: "at-risk big spender"
}
df["cluster_name"] = df["cluster"].map(cluster_map)

CLUSTER_COLORS = {
    "active customer": "#00509D",
    "at-risk customer": "#00A8E8",
    "active big spender": "#002B5B",
    "at-risk big spender": "#1282A2"
}

# HEADER 
st.markdown("""
<div class="full-header">
    <h1 class="header-title">Segmenlytics</h1>
    <div class="header-sub">Customer Segmentation Dashboard powered by RFM Analysis</div>
</div>
""", unsafe_allow_html=True)

# HEADER METRICS 
colA, colB, colC = st.columns(3)
colA.metric("Total Customers", f"{df.shape[0]:,}")
colB.metric("Total Clusters", df['cluster'].nunique())
colC.metric("Dominant Segment", df['cluster_name'].mode()[0].title())

# SIDEBAR
st.sidebar.title("⚙ Controls")
cluster_options = ["All"] + sorted(df["cluster_name"].unique())
selected_cluster = st.sidebar.selectbox("Filter Cluster", cluster_options)

show_3d = st.sidebar.checkbox("Show 3D RFM Scatter", True)
show_distribution = st.sidebar.checkbox("Show RFM Distributions", True)
show_radar = st.sidebar.checkbox("Show Radar Chart", True)

data = df if selected_cluster == "All" else df[df["cluster_name"] == selected_cluster]

# OVERVIEW METRICS
st.markdown('<div class="section-title">Overview Metrics</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Filtered Customers", f"{data.shape[0]:,}")
c2.metric("Avg Recency", f"{data['recency'].mean():.1f}")
c3.metric("Avg Frequency", f"{data['frequency'].mean():.2f}")
c4.metric("Avg Monetary", f"${data['monetary'].mean():.0f}")

# VISUALISASI
# Layout utama: left slim column + right main column
left_col, right_col = st.columns([1, 2])

# Donut + Average RFM Scores by Segment
with left_col:
    st.markdown('<div class="section-title">Cluster Composition</div>', unsafe_allow_html=True)

    counts = df["cluster_name"].value_counts().reset_index()
    counts.columns = ["cluster_name", "count"]

    fig_donut = go.Figure(
        go.Pie(
            labels=counts["cluster_name"],
            values=counts["count"],
            hole=0.55,
            marker=dict(colors=[CLUSTER_COLORS.get(c, "#0074B7") for c in counts["cluster_name"]]),
            hoverinfo="label+percent+value",
            textinfo="percent"
        )
    )
    fig_donut.update_layout(
        margin=dict(t=10, b=10, l=0, r=0),
        showlegend=True,
        legend=dict(orientation="v", x=0.98, y=0.5, bgcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")  # spacer

    st.markdown('<div class="section-title">Average RFM Scores by Segment</div>', unsafe_allow_html=True)

    avg = df.groupby("cluster_name")[["recency", "frequency", "monetary"]].mean().reset_index()
    avg = avg.sort_values("monetary", ascending=False)

    avg_melt = avg.melt(id_vars="cluster_name", value_vars=["recency", "frequency", "monetary"],
                        var_name="metric", value_name="value")
    METRIC_COLORS = {"recency": "#8FD3D0", "frequency": "#00509D", "monetary": "#1282A2"}

    fig_bar = px.bar(
        avg_melt,
        x="cluster_name",
        y="value",
        color="metric",
        barmode="group",
        color_discrete_map=METRIC_COLORS,
        labels={"cluster_name": "Cluster", "value": "Mean Value", "metric": "Metric"},
        title=""
    )
    fig_bar.update_layout(margin=dict(t=6, b=10))
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# visualisasi interaktif
with right_col:
    st.markdown('<div class="section-title">RFM Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="note">Tip: hover pada titik untuk melihat nilai rinci. Gunakan sidebar untuk menampilkan/menyembunyikan 3D visual.</div>', unsafe_allow_html=True)

    if show_3d:
        fig3d = px.scatter_3d(
            data,
            x="recency",
            y="frequency",
            z="monetary",
            color="cluster_name",
            color_discrete_map=CLUSTER_COLORS,
            size="monetary",
            hover_data=["recency", "frequency", "monetary"],
            labels={"recency": "Recency (days)", "frequency": "Frequency", "monetary": "Monetary"},
            title="Recency vs Frequency vs Monetary (3D)"
        )
        fig3d.update_layout(scene=dict(xaxis_title='Recency', yaxis_title='Frequency', zaxis_title='Monetary'),
                            legend_title_text='Cluster', height=620, margin=dict(t=40))
        st.plotly_chart(fig3d, use_container_width=True)
    else:
        fig2 = px.scatter(
            data,
            x="recency",
            y="monetary",
            size="frequency",
            color="cluster_name",
            color_discrete_map=CLUSTER_COLORS,
            hover_data=["recency", "frequency", "monetary"],
            labels={"recency": "Recency (days)", "monetary": "Monetary"},
            title="Recency vs Monetary (bubble size = frequency)"
        )
        fig2.update_layout(title_x=0.5, height=580, margin=dict(t=40))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# DISTRIBUTION BOX + KORELASI
st.markdown('<div class="section-title">Distribution Analysis & Correlation Matrix</div>', unsafe_allow_html=True)

dist_c1, dist_c2 = st.columns(2)

with dist_c1:
    if show_distribution:
        fig_box_r = px.box(df, x="cluster_name", y="recency", color="cluster_name",
                           color_discrete_map=CLUSTER_COLORS,
                           labels={"recency": "Recency (days)", "cluster_name": "Cluster"},
                           title="Distribusi Recency per Cluster")
        fig_box_r.update_layout(margin=dict(t=30, b=10))
        st.plotly_chart(fig_box_r, use_container_width=True)

        fig_box_f = px.box(df, x="cluster_name", y="frequency", color="cluster_name",
                           color_discrete_map=CLUSTER_COLORS,
                           labels={"frequency": "Frequency"},
                           title="Distribusi Frequency per Cluster")
        fig_box_f.update_layout(margin=dict(t=30, b=10))
        st.plotly_chart(fig_box_f, use_container_width=True)

with dist_c2:
    if show_distribution:
        fig_box_m = px.box(df, x="cluster_name", y="monetary", color="cluster_name",
                           color_discrete_map=CLUSTER_COLORS,
                           labels={"monetary": "Monetary"},
                           title="Distribusi Monetary per Cluster")
        fig_box_m.update_layout(margin=dict(t=30, b=10))
        st.plotly_chart(fig_box_m, use_container_width=True)

    corr = df[["recency", "frequency", "monetary"]].corr()
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="Blues", title="Korelasi Antar Fitur RFM")
    fig_corr.update_layout(margin=dict(t=20, b=10), height=360)
    st.plotly_chart(fig_corr, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# RADAR CHART 
if show_radar:
    st.markdown('<div class="section-title">RFM Radar Comparison by Customer Segment</div>', unsafe_allow_html=True)

    radar_df = df.groupby("cluster_name")[["recency", "frequency", "monetary"]].mean().reset_index()

    # normalize 0–1 per column
    radar_norm = radar_df.copy()
    for col in ["recency", "frequency", "monetary"]:
        radar_norm[col] = (radar_df[col] - radar_df[col].min()) / (radar_df[col].max() - radar_df[col].min() + 1e-9)

    categories = ["recency", "frequency", "monetary"]
    fig_radar = go.Figure()
    for _, row in radar_norm.iterrows():
        vals = row[categories].tolist()
        fig_radar.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=[c.title() for c in categories] + [categories[0].title()],
            fill='toself',
            name=row["cluster_name"]
        ))

    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True, height=520, margin=dict(t=20))
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# CUSTOMER PERSONAS 
st.markdown("""
<div class="section-title" style="display:flex;align-items:center;gap:8px;">
    Customer Personas - Insight & Recommended Actions
    <div class="tooltip">ℹ️
        <span class="tooltiptext">
            <b>Upsell</b>: mengajak pelanggan membeli versi lebih lengkap.<br><br>
            <b>Win-back</b>: kampanye untuk mengajak pelanggan yang hampir hilang agar kembali.<br><br>
            <b>Retention</b>: menjaga agar pelanggan tetap aktif dan terus membeli.<br><br>
            <b>Churn</b>: kondisi ketika pelanggan berhenti membeli atau tidak kembali lagi.<br><br>
            <b>VIP Program</b>: program eksklusif untuk pelanggan bernilai tinggi.
        </span>
    </div>
</div>

<style>
.tooltip {
  position: relative;
  display: inline-block;
  cursor: pointer;
  font-weight: bold;
  color: #1b4f72;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 240px;
  background-color: #f4f9ff;
  color: #1b4166;
  text-align: left;
  border-radius: 8px;
  padding: 10px 12px;
  position: absolute;
  z-index: 1;
  top: 24px;
  left: -20px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
  font-size: 12px;
  line-height: 1.4;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
""", unsafe_allow_html=True)

persona_full = {
    "active customer": {
        "title": "Active Customer",
        "summary": "Pelanggan yang masih aktif membeli meski nilai belanjanya tidak tinggi. Stabil dan punya potensi loyal.",
        "pain_points": [
            "Terlalu banyak email promosi membuat tidak nyaman",
            "Butuh alasan jelas untuk meningkatkan pembelian"
        ],
        "opportunities": [
            "Memberikan rekomendasi produk sesuai riwayat pembelian",
            "Program poin atau reward sederhana"
        ],
        "actions": [
            "Kirim email personal bulanan berisi rekomendasi produk",
            "Tawarkan program loyalitas berbasis poin"
        ]
    },

    "at-risk customer": {
        "title": "At-Risk Customer",
        "summary": "Aktivitas menurun dan berpotensi berhenti membeli. Perlu perhatian sebelum benar-benar hilang.",
        "pain_points": [
            "Merasa promosi yang diterima terlalu umum dan tidak relevan",
            "Tidak ada dorongan kuat untuk kembali membeli"
        ],
        "opportunities": [
            "Kampanye khusus untuk mengajak kembali",
            "Promo terbatas yang memberi urgensi"
        ],
        "actions": [
            "Jalankan alur reaktivasi: email → SMS → voucher",
            "Diskon yang disesuaikan untuk mendorong pembelian ulang"
        ]
    },

    "active big spender": {
        "title": "Active Big Spender",
        "summary": "Pelanggan bernilai tinggi yang sering membeli. Sangat cocok untuk program premium dan VIP.",
        "pain_points": [
            "Mengharapkan kualitas layanan yang lebih premium",
            "Sangat sensitif dengan ketersediaan produk"
        ],
        "opportunities": [
            "Program VIP dengan layanan eksklusif",
            "Akses lebih awal untuk produk baru"
        ],
        "actions": [
            "Berikan account manager khusus atau layanan personal",
            "Undang ke event eksklusif atau early-access produk"
        ]
    },

    "at-risk big spender": {
        "title": "At-Risk Big Spender",
        "summary": "Dulu pelanggan bernilai tinggi, tetapi kini jarang membeli. Jika hilang, dampaknya besar pada pendapatan.",
        "pain_points": [
            "Merasa kurang diperhatikan secara personal",
            "Mendapatkan penawaran lebih menarik dari kompetitor"
        ],
        "opportunities": [
            "Penawaran retensi langsung untuk mencegah churn",
            "Pendekatan personal bernilai tinggi"
        ],
        "actions": [
            "Hubungi secara personal dan berikan penawaran khusus",
            "Kirim survei singkat untuk tahu alasan menurun"
        ]
    }
}

# Render two-column persona cards
pc1, pc2 = st.columns(2)
idx = 0
for key, info in persona_full.items():
    col = pc1 if idx % 2 == 0 else pc2
    with col:
        color = CLUSTER_COLORS.get(key, "#00509D")
        st.markdown(f"""
        <div class="persona">
            <h4 style="margin:0;color:{color};text-transform:capitalize;">{info['title']}</h4>
            <p style="margin:8px 0 6px 0;"><b>Summary</b>: {info['summary']}</p>
            <p style="margin:6px 0 4px 0;"><b>Pain points</b>:</p>
            <ul>
                {''.join([f'<li>{p}</li>' for p in info['pain_points']])}
            </ul>
            <p style="margin:6px 0 4px 0;"><b>Opportunity</b>:</p>
            <ul>
                {''.join([f'<li>{o}</li>' for o in info['opportunities']])}
            </ul>
            <p style="margin:6px 0 4px 0;"><b>Recommended actions</b>:</p>
            <ul>
                {''.join([f'<li>{a}</li>' for a in info['actions']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    idx += 1

st.markdown('</div>', unsafe_allow_html=True)

# Business Strategic Overview
st.markdown("""
<div class="section-title" style="display:flex;align-items:center;gap:8px;">
    Business Strategic Overview
    <div class="tooltip">ℹ️
        <span class="tooltiptext">
            <b>CAC (Customer Acquisition Cost)</b>: biaya rata-rata untuk mendapatkan satu pelanggan baru.<br><br>
            <b>A/B Testing</b>: membandingkan dua versi konten atau strategi (A dan B) untuk melihat mana yang paling efektif dalam meningkatkan performa.<br><br>
            <b>Personalized Outreach</b>: pendekatan komunikasi yang disesuaikan dengan perilaku atau kebutuhan pelanggan (bukan pesan massal), misalnya pesan personal ke pelanggan prioritas.
        </span>
    </div>
</div>

<style>
.tooltip {
  position: relative;
  display: inline-block;
  cursor: pointer;
  font-weight: bold;
  color: #1b4f72;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 260px;
  background-color: #f4f9ff;
  color: #1b4166;
  text-align: left;
  border-radius: 8px;
  padding: 10px 12px;
  position: absolute;
  z-index: 1;
  top: 24px;
  left: -20px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
  font-size: 12px;
  line-height: 1.4;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<p><b>Executive Summary:</b></p>
<ol>
<li><b>Identifikasi:</b> Analisis RFM menghasilkan 4 segmen pelanggan dengan perilaku berbeda. 
Prioritas pertama adalah menjaga segmen <i>Active Big Spender</i> dan memulihkan <i>At-Risk Big Spender</i> 
karena kontribusinya paling besar terhadap pendapatan.</li>

<li><b>Tindakan:</b> Jalankan dua jalur paralel:
    <ul>
        <li><b>Retention & Loyalty</b> untuk pelanggan aktif (cluster 0 dan 2)</li>
        <li><b>Win-Back & Personalized Outreach</b> untuk pelanggan at-risk (cluster 1 dan 3)</li>
    </ul>
</li>

<li><b>Pengukuran:</b> Pantau perubahan dalam 30–90 hari pada:
    <ul>
        <li>Retention rate per cluster</li>
        <li>Rata-rata nilai belanja (monetary)</li>
        <li>Konversi dari kampanye win-back</li>
        <li>CAC per segment</li>
    </ul>
</li>

<li><b>Optimasi:</b> Lakukan A/B testing untuk menemukan pesan, kanal, dan penawaran paling efektif 
(email vs WhatsApp vs SMS).</li>
</ol>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# DOWNLOAD TABLE
st.markdown('<div class="section-title">Export & Quick Table</div>', unsafe_allow_html=True)

# quick aggregated table per cluster
agg = df.groupby(["cluster", "cluster_name"]).agg(
    customers=("cluster", "count"),
    avg_recency=("recency", "mean"),
    avg_frequency=("frequency", "mean"),
    avg_monetary=("monetary", "mean")
).reset_index()

agg = agg.sort_values("cluster")

styled_table = (
    agg[["cluster_name","customers","avg_recency","avg_frequency","avg_monetary"]]
    .style.set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#e3f0ff"),
                ("color", "#003366"),
                ("font-weight", "bold"),
                ("border", "1px solid #d0d7e1")
            ]
        },
        {
            "selector": "td",
            "props": [
                ("border", "1px solid #e6e6e6")
            ]
        }
    ])
    .format({
        "customers": "{:,}",
        "avg_recency": "{:.1f}",
        "avg_frequency": "{:.2f}",
        "avg_monetary": "${:,.0f}"
    })
)

st.table(styled_table)

# DOWNLOAD BUTTON
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download full dataset (CSV)", csv, "segmenlytics_rfm.csv", "text/csv")

st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("<div style='text-align:center;margin-top:18px;color:#eaf6ff;'>Segmenlytics — actionable RFM dashboard. Built with Plotly & Streamlit.</div>", unsafe_allow_html=True)