import io
import streamlit as st
from pptx import Presentation

# ---------------------------
# UI inputs (assuming these are defined earlier in your app)
# ---------------------------
input_text = st.text_area("Paste your text here:")
uploaded_template = st.file_uploader("Upload a PowerPoint template", type=["pptx", "potx"])
guidance = st.text_input("Guidance (optional):")
provider = st.selectbox("Select Provider", ["None (local heuristic)", "OpenAI", "Anthropic"])
api_key = st.text_input("API Key (if needed)", type="password")
model = st.text_input("Model (optional)")
min_slides = st.number_input("Min Slides", min_value=1, value=3)
max_slides = st.number_input("Max Slides", min_value=1, value=10)
add_speaker_notes = st.checkbox("Add Speaker Notes", value=True)

generate_btn = st.button("🚀 Generate Presentation")

# ---------------------------
# Main action
# ---------------------------
if generate_btn:
    if not input_text.strip():
        st.error("Please paste some input text to proceed.")
        st.stop()

    if uploaded_template is None:
        st.error("Please upload a .pptx/.potx template or presentation.")
        st.stop()

    # Determine selected provider
    selected_provider = provider if provider != "None (local heuristic)" else None

    # Step 1: Plan slides
    with st.spinner("Analyzing text and planning slides..."):
        try:
            plan = plan_slides(
                text=input_text,
                guidance=guidance,
                provider=selected_provider,
                api_key=api_key,
                model=model or None,
                min_slides=min_slides,
                max_slides=max_slides,
                add_speaker_notes=add_speaker_notes,
            )
        except Exception as e:
            st.exception(e)
            st.stop()

    st.success(f"Planned {len(plan.get('slides', []))} slides.")

    # Step 2: Build PPTX using the uploaded template file
    with st.spinner("Applying template styles and building .pptx..."):
        try:
            template_bytes = uploaded_template.read()
            prs = Presentation(io.BytesIO(template_bytes))
            out_pptx = build_presentation_from_plan(
                plan=plan,
                template_presentation=prs,
            )
        except Exception as e:
            st.exception(e)
            st.stop()

    # Step 3: Save to bytes and offer download
    bio = io.BytesIO()
    out_pptx.save(bio)
    bio.seek(0)

    st.download_button(
        label="⬇️ Download your presentation (.pptx)",
        data=bio,
        file_name="generated_deck.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )

    # Step 4: Lightweight textual preview
    with st.expander("Preview slide outline"):
        st.json(plan)

else:
    st.info("Fill in the inputs and click **Generate Presentation**.")

# Footer note
st.caption("No images are generated with AI. The app only reuses images already present in your uploaded template.")
