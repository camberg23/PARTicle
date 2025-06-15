import streamlit as st
from openai import OpenAI

API_KEY = st.secrets['API_KEY']
# Assume API_KEY is already defined
oai = OpenAI(api_key=API_KEY)

st.title("PARTicles - Article Compression Tool")
st.markdown("*Compress articles to your preferred reading length*")

# Article input
article_text = st.text_area(
    "Paste your article here:",
    height=300,
    placeholder="Paste the full article text you want to compress..."
)

# Compression slider
compression_pct = st.slider(
    "Compression Level (% reduction)",
    min_value=10,
    max_value=90,
    value=50,
    step=10,
    help="10% = Minimal compression (keeps 90% of content) | 90% = Maximum compression (keeps 10% of content)"
)

# Visual indicator
st.caption(f"📊 Will reduce article to approximately **{100-compression_pct}%** of original length")

# Compress button
if st.button("Compress Article", type="primary"):
    if not article_text.strip():
        st.error("Please paste an article before compressing!")
    else:
        with st.spinner(f"Compressing article to {100-compression_pct}% of original..."):
            # Calculate target length
            original_words = len(article_text.split())
            target_words = int(original_words * (100 - compression_pct) / 100)
            
            # Create prompt
            prompt = f"""Compress the following article to approximately {target_words} words (about {100-compression_pct}% of the original length).
            
Maintain the key points and main narrative while removing less essential details. Keep the tone and style consistent with the original.

Original article:
{article_text}

Compressed version:"""
            
            # Call OpenAI API
            response = oai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert editor who specializes in compressing articles while maintaining their essence and readability."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=int(target_words * 1.5)  # Give some buffer
            )
            
            compressed_text = response.choices[0].message.content
            
            # Display results
            st.success("Article compressed successfully!")
            
            # Show stats
            compressed_words = len(compressed_text.split())
            actual_reduction = round((1 - compressed_words/original_words) * 100)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Original Length", f"{original_words} words")
            with col2:
                st.metric("Compressed Length", f"{compressed_words} words")
            with col3:
                st.metric("Actual Reduction", f"{actual_reduction}%")
            
            # Display compressed article
            st.markdown("### Compressed Article")
            st.write(compressed_text)