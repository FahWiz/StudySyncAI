
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute("content");
}
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("generatePlanBtn").addEventListener("click", generateStudyPlan);
});

let subjects = [];

function addSubject() {
    let subjectDiv = document.createElement("div");
    subjectDiv.classList.add("subject");

    let subjectInput = document.createElement("input");
    subjectInput.type = "text";
    subjectInput.placeholder = "Enter subject name";
    subjectInput.classList.add("subject-input");

    let topicContainer = document.createElement("div");
    topicContainer.classList.add("topic-container");

    let addTopicBtn = document.createElement("button");
    addTopicBtn.textContent = "+ Add Topic";
    addTopicBtn.type = "button";
    addTopicBtn.onclick = function () {
        addTopic(topicContainer);
    };

    subjectDiv.appendChild(subjectInput);
    subjectDiv.appendChild(topicContainer);
    subjectDiv.appendChild(addTopicBtn);

    document.getElementById("subjectsContainer").appendChild(subjectDiv);
}

function addTopic(container) {
    let topicDiv = document.createElement("div");

    let topicInput = document.createElement("input");
    topicInput.type = "text";
    topicInput.placeholder = "Enter topic name";
    topicInput.classList.add("topic-input");

    let difficultySelect = document.createElement("select");
    difficultySelect.classList.add("difficulty-select");
    ["Easy", "Medium", "Hard"].forEach(level => {
        let option = document.createElement("option");
        option.value = level;
        option.textContent = level;
        difficultySelect.appendChild(option);
    });

    topicDiv.appendChild(topicInput);
    topicDiv.appendChild(difficultySelect);
    container.appendChild(topicDiv);
}

function generateStudyPlan(event) {
    event.preventDefault();

    let studyHoursPerDay = parseInt(document.getElementById("study_hours").value);
    let preferredTime = document.getElementById("study_time").value;
    let deadline = parseInt(document.getElementById("no_of_days").value);

    let subjectDivs = document.querySelectorAll(".subject");
    subjects = [];

    subjectDivs.forEach(subjectDiv => {
        let subjectName = subjectDiv.querySelector(".subject-input").value;
        let topics = [];

        subjectDiv.querySelectorAll(".topic-container > div").forEach(topicDiv => {
            let topicName = topicDiv.querySelector(".topic-input").value;
            let difficulty = topicDiv.querySelector(".difficulty-select").value;
            topics.push({ name: topicName, difficulty });
        });

        if (subjectName.trim() !== "" && topics.length > 0) {
            subjects.push({ name: subjectName, topics });
        }
    });

    if (subjects.length === 0 || isNaN(studyHoursPerDay) || isNaN(deadline) || deadline < 1) {
        alert("Please enter study hours, deadline, and at least one subject with topics.");
        return;
    }

    let allTopics = [];
    subjects.forEach(subject => {
        subject.topics.forEach(topic => {
            allTopics.push({
                subject: subject.name,
                topic: topic.name,
                difficulty: topic.difficulty
            });
        });
    });

    allTopics.sort((a, b) => {
        let difficultyWeight = { Easy: 1, Medium: 2, Hard: 3 };
        return difficultyWeight[b.difficulty] - difficultyWeight[a.difficulty];
    });

    let scheduleTable = document.getElementById("studySchedule");
    scheduleTable.innerHTML = `
        <thead>
            <tr>
                <th>Date</th>
                <th>Subject</th>
                <th>Topic</th>
                <th>Time</th>
                <th>Duration</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    `;

    let tbody = scheduleTable.querySelector("tbody");
    let currentTime = new Date();
    let remainingDays = deadline;
    let totalTopics = allTopics.length;
    let topicsPerDay = Math.ceil(totalTopics / deadline);

    let generatedPlan = [];

    while (remainingDays > 0 && allTopics.length > 0) {
        let dailyHours = studyHoursPerDay;
        let topicsForToday = allTopics.splice(0, topicsPerDay);

        topicsForToday.forEach(topicData => {
            let topicTime = topicData.difficulty === "Hard" ? 3 : topicData.difficulty === "Medium" ? 2 : 1;
            if (topicTime > dailyHours) topicTime = dailyHours;

            let planEntry = {
                date: currentTime.toDateString(),
                subject: topicData.subject,
                topic: topicData.topic,
                time: preferredTime,
                duration: topicTime
            };

            generatedPlan.push(planEntry);

            let row = tbody.insertRow();
            row.innerHTML = `
                <td>${planEntry.date}</td>
                <td>${planEntry.subject}</td>
                <td>${planEntry.topic}</td>
                <td>${planEntry.time}</td>
                <td>${planEntry.duration} hrs</td>
            `;

            dailyHours -= topicTime;
        });

        currentTime.setDate(currentTime.getDate() + 1);
        remainingDays--;
    }

    while (remainingDays > 0) {
        let planEntry = {
            date: currentTime.toDateString(),
            subject: "Revision",
            topic: "Review previous topics",
            time: preferredTime,
            duration: remainingDays <= 2 ? 2 : 1
        };

        generatedPlan.push(planEntry);

        let row = tbody.insertRow();
        row.innerHTML = `
            <td>${planEntry.date}</td>
            <td>${planEntry.subject}</td>
            <td>${planEntry.topic}</td>
            <td>${planEntry.time}</td>
            <td>${planEntry.duration} hrs</td>
        `;

        currentTime.setDate(currentTime.getDate() + 1);
        remainingDays--;
    }
    
    

    saveStudyPlan(generatedPlan);
}

function saveStudyPlan(studyPlanData) {
    let title = document.getElementById("name").value.trim();
    if(title==="") title="Untitled Plan11";
    fetch("/api/save-study-plan/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ title: title, study_plan: studyPlanData }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.study_plan_id) {
            alert("Study plan saved successfully!");
        } else {
            alert("Error saving study plan!");
        }
    })
    .catch(error => console.error("Error:", error));
}

