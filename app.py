from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime
import os
import requests
from utils.automation_engine import automation_recommendation
from utils.router import detect_intent
from utils.task_manager import create_task
from utils.team import analyze_team
from utils.pdf_reader import extract_text
from utils.mission_planner import generate_plan
from utils.risk_engine import predict_risk
# ---------------------------------------------------
# INITIAL SETUP
# ---------------------------------------------------

load_dotenv()

app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------------------------------------------
# DEMO STORAGE
# ---------------------------------------------------

tasks = []
productivity_score = 85
# ---------------------------------------------------
# AUTOMATION CLASSIFIER
# ---------------------------------------------------

def classify_automation(message):

    text = message.lower()

    if any(x in text for x in [
        "meeting",
        "schedule",
        "calendar",
        "appointment"
    ]):
        return "calendar"

    if any(x in text for x in [
        "email",
        "mail",
        "reply"
    ]):
        return "email"

    if any(x in text for x in [
        "task",
        "todo",
        "follow up",
        "reminder"
    ]):
        return "task"

    return "none"

# ---------------------------------------------------
# N8N AUTOMATION
# ---------------------------------------------------

def create_n8n_task(task_text):

    try:
        response = requests.post(
    "http://localhost:5678/webhook/chronos-task",
    json={
        "task": task_text,
        "source": "CHRONOS-X",
        "timestamp": datetime.now().isoformat(),
        "requested_by": "Elaine"
    },
    timeout=10
)

        return response.json()

    except Exception as e:

        return {
            "task": task_text,
            "priority": "Medium",
            "owner": "Team",
            "risk": "Low",
            "status": f"Automation Failed: {str(e)}"
        }


# ---------------------------------------------------
# HOME ROUTES
# ---------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------------------------------------------------
# CHAT
# ---------------------------------------------------
# ---------------------------------------------------
# CHAT
# ---------------------------------------------------


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    user_message = data.get("message", "")

    intent = detect_intent(user_message)

    # MISSION PLANNER
    if (
        "build" in user_message.lower()
        or "develop" in user_message.lower()
        or "create" in user_message.lower()
    ):

        plan = generate_plan(user_message)

        response = f"""
🚀 MISSION DETECTED

Goal:
{user_message}

EXECUTION PLAN

Day 1 : {plan['Day 1']}
Day 2 : {plan['Day 2']}
Day 3 : {plan['Day 3']}
Day 4 : {plan['Day 4']}
Day 5 : {plan['Day 5']}
Day 6 : {plan['Day 6']}
Day 7 : {plan['Day 7']}

Status:
READY FOR EXECUTION
"""

        return jsonify({
            "response": response
        })

    print("USER:", user_message)
    print("INTENT:", intent)

    auto = automation_recommendation(user_message)

    # Continue with the rest of your code here...

    # -----------------------------------------
    # AUTOMATION DETECTION
    # -----------------------------------------

    automation_type = classify_automation(user_message)

    needs_automation = automation_type != "none"

    # -----------------------------------------
    # AUTOMATION MODE
    # -----------------------------------------

    if needs_automation:

        result = create_n8n_task(user_message)

        task = create_task(user_message)

        tasks.append({
            "title": task["title"],
            "priority": task["priority"],
            "status": task["status"],
            "created": str(datetime.now())
        })

        response = f"""
🚀 CHRONOS AUTOMATION EXECUTED

Task: {result.get('task', task['title'])}

Automation Type: {automation_type.upper()}

Priority: {result.get('priority', task['priority'])}

Owner: {result.get('owner', 'Team')}

Risk: {result.get('risk', 'Low')}

Status: {result.get('status', 'Created')}

NEXT ACTION:
Automation workflow dispatched successfully.
"""

    # -----------------------------------------
    # TEAM ANALYSIS
    # -----------------------------------------

    elif intent == "team":

        team_data = analyze_team()

        response = f"""
👥 TEAM STATUS

Elaine : {team_data['Elaine']}%
Member2 : {team_data['Member2']}%
Member3 : {team_data['Member3']}%

RECOMMENDATION:
Assign new work to the least busy member.
"""

    # -----------------------------------------
    # NORMAL AI MODE
    # -----------------------------------------

    else:

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are CHRONOS X.

