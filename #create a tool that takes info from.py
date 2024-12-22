#create a tool that takes info from 
# resumes and pair them to job descriptions
#using NLP adn oop to manage the parsing matching and UI layers


#using streamlit for the UI
import os
import streamlit as st

class FileManager:
    """Manages file reading for resumes and job descriptions."""
    def __init__(self, resume_path, job_desc_path):
        self.resume_path = resume_path
        self.job_desc_path = job_desc_path

    def read_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} does not exist.")
        with open(file_path, 'r') as file:
            return file.read()

    def get_resumes(self):
        return self.read_file(self.resume_path)

    def get_job_descriptions(self):
        return self.read_file(self.job_desc_path)

class TextProcessor:
    """Processes text data for comparison."""
    @staticmethod
    def to_word_set(text):
        # Split text into words, normalize case, and remove duplicates
        return set(word.lower() for word in text.split())

    @staticmethod
    def find_common_words(text1, text2):
        words1 = TextProcessor.to_word_set(text1)
        words2 = TextProcessor.to_word_set(text2)
        return words1.intersection(words2)

class Matcher:
    """Matches resumes to job descriptions based on common words."""
    def __init__(self, resume_path, job_desc_path):
        self.file_manager = FileManager(resume_path, job_desc_path)

    def match(self):
        try:
            resumes = self.file_manager.get_resumes()
            job_descriptions = self.file_manager.get_job_descriptions()
            return TextProcessor.find_common_words(resumes, job_descriptions)
        except FileNotFoundError as e:
            st.error(e)
            return set()

# Streamlit UI
st.title("Resume and Job Description Matcher")

resume_file_path = st.text_input("Enter the path to the resumes file:")
job_description_file_path = st.text_input("Enter the path to the job descriptions file:")

if st.button("Match"):
    if resume_file_path and job_description_file_path:
        matcher = Matcher(resume_file_path, job_description_file_path)
        common_words = matcher.match()
        if common_words:
            st.write("Common words:", common_words)
        else:
            st.write("No common words found or an error occurred.")
    else:
        st.error("Please provide both file paths.")