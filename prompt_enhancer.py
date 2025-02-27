import streamlit as st
import openai
import os

# Set page configuration
st.set_page_config(page_title="Prompt Enhancer", page_icon="✨", layout="wide")

# App title and description
st.title("AI Prompt Enhancer")
st.markdown("This app helps you create better prompts for AI by taking your basic inputs and enhancing them.")

# Sidebar for API key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    model = st.selectbox("Select OpenAI Model", 
                        ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
                        index=0)
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("1. Enter your OpenAI API key")
    st.markdown("2. Fill in the role, context, and task")
    st.markdown("3. Click 'Enhance Prompt'")
    st.markdown("4. Copy the enhanced prompt") 

# Main form
with st.form("prompt_form"):
    role = st.text_area("Role", placeholder="Example: You are an experienced data scientist")
    context = st.text_area("Context", placeholder="Example: I am working on a project to analyze customer churn for a telecom company")
    task = st.text_area("Task", placeholder="Example: Create a data analysis plan to identify factors contributing to customer churn")
    
    submit_button = st.form_submit_button("Enhance Prompt")

# Function to enhance prompt using OpenAI API
def enhance_prompt(role, context, task, api_key, model):
    if not api_key:
        return "Please enter your OpenAI API key in the sidebar."
    
    client = openai.OpenAI(api_key=api_key)
    
    prompt_template = f"""
    Based on the following inputs, create an enhanced AI prompt:
    
    ROLE: {role}
    CONTEXT: {context}
    TASK: {task}
    
    Your goal is to create a comprehensive and clear prompt that includes:
    1. The role definition (expanded and clarified)
    2. Relevant context (enhanced with any necessary assumptions)
    3. Clear task instructions
    4. Specific format for the answer
    5. A requirement that the AI must clarify assumptions before responding
    
    Make the prompt detailed but concise. Format it nicely with clear sections.
    """
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert at creating effective AI prompts."},
                {"role": "user", "content": prompt_template}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Process and display results
if submit_button:
    if not role or not context or not task:
        st.error("Please fill in all fields (Role, Context, and Task).")
    else:
        with st.spinner("Enhancing your prompt..."):
            enhanced_prompt = enhance_prompt(role, context, task, api_key, model)
            
        st.success("Prompt enhanced successfully!")
        st.markdown("### Enhanced Prompt:")
        st.markdown(enhanced_prompt)
        
        # Add copy button
        st.text_area("Copy this enhanced prompt", value=enhanced_prompt, height=300)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ for AI prompt engineering")

