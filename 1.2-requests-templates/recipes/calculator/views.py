from django.shortcuts import render
from django.http import HttpResponse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}

def start(request, recipe):

    recipe = DATA.get(recipe)
    servings = int(request.GET.get('servings', 1))
    # recipe.update((k, v * servings) for k, v in recipe.items()) # обновляет значения словаря, пока запущен сервер
    recipe_total = {k: v * servings for k, v in recipe.items()}
    template = 'calculator/index.html'
    context = {
      'recipe': recipe_total, 'servings': servings
    }
    return render(request, template, context)

def index(request):
    msg = 'Добавьте в адресную строку название рецепта!'
    return HttpResponse(msg)