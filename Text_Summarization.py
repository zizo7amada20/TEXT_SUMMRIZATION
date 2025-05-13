
import streamlit as st
import fitz  # PyMuPDF to read PDFs
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer

# ----- Page Config -----
st.set_page_config(page_title="Text Summarizer", page_icon="📝", layout="centered")

# ----- Custom CSS -----
st.markdown("""
    <style>
    body, .main {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a1d);
        background-size: 400% 400%;
        animation: gradientMove 15s ease infinite;
        color: #f0f0f0;
    }

    @keyframes gradientMove {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .block-container {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 0 30px #8a2be2;
    }

    h1 {
        color: #bb86fc;
        text-align: center;
        font-size: 2.8rem;
        font-weight: bold;
    }

    h3 {
        color: #e0e0e0;
        text-align: center;
    }

    .stTextArea textarea {
        background-color: #2a2a2a;
        color: #f0f0f0;
        border-radius: 12px;
        border: 1px solid #555;
    }

    .stButton>button {
        background-color: #bb86fc;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        transition: 0.3s ease;
        box-shadow: 0 0 10px #bb86fc, 0 0 20px #bb86fc inset;
    }

    .stButton>button:hover {
        background-color: #9b59b6;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# ----- Title -----
st.title('📝 Text Summarization Application')
st.markdown("### ✨ Enter your text below or upload a PDF file, then choose a summarization method.")

# ----- PDF Upload -----
uploaded_file = st.file_uploader("📄 Upload a PDF File", type=["pdf"])
pdf_text = ""

if uploaded_file is not None:
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            pdf_text += page.get_text()

# ----- User Input -----
default_text = st.text_area('✍️ Please, Enter a Text to Summarize:', height=200)
text = pdf_text if pdf_text.strip() else default_text

col1, col2 = st.columns(2)

with col1:
    options = st.selectbox('📚 Choose Summarizer Type:', ('LSA', 'Luhn', 'LexRank', 'TextRank'))

    # Showing explanation based on user selection
    if options == 'LSA':
        st.info("**LSA** (Latent Semantic Analysis): Extracts important sentences based on the latent topics in the text.")
    elif options == 'Luhn':
        st.info("**Luhn**: Focuses on sentences with high-frequency significant words, ignoring less important ones.")
    elif options == 'LexRank':
        st.info("**LexRank**: Uses a graph-based approach to rank sentences by their importance.")
    elif options == 'TextRank':
        st.info("**TextRank**: Similar to LexRank but with different scoring based on sentence relationships.")

with col2:
    sentence_count = st.selectbox('🧮 Number of Sentences:', [5, 10, 20, 30])

# ----- Summarization Function -----
def Summarize_Text(text, summarizer_type='LSA', sentence_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer('English'))

    if summarizer_type == 'LSA':
        summarizer = LsaSummarizer()
    elif summarizer_type == 'Luhn':
        summarizer = LuhnSummarizer()
    elif summarizer_type == 'LexRank':
        summarizer = LexRankSummarizer()
    elif summarizer_type == 'TextRank':
        summarizer = TextRankSummarizer()

    summary = summarizer(parser.document, sentence_count)
    return ' '.join(str(sentence) for sentence in summary)

# ----- Statistics Function -----
def text_statistics(text):
    words = len(text.split())
    characters = len(text)
    sentences = text.count('.') + text.count('!') + text.count('?') + text.count('؟')
    return words, characters, sentences

# ----- Summarize Button -----
if st.button('🚀 Summarize Text'):
    if text.strip():
        # Before Summarization stats
        words_before, chars_before, sent_before = text_statistics(text)
        st.markdown("## 📊 Text Statistics (Before Summarization):")
        st.write(f"- Words: {words_before}")
        st.write(f"- Characters: {chars_before}")
        st.write(f"- Sentences (estimated): {sent_before}")

        # Summarization
        summary = Summarize_Text(text, options, sentence_count)

        # After Summarization stats
        words_after, chars_after, sent_after = text_statistics(summary)
        st.markdown("## 📄 Text Summary:")
        st.success(summary)

        st.markdown("## 📊 Text Statistics (After Summarization):")
        st.write(f"- Words: {words_after}")
        st.write(f"- Characters: {chars_after}")
        st.write(f"- Sentences : {sent_after}")

        # --- Download button ---
        st.download_button(
            label="💾 Download Summary",
            data=summary,
            file_name="summary.txt",
            mime="text/plain"
        )
    else:
        st.warning('⚠️ Please enter some text first.')
