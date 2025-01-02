import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="AI Learning Path Generator",
    page_icon="🎓",
    layout="wide"
)

# Title and description
st.title("🎓 AI Learning Path Generator")
st.markdown("""
Generate your personalized AI learning curriculum based on your preferences and goals.
""")

# Sidebar for user inputs
with st.sidebar:
    st.header("Your Learning Preferences")
    
    # 1. Persona selection
    persona = st.selectbox(
        "What's your role?",
        options=["Developer", "Manager", "Leader"],
        help="Select the role that best describes your position"
    )
    
    # 2. Learning duration
    duration = st.slider(
        "How much time can you dedicate? (in hours)",
        min_value=1,
        max_value=10,
        value=2,
        help="Select the number of hours you can dedicate to learning"
    )
    
    # 3. Specific interests
    interests = st.text_area(
        "What specific topics are you interested in?",
        placeholder="E.g., Machine Learning, Neural Networks, AI Strategy...",
        help="Enter specific topics you'd like to learn about"
    )

# Load and filter video data
@st.cache_data
def load_video_data():
    return pd.read_csv("data/video_metadata.csv")

def filter_videos(df, persona, max_duration, interests):
    # Convert persona to lowercase for matching
    persona = persona.lower()
    
    # Filter by persona
    filtered_df = df[df['target_persona'].str.lower().str.contains(persona)]
    
    # Filter by cumulative duration
    filtered_df['cumulative_duration'] = filtered_df['duration_minutes'].cumsum()
    filtered_df = filtered_df[filtered_df['cumulative_duration'] <= (max_duration * 60)]
    
    # Filter by interests if provided
    if interests:
        interests_list = [interest.strip().lower() for interest in interests.split(',')]
        interest_mask = filtered_df['topics'].str.lower().apply(
            lambda x: any(interest in x for interest in interests_list)
        )
        filtered_df = filtered_df[interest_mask]
    
    return filtered_df

# Main content
if st.sidebar.button("Generate Learning Path"):
    try:
        df = load_video_data()
        filtered_videos = filter_videos(df, persona, duration, interests)
        
        if len(filtered_videos) == 0:
            st.warning("No videos found matching your criteria. Try adjusting your preferences.")
        else:
            st.success(f"Found {len(filtered_videos)} videos for your learning path!")
            
            # Display video recommendations
            for idx, row in filtered_videos.iterrows():
                with st.expander(f"📺 {row['title']} ({row['duration_minutes']} minutes)"):
                    st.write(f"**Topics:** {row['topics']}")
                    st.write(f"**Difficulty:** {row['difficulty_level'].title()}")
                    st.write(f"**Video Link:** [{row['title']}]({row['url']})")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
