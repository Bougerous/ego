import streamlit as st
from dotenv import load_dotenv
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Ego - Digital Self-Reflection",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.personality_data = {}
    st.session_state.vector_store = None


def initialize_vector_db():
    """Initialize the local vector database."""
    # Create embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create a persistent ChromaDB instance in the local directory
    vector_store = Chroma(
        collection_name="ego_personality",
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
    
    return vector_store


def main():
    """Main application function."""
    st.title("Ego: Digital Self-Reflection")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Personality Assessment", "Chat with Past Self", "Analytics"]
    )
    
    # Initialize vector database if not already done
    if not st.session_state.initialized:
        with st.spinner("Initializing local database..."):
            st.session_state.vector_store = initialize_vector_db()
            st.session_state.initialized = True
    
    # Page routing
    if page == "Home":
        home_page()
    elif page == "Personality Assessment":
        assessment_page()
    elif page == "Chat with Past Self":
        chat_page()
    elif page == "Analytics":
        analytics_page()


def home_page():
    """Home page content."""
    st.header("Welcome to Ego")
    
    st.markdown("""
    Ego is a privacy-focused application designed to capture your personality and enable 
    meaningful conversations with your past self. All your data is stored locally on your device.
    
    ## How it works:
    1. Complete personality assessments to build your digital profile
    2. Engage in regular reflections to capture your thoughts and perspectives
    3. Chat with your past self to gain insights into your personal evolution
    4. Analyze patterns and trends in your personality over time
    
    Get started by navigating to the Personality Assessment page.
    """)


def assessment_page():
    """Personality assessment page."""
    st.header("Personality Assessment")
    
    assessment_type = st.selectbox(
        "Select Assessment Type",
        ["Big Five (OCEAN)", "Myers-Briggs Type Indicator (MBTI)", "Enneagram"]
    )
    
    if assessment_type == "Big Five (OCEAN)":
        big_five_assessment()
    elif assessment_type == "Myers-Briggs Type Indicator (MBTI)":
        mbti_assessment()
    elif assessment_type == "Enneagram":
        enneagram_assessment()


def big_five_assessment():
    """Big Five personality assessment."""
    st.subheader("Big Five (OCEAN) Assessment")
    
    st.markdown("""
    The Big Five personality traits represent five broad dimensions of personality:
    - Openness to experience
    - Conscientiousness
    - Extraversion
    - Agreeableness
    - Neuroticism
    
    Rate yourself on each dimension using the sliders below.
    """)
    
    openness = st.slider("Openness to Experience", 1, 100, 50)
    conscientiousness = st.slider("Conscientiousness", 1, 100, 50)
    extraversion = st.slider("Extraversion", 1, 100, 50)
    agreeableness = st.slider("Agreeableness", 1, 100, 50)
    neuroticism = st.slider("Neuroticism", 1, 100, 50)
    
    if st.button("Save Big Five Assessment"):
        # Store in session state
        st.session_state.personality_data["big_five"] = {
            "openness": openness,
            "conscientiousness": conscientiousness,
            "extraversion": extraversion,
            "agreeableness": agreeableness,
            "neuroticism": neuroticism
        }
        
        # TODO: Store in vector database
        
        st.success("Big Five assessment saved successfully!")


def mbti_assessment():
    """MBTI assessment."""
    st.subheader("Myers-Briggs Type Indicator (MBTI) Assessment")
    
    st.markdown("""
    The MBTI identifies preferences across four dichotomies:
    - Extraversion (E) vs. Introversion (I)
    - Sensing (S) vs. Intuition (N)
    - Thinking (T) vs. Feeling (F)
    - Judging (J) vs. Perceiving (P)
    
    Select your preferences below.
    """)
    
    ei = st.radio("Energy orientation", ["Extraversion (E)", "Introversion (I)"])
    sn = st.radio("Information gathering", ["Sensing (S)", "Intuition (N)"])
    tf = st.radio("Decision making", ["Thinking (T)", "Feeling (F)"])
    jp = st.radio("Lifestyle", ["Judging (J)", "Perceiving (P)"])
    
    mbti_type = f"{ei[0]}{sn[0]}{tf[0]}{jp[0]}"
    
    st.write(f"Your MBTI type: {mbti_type}")
    
    if st.button("Save MBTI Assessment"):
        # Store in session state
        st.session_state.personality_data["mbti"] = {
            "type": mbti_type,
            "ei": ei[0],
            "sn": sn[0],
            "tf": tf[0],
            "jp": jp[0]
        }
        
        # TODO: Store in vector database
        
        st.success("MBTI assessment saved successfully!")


