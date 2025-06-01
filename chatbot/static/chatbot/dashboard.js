
        function showTab(tabId) {
            document.querySelectorAll(".tab-content").forEach(tab => {
                tab.classList.remove("active");  // Hide all tabs
            });
            document.getElementById(tabId).classList.add("active"); // Show selected tab
        }

        function toggleTable(tableId, btn) {
            let table = document.getElementById(tableId);
            let icon = btn.querySelector(".toggle-icon");

            if (table.style.maxHeight) {
                table.style.maxHeight = null; // Close dropdown
                icon.textContent = "+"; // Change to plus
            } else {
                table.style.maxHeight = table.scrollHeight + "px"; // Open dropdown smoothly
                icon.textContent = "-"; // Change to minus
            }
        }

        function getCSRFToken() {
            return document.getElementById("csrf_token").value;
        }
        
        
        
        
        function markAsComplete(detailId) {
            fetch(`/api/mark-as-complete/${detailId}/`, {
                method: "POST",
                headers: { 
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    
                    
                let progressBar = document.getElementById("progress-bar");
            if (progressBar) {
                progressBar.style.width = data.progress + "%";  // Update width
                progressBar.textContent = Math.round(data.progress) + "%";  // Update text
                progressBar.setAttribute("aria-valuenow", data.progress);  // Update ARIA value
            }
                location.reload();
                } else {
                    alert(data.error);
                }
            })
            .catch(error => console.error("Error:", error));
        }

        function addTask() {
            let input = document.getElementById("new-task");
            let task = input.value.trim();
        
            if (task) {
                let li = document.createElement("li");
                li.innerHTML = task + ' <button onclick="removeTask(this)">❌</button>';
                document.getElementById("todo-items").appendChild(li);
                
                input.value = "";
        
                let todoListContainer = document.querySelector(".to-do-list");
                todoListContainer.scrollTop = todoListContainer.scrollHeight;
            }
        }
        
        function removeTask(button) {
            button.parentElement.remove();
        }
        
    

let time = 1500; // 25 seconds
let timer = null; 

function startTimer() {
    if (!timer) {  // Prevent multiple intervals
        timer = setInterval(updateTimer, 1000);
    }
}

function updateTimer() {
    if (time > 0) {
        time--;
        let minutes = Math.floor(time / 60);
        let seconds = time % 60;
        document.getElementById("timer").textContent = 
            `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    } else {
        clearInterval(timer);
        timer = null;
        alert("Time's up!");
    }
}

function pauseTimer() {
    clearInterval(timer);
    timer = null;
}

function resetTimer() {
    clearInterval(timer);
    timer = null;
    time = 1500;
    document.getElementById("timer").textContent = "25:00";
}
