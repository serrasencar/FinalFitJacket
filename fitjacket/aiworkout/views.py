from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
from django.contrib import messages

genai.configure(api_key="AIzaSyCDKXnmEsoD-4rfV6rvGDdcToG_uOiASZY")
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
            f"Create a personalized workout for the day for a user with {skill_level} experience. "
            f"Their preferred workout categories are: {categories_str}. "
            "Start with a 2-3 sentence intro about scientific muscle groups targeted and the skill level and categories this workout supports. "
            "Use motivating language and mention that it is personalized for the user. FitJacket hopes they enjoy it. "
            "Include at least 5 exercises with: name, sets, reps, rest time, and whether equipment is needed. "
            "Format clearly without asterisks, markdown, or bolding. Avoid extra spacing after exercise numbers. "
            "Make it a little scientific. Follow the format below:\n\n"

            "Example:\n"
            "This workout focuses on building foundational strength and improving your explosive power. "
            "It targets major muscle groups like your legs, glutes, and core, perfect for beginners interested in stretching and plyometrics. "
            "FitJacket hopes you enjoy this personalized workout designed just for you!\n\n"

            "Exercise 1: Standing Quad Stretch\n"
            "Sets: 3\n"
            "Reps: 15 seconds hold per leg\n"
            "Rest: 30 seconds\n"
            "Equipment: None\n\n"

            "Exercise 2: Jumping Jacks\n"
            "Sets: 3\n"
            "Reps: 20\n"
            "Rest: 60 seconds\n"
            "Equipment: None\n\n"

            "Exercise 3: Hamstring Stretch (lying down)\n"
            "Sets: 3\n"
            "Reps: 15 seconds hold per leg\n"
            "Rest: 30 seconds\n"
            "Equipment: None\n\n"

            "Exercise 4: Butt Kicks\n"
            "Sets: 3\n"
            "Reps: 20\n"
            "Rest: 60 seconds\n"
            "Equipment: None\n\n"

            "Exercise 5: Squat Jumps\n"
            "Sets: 3\n"
            "Reps: 10\n"
            "Rest: 90 seconds\n"
            "Equipment: None\n\n"

            "End with a short motivational message like: Remember to listen to your body and take breaks when needed. You've got this!"
            
            "Include a few scientific labels for muscles."
        )

        try:
            response = model.generate_content(prompt)
            workout_plan = response.text.replace("Exercise 1\n\n", "Exercise 1\n").strip()
        except Exception as e:
            workout_plan = "Something went wrong. Please try again."

    return render(request, "aiworkout/show.html", {
        "workout_plan": workout_plan
    })
