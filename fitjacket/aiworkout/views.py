from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
from django.contrib import messages
import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env file

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


def workout_completed(request):
    if request.method == "POST":
        return render(request, "aiworkout/completed.html")
    return redirect("aiworkout")


@login_required
def aiworkout_view(request):
    workout_plan = None

    if request.method == "POST":
        user = request.user
        try:
            skill_level = user.userprofile.skill_level
            categories = user.userprofile.goals
        except AttributeError:
            skill_level = "beginner"
            categories = ["strength", "cardio"]

        categories_str = ", ".join(categories)

        prompt = (
            "Say something funny."
        )

        try:
            response = model.generate_content(prompt)
            workout_plan = response.text.replace("Exercise 1\n\n", "Exercise 1\n").strip()
        except Exception as e:
            workout_plan = "Something went wrong. Please try again."

    return render(request, "aiworkout/show.html", {
        "workout_plan": workout_plan
    })
