# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 14:59:55 2025

@author: Allet
"""

# Re-running the code after kernel reset
from faker import Faker
import random
import pandas as pd

# Initialize Faker and set seed for reproducibility
fake = Faker()
Faker.seed(123)
random.seed(123)

# Designations and skills
designations = [
    "Data Analyst", "Business Analyst", "Junior Data Scientist", "Senior Data Analyst",
    "Data Science Intern", "Reporting Analyst", "BI Developer", "Data Engineer",
    "ML Associate", "Insights Analyst"
]
skills = ['Python', 'Power BI', 'SQL', 'Excel', 'Tableau', 'Statistics', 'R', 'NumPy', 'Pandas']

# Sample questions
questions = [
    "Tell me about yourself.",
    "What is SQL?",
    "How do you clean data?",
    "What is your experience with Power BI?",
    "Describe a difficult situation you handled.",
    "What is a JOIN operation in SQL?",
    "Why do you want this job?"
]

# Answers bank with multiple relevant answers
answers_bank = {
    "Tell me about yourself.": [
        "My name is {name} and I hold a degree in {education}. I'm a recent graduate in data science with strong skills in Python and SQL.",
        "Hello, I'm {name}, I completed my {education}, and I love solving analytical problems through data.",
        "Hi, I'm {name}. I studied {education} and did internships where I worked on real-world data projects and dashboards."
    ],
    "What is SQL?": [
        "SQL stands for Structured Query Language and is used to manage data in relational databases.",
        "It’s a language used for querying, updating, and managing data stored in databases.",
        "SQL helps you interact with databases — for example, to retrieve customer records or sales data."
    ],
    "How do you clean data?": [
        "I handle missing values, remove duplicates, and standardize formats during data cleaning.",
        "I use Pandas in Python to identify null values, drop irrelevant columns, and correct inconsistent entries.",
        "I apply techniques like normalization, encoding categorical values, and outlier detection."
    ],
    "What is your experience with Power BI?": [
        "I’ve built interactive dashboards and used DAX to create KPIs and visualizations.",
        "I use Power BI for reporting sales trends and customer analysis with slicers and filters.",
        "I connected Power BI to Excel and SQL databases to create dynamic reports for management."
    ],
    "Describe a difficult situation you handled.": [
        "During a group project, a teammate left suddenly, and I took over their tasks to meet the deadline.",
        "Once I faced a technical glitch hours before a demo, and I quickly built a workaround using Python.",
        "I had to resolve a conflict in the team by mediating and redistributing responsibilities."
    ],
    "What is a JOIN operation in SQL?": [
        "JOIN combines rows from two or more tables based on a related column like ID.",
        "It’s used to merge data — for instance, customer details with their orders.",
        "JOIN helps bring together different tables so you can analyze related data easily."
    ],
    "Why do you want this job?": [
        "I’m passionate about data and love solving real-world problems through analysis.",
        "This role aligns perfectly with my skill set and career goals in analytics.",
        "I want to grow in the data field and believe your company offers great learning opportunities."
    ]
}

# Sentiments
sentiments = ["positive", "neutral", "negative"]

# Noise function
def introduce_manual_noise(answer, degrade=False):
    harmless_noise = [
        "umm...", "uhh...", "I guess", "you know", "like", "I think", "sort of", "kinda"
    ]
    wrong_responses = [
        "I'm not sure about that.",
        "I don't remember exactly.",
        "Sorry, I haven't learned that yet.",
        "I haven’t used that in any of my projects yet."
    ]
    if degrade:
        return random.choice(wrong_responses)
    elif random.random() < 0.4:
        return f"{random.choice(harmless_noise)} {answer}"
    else:
        return answer

# Interview simulation
interview_data = []
used_names = set()

for i in range(1000):
    emp_id = f"EID{i+1:04}"
    while True:
        name = fake.name()
        if name not in used_names:
            used_names.add(name)
            break

    designation = random.choice(designations)
    education = random.choice(["B.Sc in CS", "B.Tech", "M.Sc in Data Science", "MBA with Analytics"])
    experience_years = random.randint(0, 5)
    experience = f"{experience_years} years"
    fresher_tag = "Fresher" if experience_years == 0 else "Experienced"
    interview_date = fake.date_between(start_date='-180d', end_date='today')

    first_q = "Tell me about yourself."
    remaining_qs = [q for q in questions if q != first_q]
    sampled_qs = [first_q] + random.sample(remaining_qs, 5)

    transcript_parts, scores, skills_used = [], [], set()
    bad_answer_count = 0
    answer_flags = {}

    for q in sampled_qs:
        degrade = random.random() < 0.15
        raw_answer = random.choice(answers_bank[q]) if not degrade else ""

        if not degrade and ('{name}' in raw_answer or '{education}' in raw_answer):
            raw_answer = raw_answer.format(name=name, education=education)

        answer = introduce_manual_noise(raw_answer, degrade=degrade)
        score = random.randint(4, 5) if not degrade else random.randint(1, 3)

        if degrade or any(x in answer.lower() for x in ["i don’t know", "haven’t used", "not sure"]):
            bad_answer_count += 1
            answer_flags[q] = "not answered"
        else:
            answer_flags[q] = "answered"

        selected_skills = random.sample(skills, k=random.randint(1, 3))
        skills_used.update(selected_skills)
        scores.append(score)
        transcript_parts.append(f"Interviewer: {q}\nCandidate: {answer}\n")

    transcript = "\n".join(transcript_parts)
    overall_score = round(sum(scores) / len(scores), 2)
    skills_str = ', '.join(skills_used)

    feedback = ("Excellent candidate. Recommended." if overall_score >= 4.5 else
                "Good potential. Needs upskilling." if overall_score >= 3.5 else
                "Average. Technical areas need improvement." if overall_score >= 2.5 else
                "Not suitable currently.")

    if overall_score >= 4.2 and bad_answer_count <= 1:
        hiring_decision = "Hire"
    elif 3.5 <= overall_score < 4.2 and bad_answer_count <= 2:
        hiring_decision = "Hold for Further Review"
    else:
        hiring_decision = "Reject"


    summary_issues = []
    for skill in skills_used:
        if skill == "Power BI" and answer_flags.get("What is your experience with Power BI?") == "not answered":
            summary_issues.append("Power BI listed but not confidently answered")
        if skill == "SQL" and answer_flags.get("What is SQL?") == "not answered":
            summary_issues.append("SQL listed but not confidently answered")

    skills_summary = "; ".join(summary_issues) if summary_issues else "All mentioned skills supported."
    interview_summary = (f"Candidate {name} ({emp_id}) applied for the role of {designation} with {education} background. "
                         f"They are a {fresher_tag}. Performance in the interview was rated {overall_score}/5. "
                         f"Skills mentioned: {skills_str}. {skills_summary}")

    interview_data.append({
        "employee_id": emp_id,
        "name": name,
        "designation": designation,
        "education": education,
        "experience": experience,
        "interview_date": interview_date,
        "interview_transcript": transcript,
        "skills_mentioned": skills_str,
        "overall_score": overall_score,
        "feedback": feedback,
        "interview_summary": interview_summary,
        "hiring_decision": hiring_decision
    })

# Save to CSV
df_conversational_transcripts = pd.DataFrame(interview_data)
file_path = "conversational_interviews_with_noise4444.csv"
df_conversational_transcripts.to_csv(file_path, index=False)
file_path
