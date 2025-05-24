from django.shortcuts import render 
import json
from .chatbot import chef
# Create your views here.


def chatbot(request):
    context = None

    if request.method == "POST":
        input_text = request.POST['cheif']
        chef_response = chef(input_text)
        # print(chef_response)

        try:
            # 1) Parse raw JSON (string → dict) if needed
            parsed = json.loads(chef_response) if isinstance(chef_response, str) else chef_response

            # 2) Drill into the 'content' wrapper
            data = parsed.get("content", {})

            # 3) Now grab the real values
            ingredients = data.get("ingredients")
            recipe      = data.get("recipe")
            fact        = data.get("fact")
            information = data.get("information")
            error       = data.get("error")

            context = {
                "ingredients":  ingredients,
                "recipe":       recipe,
                "fact":         fact,
                "information":  information,
                "error":        error,
            }
        
        except json.JSONDecodeError as e:
            context = { "error": f"JSON Decode Error: {e}", "raw_response": chef_response }
        except Exception as e:
            context = { "error": f"Unexpected Error: {e}", "raw_response": chef_response }

    return render(request, 'ai_app/food_BG.html', context)