def enneagram_assessment():
    """Enneagram assessment."""
    st.subheader("Enneagram Assessment")
    
    st.markdown("""
    The Enneagram describes nine distinct personality types:
    1. The Reformer: Principled, purposeful, self-controlled
    2. The Helper: Generous, people-pleasing, possessive
    3. The Achiever: Adaptable, excelling, driven
    4. The Individualist: Expressive, dramatic, self-absorbed
    5. The Investigator: Perceptive, innovative, isolated
    6. The Loyalist: Engaging, responsible, anxious
    7. The Enthusiast: Spontaneous, versatile, scattered
    8. The Challenger: Self-confident, decisive, confrontational
    9. The Peacemaker: Receptive, reassuring, complacent
    
    Select your primary type and wing below.
    """)
    
    primary_type = st.selectbox("Primary Type", list(range(1, 10)))
    
    wing_options = [primary_type - 1, primary_type + 1]
    wing_options = [w for w in wing_options if 1 <= w <= 9]
    wing = st.selectbox("Wing", wing_options)
    
    instinct = st.selectbox("Dominant Instinct", [
        "Self-Preservation (sp)",
        "Social (so)",
        "One-to-One/Sexual (sx)"
    ])
    
    if st.button("Save Enneagram Assessment"):
        # Store in session state
        st.session_state.personality_data["enneagram"] = {
            "primary_type": primary_type,
            "wing": wing,
            "instinct": instinct
        }
        
        # TODO: Store in vector database
        
        st.success("Enneagram assessment saved successfully!")


def chat_page():
    """Chat with past self page."""
    st.header("Chat with Your Past Self")
    
    # Check if personality data exists
    if not st.session_state.personality_data:
        st.warning(
            "Please complete at least one personality assessment before chatting."
        )
        return
    
    st.markdown("""
    Ask a question to your past self. The application will use your stored personality data
    to generate responses that reflect how you might have responded in the past.
    """)
    
    # Chat input
    user_query = st.text_input("Your question:")
    
    if user_query and st.button("Ask"):
        with st.spinner("Generating response..."):
            # TODO: Implement actual retrieval and LLM response
            # For now, just a placeholder response
            st.write("Your past self:")
            response = (
                f"Based on your personality data, your past self might say: "
                f"I would need to think about '{user_query}' carefully before responding."
            )
            st.info(response)


def analytics_page():
    """Analytics and insights page."""
    st.header("Personality Analytics")
    
    # Check if personality data exists
    if not st.session_state.personality_data:
        st.warning(
            "Please complete at least one personality assessment to view analytics."
        )
        return
    
    st.markdown("""
    This page provides insights and visualizations based on your personality data.
    As you complete more assessments over time, you'll be able to track changes in your personality.
    """)
    
    # Display Big Five data if available
    if "big_five" in st.session_state.personality_data:
        st.subheader("Big Five (OCEAN) Profile")
        big_five = st.session_state.personality_data["big_five"]
        
        # Create a simple bar chart
        st.bar_chart({
            "Openness": big_five["openness"],
            "Conscientiousness": big_five["conscientiousness"],
            "Extraversion": big_five["extraversion"],
            "Agreeableness": big_five["agreeableness"],
            "Neuroticism": big_five["neuroticism"]
        })
    
    # Display MBTI data if available
    if "mbti" in st.session_state.personality_data:
        st.subheader("MBTI Type")
        mbti = st.session_state.personality_data["mbti"]
        st.write(f"Your type: {mbti['type']}")
        
        # Display dichotomies
        col1, col2 = st.columns(2)
        with col1:
            st.write("Energy orientation:")
            st.progress(100 if mbti["ei"] == "E" else 0)
            st.write("E" if mbti["ei"] == "E" else "I")
            
            st.write("Information gathering:")
            st.progress(100 if mbti["sn"] == "S" else 0)
            st.write("S" if mbti["sn"] == "S" else "N")
        
        with col2:
            st.write("Decision making:")
            st.progress(100 if mbti["tf"] == "T" else 0)
            st.write("T" if mbti["tf"] == "T" else "F")
            
            st.write("Lifestyle:")
            st.progress(100 if mbti["jp"] == "J" else 0)
            st.write("J" if mbti["jp"] == "J" else "P")
    
    # Display Enneagram data if available
    if "enneagram" in st.session_state.personality_data:
        st.subheader("Enneagram Profile")
        enneagram = st.session_state.personality_data["enneagram"]
        st.write(
            f"Type {enneagram['primary_type']}w{enneagram['wing']} "
            f"({enneagram['instinct']})"
        )
        
        # TODO: Add more detailed Enneagram visualization


if __name__ == "__main__":
    main()