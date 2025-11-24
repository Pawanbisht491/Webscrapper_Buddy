import io
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama

def try_to_dataframe(parsed_text):
    """
    Try multiple safe strategies to convert parsed_text to DataFrame:
     1) If it's already in a newline-separated table with tab/| or comma separators -> parse
     2) If it contains HTML table -> read_html
     3) Otherwise last-resort: put whole text in single-column DF
    """
    # 1) try html table
    try:
        dfs = pd.read_html(parsed_text)
        if dfs:
            return dfs[0]
    except Exception:
        pass

    # 2) try CSV-like (tab, pipe, comma)
    lines = [l.strip() for l in parsed_text.splitlines() if l.strip()]
    if not lines:
        return pd.DataFrame()

    # detect separator using the header row heuristics
    header = lines[0]
    for sep in ['\t', '|', ',', ';']:
        if sep in header:
            try:
                df = pd.read_csv(io.StringIO("\n".join(lines)), sep=sep)
                return df
            except Exception:
                pass

    # 3) Try whitespace-split columns (if consistent)
    parts = [row.split() for row in lines]
    if len(parts) >= 2:
        # if all rows have same number of tokens => build columns
        lens = [len(p) for p in parts]
        if len(set(lens)) == 1 and lens[0] > 1:
            df = pd.DataFrame(parts[1:], columns=parts[0])
            return df

    # 4) fallback: single-column DataFrame
    return pd.DataFrame({"text": lines})

def df_to_excel_bytes(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="parsed")
    return output.getvalue()

def df_to_pdf_bytes(df, title="Parsed Table"):
    # Render DataFrame as matplotlib table and save to PDF in-memory
    fig, ax = plt.subplots(figsize=(8.5, max(2, 0.4 * len(df))))
    ax.axis('off')
    ax.set_title(title)
    # create table
    tbl = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.scale(1, 1.2)
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf.read()

st.title("Web_Scraper Buddy")
url = st.text_input("Enter Website URL")

if st.button("Scrape Site"):
    st.write(f"Scraping the website")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)    

    st.session_state.dom_content = cleaned_content
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Parse the content with Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.write(parsed_result)

            df = try_to_dataframe(parsed_result)

            # show a preview
            st.subheader("Parsed table preview")
            st.dataframe(df)

            # Prepare downloads
            excel_bytes = df_to_excel_bytes(df)
            pdf_bytes = df_to_pdf_bytes(df)

            st.download_button(
            "Download Excel (.xlsx)",
            data=excel_bytes,
            file_name="parsed_courses.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.download_button(
                "Download PDF (.pdf)",
                data=pdf_bytes,
                file_name="parsed_courses.pdf",
                mime="application/pdf"
            )
