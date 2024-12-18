import streamlit as st
import google.generativeai as genai
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class AdvancedHealthPlanner:
    def __init__(self):
        self.setup_page_config()
        self.load_custom_css()
        self.init_session_state()

    def setup_page_config(self):
        st.set_page_config(
            page_title="Advanced Health Companion",
            page_icon="🌟",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    def load_custom_css(self):
        st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .chart-container {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header-style {
            color: #1f2937;
            padding: 10px 0;
            border-bottom: 2px solid #e5e7eb;
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

    def init_session_state(self):
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = {
                'measurements': [],
                'weight_log': [],
                'fitness_progress': {},
                'nutrition_log': [],
                'health_risk_factors': {}
            }


    def show_about_section(self):
        st.markdown("<h2 class='header-style'>ℹ️ About</h2>", unsafe_allow_html=True)
        
        # App Information
        with st.container():
            st.markdown("""
            <div class='metric-card'>
                <h3>🌟 About the App</h3>
                <p>The AI powered Health & Fitness Companion is a comprehensive health management platform that combines artificial intelligence with personalized health tracking. Our platform offers:</p>
                <ul>
                    <li>Personalized fitness and nutrition planning</li>
                    <li>Advanced body measurement tracking</li>
                    <li>AI-powered health risk assessments</li>
                    <li>Detailed nutritional analysis and meal planning</li>
                </ul>
                <p>Version: 1.0.0</p>
                <p>Last Updated: December 2024</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Developer Information
        with st.container():
            st.markdown("""
            <div class='metric-card'>
                <h3>👨‍💻 About the Developer</h3>
                <p><strong>Elizabeth O. Edwards</strong></p>
                <p>Digital Technology Solutions Consultant</p>
                <br>
                <p>Connect with me:</p>
                <ul>
                    <li>📧 Email: hello@inspiriasoft.com</li>
                    <li>🔗 LinkedIn: linkedin.com/in/elizabetholorunleke</li>
                    <li>🐱 GitHub: github.com/qween-beth</li>
                    <li>🌐 Portfolio: inspiriasoft.com</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # Technologies Used
        with st.container():
            st.markdown("""
            <div class='metric-card'>
                <h3>🛠️ Technologies Used</h3>
                <ul>
                    <li>🐍 Python</li>
                    <li>📊 Streamlit</li>
                    <li>🤖 Google Gemini AI</li>
                    <li>📈 Plotly</li>
                    <li>🐼 Pandas</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # Feedback Section
        with st.container():
            st.markdown("""
            <div class='metric-card'>
                <h3>📝 Feedback</h3>
                <p>We value your input! If you have any suggestions, feature requests, or bug reports, please reach out through any of the contact methods above.</p>
            </div>
            """, unsafe_allow_html=True)


    def track_body_measurements(self):
        st.markdown("<h2 class='header-style'>📏 Body Measurement Tracker</h2>", unsafe_allow_html=True)
        
        with st.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                chest = st.number_input("Chest (inches)", min_value=20.0, max_value=60.0, step=0.1)
            with col2:
                waist = st.number_input("Waist (inches)", min_value=20.0, max_value=60.0, step=0.1)
            with col3:
                hip = st.number_input("Hips (inches)", min_value=20.0, max_value=60.0, step=0.1)

            if st.button("Log Measurements", key='log_measurements'):
                measurement_entry = {
                    'date': datetime.now(),
                    'chest': chest,
                    'waist': waist,
                    'hip': hip
                }
                
                # Initialize measurements list if it doesn't exist
                if 'measurements' not in st.session_state.user_profile:
                    st.session_state.user_profile['measurements'] = []
                
                st.session_state.user_profile['measurements'].append(measurement_entry)
                st.success("✅ Measurements logged successfully!")
                
                # Debug information
                st.write("Debug Info:")
                st.write(f"Number of measurements logged: {len(st.session_state.user_profile['measurements'])}")
                st.write("Latest measurement:", measurement_entry)

            # Show current data
            if st.session_state.user_profile.get('measurements'):
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                
                # Convert measurements to DataFrame
                df = pd.DataFrame(st.session_state.user_profile['measurements'])
                df['date'] = pd.to_datetime(df['date'])
                
                # Debug information for DataFrame
                st.write("DataFrame Head:")
                st.write(df)
                
                # Create and display the chart
                fig = px.line(df, x='date', y=['chest', 'waist', 'hip'],
                            title='Body Measurement Progression',
                            labels={'value': 'Inches', 'date': 'Date'},
                            template='plotly_white')
                
                fig.update_layout(
                    legend_title_text='Measurement',
                    hovermode='x unified',
                    height=500  # Explicitly set height
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Add clear measurements button
                if st.button("Clear All Measurements"):
                    st.session_state.user_profile['measurements'] = []
                    st.success("All measurements cleared!")
                    st.experimental_rerun()
            else:
                st.info("No measurements logged yet. Add your first measurement above!")

    def health_risk_assessment(self, model):
        st.markdown("<h2 class='header-style'>🩺 Health Risk Assessment</h2>", unsafe_allow_html=True)
        
        with st.container():
            risk_questions = {
                "Sleep": "How many hours of sleep do you get per night?",
                "Nutrition": "How many servings of fruits and vegetables do you eat daily?",
                "Exercise": "How many times per week do you exercise?",
                "Stress": "How would you rate your stress levels? (0=Low, 10=High)",
                "Water": "How many glasses of water do you drink daily?"
            }

            risk_answers = {}
            col1, col2 = st.columns(2)
            
            for i, (category, question) in enumerate(risk_questions.items()):
                with col1 if i % 2 == 0 else col2:
                    risk_answers[category] = st.slider(question, 0, 10, 5)

            if st.button("Analyze Health Risks", key='analyze_risks'):
                with st.spinner("Analyzing your health profile..."):
                    risk_prompt = f"""
                    Perform a comprehensive health risk assessment based on these metrics:
                    {risk_answers}

                    Please provide:
                    1. Overall health risk score (Low, Moderate, High)
                    2. Breakdown of specific risk areas
                    3. Actionable recommendations for improvement
                    4. Priority areas to focus on
                    """
                    
                    try:
                        response = model.generate_content(risk_prompt)
                        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                        st.markdown("### 📊 Your Health Risk Analysis")
                        st.write(response.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ Risk assessment error: {str(e)}")

    def nutrition_deep_dive(self, model):
        st.markdown("<h2 class='header-style'>🥗 Nutritional Deep Dive</h2>", unsafe_allow_html=True)
        
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                dietary_goals = st.multiselect(
                    "Select Your Nutritional Goals",
                    options=[
                        "Weight Loss",
                        "Muscle Gain",
                        "Heart Health",
                        "Diabetes Management",
                        "Improved Energy",
                        "Better Sleep",
                        "Digestive Health"
                    ]
                )

            with col2:
                allergens = st.multiselect(
                    "Select Any Dietary Restrictions",
                    options=[
                        "Gluten",
                        "Dairy",
                        "Nuts",
                        "Soy",
                        "Shellfish",
                        "Eggs",
                        "Fish"
                    ]
                )

            meal_preference = st.selectbox(
                "Preferred Meal Complexity",
                options=["Simple (15 min prep)", "Moderate (30 min prep)", "Complex (45+ min prep)"]
            )

            if st.button("Generate Nutrition Plan", key='generate_nutrition'):
                with st.spinner("Creating your personalized nutrition plan..."):
                    nutrition_prompt = f"""
                    Create a detailed nutritional plan for someone with:
                    Goals: {dietary_goals}
                    Restrictions: {allergens}
                    Meal Complexity: {meal_preference}

                    Please provide:
                    1. Daily macronutrient targets
                    2. Key micronutrients to focus on
                    3. Three {meal_preference.split()[0].lower()} meal recipes
                    4. Specific supplement recommendations if needed
                    5. Meal timing recommendations
                    """

                    try:
                        response = model.generate_content(nutrition_prompt)
                        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                        st.markdown("### 🍽️ Your Personalized Nutrition Plan")
                        st.write(response.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ Nutrition analysis error: {str(e)}")

    def main(self):
        st.title("🌟 Advanced Health Companion")
        
        with st.sidebar:
            st.header("🔑 Configuration")
            gemini_api_key = st.text_input(
                "Enter Gemini API Key",
                type="password",
                help="Get your API key from Google AI Studio"
            )

            if not gemini_api_key:
                st.info("💡 Please enter your Gemini API key to access all features.")
                st.markdown("[Get API Key](https://aistudio.google.com/apikey)")
                return

        try:
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel('gemini-pro')

            feature = st.sidebar.selectbox(
                "Choose Feature",
                [
                    "Body Measurement Tracking",
                    "Health Risk Assessment",
                    "Nutritional Deep Dive",
                    "About"  # New option
                ]
            )

            if feature == "Body Measurement Tracking":
                self.track_body_measurements()
            elif feature == "Health Risk Assessment":
                self.health_risk_assessment(model)
            elif feature == "Nutritional Deep Dive":
                self.nutrition_deep_dive(model)
            elif feature == "About":
                self.show_about_section()

        except Exception as e:
            st.error(f"❌ System Error: {str(e)}")
            st.info("Please check your API key and try again.")


def run():
    planner = AdvancedHealthPlanner()
    planner.main()

if __name__ == "__main__":
    run()