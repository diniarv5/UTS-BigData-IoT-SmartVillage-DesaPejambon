import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────
# 1. KONFIGURASI HALAMAN
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Smart Auditor Pejambon",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# 2. CUSTOM CSS – Adaptive Dark / Light
# ─────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

/* ── Root Variables (Light) ── */
:root {
    --navy:       #0F2D4A;
    --blue:       #1B6CA8;
    --sky:        #3B9FD1;
    --accent:     #00C8B0;
    --success:    #22C55E;
    --danger:     #EF4444;
    --warning:    #F59E0B;

    --bg:         #F0F4F8;
    --surface:    #FFFFFF;
    --surface2:   #E8EEF5;
    --border:     rgba(15,45,74,0.12);
    --text:       #0F2D4A;
    --text-muted: #5A7089;
    --shadow:     0 4px 24px rgba(15,45,74,0.10);
    --shadow-sm:  0 2px 8px  rgba(15,45,74,0.07);
}

/* ── Root Variables (Dark) ── */
@media (prefers-color-scheme: dark) {
    :root {
        --bg:         #0A1628;
        --surface:    #0F2040;
        --surface2:   #162A50;
        --border:     rgba(0,200,176,0.15);
        --text:       #E8F0FA;
        --text-muted: #7BA3C8;
        --shadow:     0 4px 24px rgba(0,0,0,0.40);
        --shadow-sm:  0 2px 8px  rgba(0,0,0,0.30);
    }
}

/* ── Streamlit dark theme override ── */
[data-theme="dark"] {
    --bg:         #0A1628;
    --surface:    #0F2040;
    --surface2:   #162A50;
    --border:     rgba(0,200,176,0.15);
    --text:       #E8F0FA;
    --text-muted: #7BA3C8;
    --shadow:     0 4px 24px rgba(0,0,0,0.40);
    --shadow-sm:  0 2px 8px  rgba(0,0,0,0.30);
}

/* ── Base ── */
html, body, .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Main content area ── */
.main .block-container {
    padding: 2rem 2.5rem 3rem;
    max-width: 1440px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text) !important;
}
[data-testid="stSidebarNav"] {
    padding-top: 0.5rem;
}

/* ── Hero Header ── */
.hero-banner {
    background: linear-gradient(135deg, var(--navy) 0%, #1B6CA8 60%, #00C8B0 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(15,45,74,0.25);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 240px; height: 240px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 40%;
    width: 160px; height: 160px;
    border-radius: 50%;
    background: rgba(0,200,176,0.12);
}
.hero-title {
    font-size: 2rem;
    font-weight: 800;
    color: #FFFFFF !important;
    margin: 0 0 0.5rem;
    line-height: 1.2;
    position: relative; z-index: 1;
}
.hero-sub {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.80) !important;
    margin: 0;
    font-weight: 400;
    position: relative; z-index: 1;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,200,176,0.25);
    border: 1px solid rgba(0,200,176,0.50);
    color: #00FFE7 !important;
    border-radius: 50px;
    padding: 0.25rem 0.9rem;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 1rem;
    position: relative; z-index: 1;
}

/* ── Section Heading ── */
.section-heading {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 0.02em;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
    margin-left: 0.75rem;
}

/* ── KPI Cards ── */
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 4px 0 0 4px;
}
.kpi-card.blue::before   { background: var(--blue); }
.kpi-card.teal::before   { background: var(--accent); }
.kpi-card.green::before  { background: var(--success); }
.kpi-card.yellow::before { background: var(--warning); }

.kpi-icon {
    font-size: 1.6rem;
    margin-bottom: 0.6rem;
    display: block;
}
.kpi-label {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 0.3rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1;
    margin-bottom: 0.4rem;
    font-family: 'DM Mono', monospace;
}
.kpi-delta {
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 50px;
    display: inline-block;
}
.kpi-delta.pos { background: rgba(34,197,94,0.12); color: #16A34A; }
.kpi-delta.neu { background: rgba(59,159,209,0.12); color: var(--sky); }

/* ── Chart Card ── */
.chart-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1.5rem;
}
.chart-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 0.03em;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid var(--border) !important;
}

