from flask import Flask, render_template, request, jsonify

import pandas as pd
import numpy as np
import sklearn.metrics.pairwise as cos_similarity
import random

app = Flask(__name__)

# Load the dataset
df = pd.read_csv("student_preferences.csv")
course_list = pd.read_csv("courses_list.csv")
courses = pd.read_csv("courses.csv")

# Normalize the rating for teacher rating, teacher teaching skills and course difficulty 
df['Teacher Rating'] = (df['TR'] - df['TR'].mean())/df['TR'].std()
df['Teacher Friendliness'] = (df['TF'] - df['TF'].mean())/df['TF'].std()
df['Course Difficulty'] = (df['CD'] - df['CD'].mean())/df['CD'].std()
df['Teacher Teaching Skills'] = (df['TTS'] - df['TTS'].mean())/df['TTS'].std()
df['CGPA'] = (df['CG'] - df['CG'].mean())/df['CG'].std()
df['RecRating'] = (df['RCR'] - df['RCR'].mean())/df['RCR'].std()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    student_cgpa = data['cgpa']
    course_creds = data['credits']
    teacher_rating = data['teacher_rating']
    teacher_friendliness = data['teacher_friendliness']
    course_difficulty = data['course_difficulty']
    teacher_teaching_skills = data['teacher_skills']

    student_preferences = [teacher_rating, teacher_friendliness, course_difficulty, teacher_teaching_skills, course_creds, student_cgpa]

    # Define a function that returns the cosine similarity between two arrays
    def cosine_similarity(arr1, arr2):
        x = np.asarray(arr1, dtype='float64')
        y = np.asarray(arr2, dtype='float64')
        dot_product = np.dot(x, y)
        norm = float(np.linalg.norm(x)) * float(np.linalg.norm(y))
        similarity = dot_product / norm
        return similarity

    # Compute the similarity between courses using cosine similarity
    similarities = []
    weighted_similarities = []
    for i in range(len(df)):
        a = [df.iat[i, 0], df.iat[i, 1], df.iat[i, 2], df.iat[i, 3], df.iat[i, 4], df.iat[i, 5]]
        similarity = cosine_similarity(a, student_preferences)
        similarities.append(similarity)
        weighted_similarities.append(similarity * df['RCR'][i])

    df['Cosine Similarities'] = similarities
    df['Weighted Cosine Similarities'] = weighted_similarities
    df_sorted = df.sort_values(by=['Weighted Cosine Similarities'], ascending=False)

    recommended_course_id = df_sorted["SNO"].iloc[0]
    recommended_course = courses[courses["Serial No."] == recommended_course_id]
    prediction = recommended_course["Course ID"].values[0]
    recommended_course_details = course_list[course_list["Course Code"] == prediction].iloc[0]

    response = {
        'course_code': str(recommended_course_details["Course Code"]),
        'course_title': str(recommended_course_details["Course Title"]),
        'credits': int(recommended_course_details["Credits"]),
        'professor': str(recommended_course["Teacher Name"].values[0])
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)