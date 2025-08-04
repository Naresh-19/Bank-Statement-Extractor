import streamlit as st
import pandas as pd
import tempfile
import os
from bank_extractor import extract_bank_statement
import io

st.set_page_config(
    page_title="Bank Statement Extractor",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #1A202C;
        color: white;
    }
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    .feature-card {
        background: linear-gradient(145deg, #2d3748, #202c3c);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #1A202C;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px -8px rgba(0, 0, 0, 0.15);
    }
    .info-card {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1.5rem 0;
        font-weight: 500;
        box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.3);
    }
    .success-card {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1.5rem 0;
        font-weight: 500;
        box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.3);
    }
    .error-card {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1.5rem 0;
        font-weight: 500;
        box-shadow: 0 4px 14px 0 rgba(239, 68, 68, 0.3);
    }
    .warning-card {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1.5rem 0;
        font-weight: 500;
        box-shadow: 0 4px 14px 0 rgba(245, 158, 11, 0.3);
    }
    .metric-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    .metric-card {
        background: linear-gradient(145deg, #2d3748, #202c3c);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #1A202C;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
        text-align: center;
        min-width: 150px;
        flex: 1;
        max-width: 200px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 500;
    }
    .column-tag {
        background: linear-gradient(135deg, #8b5cf6, #7c3aed);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.25rem;
        font-size: 0.875rem;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);
    }
    .main .block-container {
        max-width: 100% !important;
        padding: 1rem 2rem !important;
    }
    .stDataFrame > div {
        width: 100% !important;
    }
    .element-container {
        width: 100% !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px -8px rgba(59, 130, 246, 0.4);
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.875rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.3);
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px -8px rgba(16, 185, 129, 0.4);
    }
    .css-1d391kg {
        background: linear-gradient(180deg, #1A202C, #1A202C);
    }
    .center-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .flex-center {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
""", unsafe_allow_html=True)

def main():
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">Bank Statement Extractor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Extract transaction data from your bank statements with AI-powered precision</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    setup_sidebar()
    st.markdown('<div class="info-card">📤 Upload your bank statement PDF to automatically extract and analyze transaction data</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose your PDF file",
        type=['pdf'],
        help="Supported formats: PDF files with tabular transaction data",
        label_visibility="collapsed"
    )
    if uploaded_file is None:
        st.markdown("""
        <div style="text-align: center; color: #64748b; margin-top: 1rem;">
            <p><strong>📋 Drag and drop your PDF here or click to browse</strong></p>
            <p style="font-size: 0.875rem;">Maximum file size: 200MB</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if uploaded_file is not None:
        display_file_info(uploaded_file)
        if st.button("🚀 Extract Transactions", type="primary", use_container_width=True):
            process_pdf(uploaded_file)

def setup_sidebar():
    with st.sidebar:
        st.markdown("### 📋 How to Use")
        steps = [
            "📤 Upload your bank statement PDF",
            "🔍 Click 'Extract Transactions'",
            "📊 Review extracted data",
            "💾 Download CSV or Excel format"
        ]
        for i, step in enumerate(steps, 1):
            st.markdown(f"**{i}.** {step}")
        st.markdown("---")

def display_file_info(uploaded_file):
    st.markdown("---")
    st.markdown(f"""
    <div class="feature-card">
        <h4 style="text-align: center; margin-bottom: 1rem; color: white;">📄 File Information</h4>
        <div style="display: flex; justify-content: center; gap: 4rem; align-items: center;">
            <div style="text-align: center;">
                <strong>📝 File Name</strong><br>
                <span style="color: #64748b; font-size: 0.875rem;">{uploaded_file.name}</span>
            </div>
            <div style="text-align: center;">
                <strong>📊 File Size</strong><br>
                <span style="color: #64748b; font-size: 0.875rem;">{uploaded_file.size / 1024:.1f} KB</span>
            </div>
            <div style="text-align: center;">
                <strong>📄 File Type</strong><br>
                <span style="color: #64748b; font-size: 0.875rem;">PDF Document</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def process_pdf(uploaded_file):
    progress_container = st.container()
    log_container = st.container()
    results_container = st.container()
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_pdf_path = tmp_file.name
        progress_messages = []
        def progress_callback(message):
            progress_messages.append(message)
        with progress_container:
            with st.spinner("🔄 Analyzing PDF structure and extracting transactions..."):
                df, summary = extract_bank_statement(
                    temp_pdf_path, 
                    progress_callback=progress_callback
                )
        os.unlink(temp_pdf_path)
        with log_container:
            with st.expander("📋 View Processing Log", expanded=False):
                st.markdown("**Extraction Steps:**")
                for i, msg in enumerate(progress_messages, 1):
                    st.markdown(f"`{i:02d}.` {msg}")
        with results_container:
            display_modern_results(df, summary, uploaded_file.name)
    except Exception as e:
        st.markdown(f'<div class="error-card">❌ <strong>Processing Error:</strong> {str(e)}</div>', unsafe_allow_html=True)
        with st.expander("🔧 Troubleshooting Tips"):
            st.markdown("""
            **Common solutions:**
            - Ensure PDF contains text-based tables (not scanned images)
            - Check if PDF is not password protected
            - Verify the file is not corrupted
            - Try a different bank statement format
            """)
        if 'temp_pdf_path' in locals():
            try:
                os.unlink(temp_pdf_path)
            except:
                pass

def display_modern_results(df, summary, filename):
    st.markdown("---")
    if df.empty:
        st.markdown('<div class="warning-card">⚠️ <strong>No transactions found</strong><br>The PDF may not contain tabular transaction data or tables may not be properly formatted.</div>', unsafe_allow_html=True)
        with st.expander("💡 Suggestions for Better Results"):
            st.markdown("""
            **To improve extraction:**
            1. **Ensure text-based PDF:** Scanned images won't work
            2. **Check table format:** Data should be in clear tabular structure
            3. **Verify readability:** PDF should not be corrupted or password-protected
            4. **Try different statement:** Some formats work better than others
            """)
        return
    header_status = "✅ Headers auto-detected" if summary.get('header_detection_success', False) else "⚠️ Using generic headers"
    st.markdown(f'<div class="success-card">✅ <strong>Successfully extracted {len(df):,} transactions</strong><br>From: {filename}<br>{header_status}</div>', unsafe_allow_html=True)
    if summary.get('extracted_headers'):
        with st.expander("🏷️ Header Detection Details", expanded=False):
            st.markdown("**Original Headers Detected:**")
            for i, header in enumerate(summary['extracted_headers'], 1):
                st.markdown(f"`{i:02d}.` {header}")
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    st.markdown("### 📊 Extraction Summary")
    st.markdown('</div>', unsafe_allow_html=True)
    metrics_cols = st.columns(4)
    header_quality = "Auto" if summary.get('header_detection_success', False) else "Generic"
    metrics = [
        ("📋", "Transactions", f"{summary['total_transactions']:,}"),
        ("🗂️", "Columns", f"{len(summary['columns'])}"),
        ("📅", "Date Range", summary['date_range'] if summary['date_range'] else "Not detected"),
        ("🏷️", "Headers", header_quality)
    ]
    for i, (icon, label, value) in enumerate(metrics):
        with metrics_cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    st.markdown("### 🏷️ Detected Columns")
    st.markdown('</div>', unsafe_allow_html=True)
    columns_html = ""
    for col_name in summary['columns']:
        columns_html += f'<span class="column-tag">{col_name}</span>'
    st.markdown(f'<div style="text-align: center; margin: 1rem 0;">{columns_html}</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    st.markdown("### 📑 Transaction Data Preview")
    st.markdown('</div>', unsafe_allow_html=True)
    st.dataframe(
        df,
        use_container_width=True,
        height=500,
        hide_index=True
    )
    st.markdown("---")
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    st.markdown("### 💾 Export Options")
    st.markdown('</div>', unsafe_allow_html=True)
    download_cols = st.columns([2, 1, 1, 2])
    csv_data = df.to_csv(index=False)
    base_filename = filename.replace('.pdf', '')
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Transactions')
        summary_data = [
            ['Total Transactions', summary['total_transactions']],
            ['Columns Detected', len(summary['columns'])],
            ['Date Range', summary['date_range'] if summary['date_range'] else 'Not detected'],
            ['Header Detection', 'Success' if summary.get('header_detection_success', False) else 'Failed - Used Generic'],
            ['Source File', filename]
        ]
        if summary.get('extracted_headers'):
            summary_data.append(['Detected Headers', ', '.join(summary['extracted_headers'])])
        summary_df = pd.DataFrame(summary_data, columns=['Metric', 'Value'])
        summary_df.to_excel(writer, index=False, sheet_name='Summary')
    excel_data = buffer.getvalue()
    with download_cols[1]:
        st.download_button(
            label="📊 Download CSV",
            data=csv_data,
            file_name=f"transactions_{base_filename}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with download_cols[2]:
        st.download_button(
            label="📈 Download Excel",
            data=excel_data,
            file_name=f"transactions_{base_filename}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    st.markdown("---")
    with st.expander("📋 Export Information"):
        st.markdown("""
        **CSV Format:**
        - Plain text format, compatible with all spreadsheet applications
        - Preserves all extracted data and column structure

        **Excel Format:**
        - Contains two sheets: 'Transactions' and 'Summary'
        - Enhanced formatting and metadata included
        - Compatible with Microsoft Excel and Google Sheets
        """)

if __name__ == "__main__":
    main()