/* ── Info banner ── */
.info-strip {
    background: rgba(27,108,168,0.10);
    border: 1px solid rgba(27,108,168,0.25);
    border-radius: 10px;
    padding: 0.75rem 1.2rem;
    font-size: 0.88rem;
    color: var(--sky);
    font-weight: 500;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Footer ── */
.footer {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    text-align: center;
    font-size: 0.80rem;
    color: var(--text-muted);
    font-family: 'DM Mono', monospace;
}

/* ── Hide Streamlit default elements ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Sidebar radio buttons ── */
[data-testid="stSidebar"] .stRadio > label {
    background: var(--surface2);
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    margin-bottom: 4px;
    cursor: pointer;
    transition: background 0.15s;
}
[data-testid="stSidebar"] .stRadio > label:hover {
    background: rgba(27,108,168,0.20);
}

/* ── Streamlit metric override ── */
[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace;
    font-weight: 700;
    color: var(--text) !important;
}
[data-testid="stMetricDelta"] {
    font-size: 0.80rem !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 3. DATA MOCKUP
# ─────────────────────────────────────────
df_bansos = pd.DataFrame({
    'Program': ['PKH', 'BPNT', 'JSLUD', 'BLT-DD'],
    'KPM':     [85, 120, 45, 60],
    'Realisasi (%)': [92.4, 97.1, 88.5, 93.3],
})

df_iot = pd.DataFrame({
    'Status': ['Layak', 'Anomali (Inclusion Error)'],
    'Total':  [198, 16],
})

df_trend = pd.DataFrame({
    'Bulan': ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
    'Deteksi Anomali': [5, 8, 12, 9, 14, 16],
    'Update Data':     [420, 610, 530, 710, 680, 750],
})

# ─────────────────────────────────────────
# 4. SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 1rem;">
        <div style="font-size:3rem;">🏘️</div>
        <div style="font-weight:800; font-size:1rem; margin-top:0.3rem;">Smart Auditor</div>
        <div style="font-size:0.78rem; opacity:0.6; font-family:'DM Mono',monospace;">Desa Pejambon</div>
    </div>
    <hr style="border-color:var(--border); margin: 0.5rem 0 1.5rem;">
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigasi",
        ["📊 Dashboard Utama", "🔍 Detail Audit Lapangan", "🛰️ Log Sistem IoT"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(0,200,176,0.10); border:1px solid rgba(0,200,176,0.25);
                border-radius:10px; padding:1rem; font-size:0.82rem;">
        <div style="font-weight:700; color:#00C8B0; margin-bottom:0.4rem;">● Sistem Online</div>
        <div style="opacity:0.7;">IoT Sensor: 12/12 Aktif</div>
        <div style="opacity:0.7;">Sinkronisasi: 3 menit lalu</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="position:absolute; bottom:1.5rem; left:0; right:0; text-align:center;
                font-size:0.72rem; opacity:0.4; font-family:'DM Mono',monospace;">
        v2.0.0 · April 2026
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# 5. MAIN CONTENT
# ─────────────────────────────────────────

# ── Hero Banner ──
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">🛰️ Big Data &amp; IoT Analytics Platform</div>
    <h1 class="hero-title">Sistem Audit Bansos Cerdas<br>Smart Village Pejambon</h1>
    <p class="hero-sub">Automated Data Life Cycle · Transparansi &amp; Akuntabilitas Berbasis Data Real-time</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-strip">
    ℹ️ Data diperbarui secara otomatis setiap jam melalui integrasi sensor IoT dan validasi lapangan.
    Laporan terakhir: <strong>15 April 2026, 08:42 WIB</strong>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
if "Dashboard" in menu:

    # ── KPI Section ──
    st.markdown('<div class="section-heading">📊 Indikator Kinerja Utama</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown("""
        <div class="kpi-card blue">
            <span class="kpi-icon">🎯</span>
            <div class="kpi-label">Akurasi Data</div>
            <div class="kpi-value">96.2%</div>
            <span class="kpi-delta pos">✓ Target ≥ 95%</span>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown("""
        <div class="kpi-card yellow">
            <span class="kpi-icon">⚠️</span>
            <div class="kpi-label">Deteksi Anomali</div>
            <div class="kpi-value">16</div>
            <span class="kpi-delta neu">↑ +20% Kuartal</span>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown("""
        <div class="kpi-card teal">
            <span class="kpi-icon">⚡</span>
            <div class="kpi-label">Kecepatan Update</div>
            <div class="kpi-value">&lt;1 Jam</div>
            <span class="kpi-delta pos">● Real-time IoT</span>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown("""
        <div class="kpi-card green">
            <span class="kpi-icon">🏠</span>
            <div class="kpi-label">Cakupan KK</div>
            <div class="kpi-value">94.7%</div>
            <span class="kpi-delta pos">650 / 686 KK</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ──
    st.markdown('<div class="section-heading">📈 Visualisasi Data</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        st.markdown('<div class="chart-card"><div class="chart-title">Distribusi KPM per Program Bansos</div>', unsafe_allow_html=True)
        fig_pie = px.pie(
            df_bansos, names='Program', values='KPM',
            color_discrete_sequence=['#0F2D4A', '#1B6CA8', '#00C8B0', '#3B9FD1'],
            hole=0.45
        )
        fig_pie.update_traces(
            textposition='outside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>KPM: %{value}<extra></extra>'
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family='Plus Jakarta Sans',
            margin=dict(t=20, b=20, l=20, r=20),
            showlegend=True,
            legend=dict(orientation='h', y=-0.15),
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="chart-card"><div class="chart-title">Hasil Validasi Smart Auditor (IoT)</div>', unsafe_allow_html=True)
        fig_bar = px.bar(
            df_iot, x='Status', y='Total',
            color='Status',
            color_discrete_map={
                'Layak':                    '#22C55E',
                'Anomali (Inclusion Error)':'#EF4444'
            },
            text='Total',
        )
        fig_bar.update_traces(
            textposition='outside',
            marker_line_width=0,
            width=0.45,
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family='Plus Jakarta Sans',
            margin=dict(t=20, b=10, l=10, r=10),
            showlegend=False,
            xaxis=dict(showgrid=False, title=''),
            yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.15)', title='Jumlah KPM'),
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Trend Chart ──
    st.markdown('<div class="section-heading">📉 Tren 6 Bulan Terakhir</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card"><div class="chart-title">Deteksi Anomali Bulanan</div>', unsafe_allow_html=True)

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_trend['Bulan'], y=df_trend['Deteksi Anomali'],
        mode='lines+markers',
        name='Anomali Terdeteksi',
        line=dict(color='#EF4444', width=2.5),
        marker=dict(size=8, color='#EF4444'),
        fill='tozeroy',
        fillcolor='rgba(239,68,68,0.08)',
    ))
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family='Plus Jakarta Sans',
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.15)'),
        height=220,
    )
    st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Data Table ──
    st.markdown('<div class="section-heading">📋 Data Terintegrasi KPM Bansos 2025</div>', unsafe_allow_html=True)
    st.dataframe(
        df_bansos.style
            .background_gradient(subset=['KPM'], cmap='Blues')
            .format({'Realisasi (%)': '{:.1f}%'}),
        use_container_width=True,
        height=200,
    )

elif "Audit" in menu:
    st.markdown('<div class="section-heading">🔍 Detail Audit Lapangan</div>', unsafe_allow_html=True)
    st.info("Halaman ini menampilkan hasil audit lapangan per RW dan kategori penerima manfaat.")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("RW Sudah Diaudit", "12 / 14", "+2 minggu ini")
    with col_b:
        st.metric("Temuan Lapangan", "23 Kasus", "+5 baru")
    with col_c:
        st.metric("Tindak Lanjut", "18 Selesai", "78% resolved")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">⚙️ Modul Audit Lapangan</div>
        <p style="opacity:0.6; font-size:0.88rem;">Upload data lapangan (.xlsx / .csv) untuk sinkronisasi otomatis dengan sistem IoT dan validasi silang dengan database pusat.</p>
    </div>
    """, unsafe_allow_html=True)
    st.file_uploader("Upload Data Lapangan", type=["xlsx", "csv"])

else:
    st.markdown('<div class="section-heading">🛰️ Log Sistem IoT</div>', unsafe_allow_html=True)
    st.info("Monitoring real-time sensor IoT yang terpasang di titik distribusi bantuan sosial.")

    col_x, col_y = st.columns(2)
    with col_x:
        st.metric("Sensor Aktif", "12 / 12", "100%")
        st.metric("Paket Data Terkirim", "1,284", "+312 hari ini")
    with col_y:
        st.metric("Latensi Rata-rata", "142 ms", "-18 ms")
        st.metric("Uptime Sistem", "99.7%", "30 hari terakhir")

    st.markdown("<br>", unsafe_allow_html=True)
    log_data = pd.DataFrame({
        'Waktu':  ['08:42:10', '08:39:55', '08:35:02', '08:30:44', '08:22:17'],
        'Sensor': ['IoT-003', 'IoT-007', 'IoT-001', 'IoT-011', 'IoT-007'],
        'Event':  ['Update data KPM', 'Ping heartbeat', 'Update data KPM', 'Anomali terdeteksi', 'Update data KPM'],
        'Status': ['✅ OK', '✅ OK', '✅ OK', '⚠️ Alert', '✅ OK'],
    })
    st.dataframe(log_data, use_container_width=True, hide_index=True)

# ── Footer ──
st.markdown("""
<div class="footer">
    Pemerintah Desa Pejambon © 2026 &nbsp;·&nbsp; Powered by Big Data &amp; IoT Analytics &nbsp;·&nbsp; Smart Village Initiative
</div>
""", unsafe_allow_html=True)