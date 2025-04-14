import requests
from django.shortcuts import render

def exercise_list(request):
    url = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"
    response = requests.get(url)
    all_exercises = response.json()

    # Get search & checkbox filter query params
    query = request.GET.get('search', '').lower()
    categories = request.GET.getlist('category')  # list
    levels = request.GET.getlist('level')          # list

    filtered = []

    for ex in all_exercises:
        name_match = query in ex['name'].lower() if query else True
        cat_match = ex.get('category', '').lower() in categories if categories else True
        level_match = ex.get('level', '').lower() in levels if levels else True

        if name_match and cat_match and level_match:
            if ex.get("images"):
                ex["image_url"] = f"https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/{ex['images'][0]}"
            else:
                ex["image_url"] = None
            filtered.append(ex)

    exercises = filtered[:100]

    # Predefined filter options
    categories_list = ['strength', 'cardio', 'stretching', 'plyometrics', 'powerlifting', 'strongman']
    levels_list = ['beginner', 'intermediate', 'expert']

    return render(request, 'exercises/index.html', {
        'exercises': exercises,
        'categories_list': categories_list,
        'levels_list': levels_list,
        'selected_categories': categories,  # 👈 used in template
        'selected_levels': levels,          # 👈 used in template
        'search_query': request.GET.get('search', '')  # 👈 for search bar value
    })


def exercise_detail(request, exercise_id):
    url = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"
    response = requests.get(url)
    exercises = response.json()

    # Find the specific exercise by id
    exercise = next((ex for ex in exercises if ex['id'] == exercise_id), None)

    if exercise:
        # Add full image URLs
        exercise["image_urls"] = [
            f"https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/{img}"
            for img in exercise.get("images", [])
        ]
    else:
        return render(request, '404.html', status=404)

    return render(request, 'exercises/show.html', {'exercise': exercise})
