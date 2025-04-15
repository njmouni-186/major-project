document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('preferences-form');
    const courseRecommendationDiv = document.getElementById('course-recommendation');
    const feedbackButton = document.querySelector('#feedback button');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Get user inputs
        const cgpa = parseFloat(document.getElementById('cgpa').value);
        const credits = parseInt(document.getElementById('credits').value);
        const teacherRating = parseInt(document.getElementById('teacher-rating').value);
        const teacherFriendliness = parseInt(document.getElementById('teacher-friendliness').value);
        const courseDifficulty = parseInt(document.getElementById('course-difficulty').value);
        const teacherSkills = parseInt(document.getElementById('teacher-skills').value);

        // Send data to the server
        fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                cgpa: cgpa,
                credits: credits,
                teacher_rating: teacherRating,
                teacher_friendliness: teacherFriendliness,
                course_difficulty: courseDifficulty,
                teacher_skills: teacherSkills
            })
        })
        .then(response => response.json())
        .then(data => {
            // Display recommended course
            courseRecommendationDiv.innerHTML = `
                <h3>Recommended Course</h3>
                <p>Course Code: ${data.course_code}</p>
                <p>Course Title: ${data.course_title}</p>
                <p>Credits: ${data.credits}</p>
                <p>Recommended Professor: ${data.professor}</p>
                <p>Our model estimates that you should be able to do the said course easily!</p>
            `;
        })
        .catch(error => console.error('Error:', error));
    });

    feedbackButton.addEventListener('click', function() {
        const feedbackRating = parseInt(document.getElementById('feedback-rating').value);
        alert(`Thank you for your feedback! You rated the recommendation system: ${feedbackRating}/10`);
    });
});