You are NOT a chatbot.

You are an autonomous AI Chief of Staff.

Primary objective:

Maximize team productivity and ensure successful project execution.

You must:

1. Detect objectives.
2. Break objectives into tasks.
3. Assign priorities.
4. Predict risks.
5. Recommend automation opportunities.
6. Suggest delegation.
7. Create schedules.
8. Trigger workflows whenever possible.

Always respond in this format:

MISSION:
CURRENT STATUS:
TASKS:
PRIORITY:
RISKS:
AUTOMATIONS:
NEXT ACTION:

Never answer casually.
Never engage in small talk.
Act like JARVIS + COO.
"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        response = completion.choices[0].message.content

    response += f"""

⚙️ AUTOMATION ENGINE

{auto['automation']}
"""

    return jsonify({
        "response": response
    })


# ---------------------------------------------------
# ADD TASK
# ---------------------------------------------------

@app.route("/add-task", methods=["POST"])
def add_task_route():

    data = request.get_json()

    task = {
        "title": data["title"],
        "priority": data.get("priority", "Medium"),
        "status": "Pending",
        "created": str(datetime.now())
    }

    tasks.append(task)

    return jsonify({
        "message": "Task Added Successfully",
        "task": task
    })
    


# ---------------------------------------------------
# GET TASKS
# ---------------------------------------------------

@app.route("/tasks")
def get_tasks():

    return jsonify(tasks)


# ---------------------------------------------------
# PRODUCTIVITY STATS
# ---------------------------------------------------

@app.route("/stats")
def stats():

    completed = len([
        t for t in tasks
        if t["status"] == "Completed"
    ])

    pending = len([
        t for t in tasks
        if t["status"] == "Pending"
    ])

    score = productivity_score

    if len(tasks) > 0:
        score = int(((completed + 1) / len(tasks)) * 100)

    return jsonify({
        "productivity_score": score,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "total_tasks": len(tasks)
    })


# ---------------------------------------------------
# TEAM STATUS
# ---------------------------------------------------

@app.route("/team-status")
def team_status():

    return jsonify(
        analyze_team()
    )


# ---------------------------------------------------
# RISK ANALYSIS
# ---------------------------------------------------

@app.route("/risk-analysis", methods=["POST"])
def risk_analysis():

    data = request.get_json()

    hours_needed = int(data["hours_needed"])
    hours_available = int(data["hours_available"])

    if hours_available >= hours_needed:
        risk = "LOW"

    elif hours_available >= hours_needed * 0.7:
        risk = "MEDIUM"

    else:
        risk = "HIGH"

    return jsonify({
        "risk": risk,
        "hours_needed": hours_needed,
        "hours_available": hours_available
    })


# ---------------------------------------------------
# PDF ANALYSIS
# ---------------------------------------------------

@app.route("/analyze-pdf", methods=["POST"])
def analyze_pdf():

    try:

        if "file" not in request.files:
            return jsonify({
                "analysis": "No PDF uploaded."
            })

        file = request.files["file"]

        if file.filename == "":
            return jsonify({
                "analysis": "No file selected."
            })

        os.makedirs("uploads", exist_ok=True)

        save_path = os.path.join(
            "uploads",
            file.filename
        )

        file.save(save_path)

        pdf_text = extract_text(save_path)

        if pdf_text.strip() == "":
            pdf_text = "No readable text found."

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are CHRONOS X.

Analyze this mission brief.

Return:

1. Executive Summary
2. Key Tasks
3. Deadlines
4. Risks
5. Automation Opportunities
6. Action Plan
"""
                },
                {
                    "role": "user",
                    "content": pdf_text[:12000]
                }
            ]
        )

        result = completion.choices[0].message.content

        return jsonify({
            "analysis": result
        })

    except Exception as e:

        print("PDF ROUTE ERROR:", e)

        return jsonify({
            "analysis": f"Error: {str(e)}"
        })

# ---------------------------------------------------
# RUN
# ---------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)