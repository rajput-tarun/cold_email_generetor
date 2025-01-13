import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### YOUR PROFILE:
            You are Tarun Kumar, an M.Tech graduate in Data Science from IIT Guwahati. 
            You have a strong academic background and hands-on experience in data analysis, deep learning, machine learning, and artificial intelligence. 
            Your projects reflect expertise in predictive modeling, computer science, problem solving, 
            data visualization, and leveraging LLMs for NLP tasks. 
    
            ### INSTRUCTION:
            Write a professional cold email to the HR team of a company expressing interest in relevant job opportunities. 
            Highlight your technical skills, academic achievements, and practical experiences that make you an ideal candidate for their team.
            Make sure to communicate your passion for solving complex problems using data-driven approaches and how you can contribute value to their organization. 
            
            Include the most relevant CV link(s) from the following: {link_list} to showcase your profile effectively. 
            Personalize the email to reflect the recipient's industry or company domain (e.g., technology, consulting, finance).
            
            Remember, you are Tarun Kumar. Do not include unnecessary preambles.
            
            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))