from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from PitchingService.BaseballData.pitcher_db import Pitcher
from PitchingService.BaseballData.statcast_data import populate_pitcher_db

def get_pitcher_data_by_id(request, pitcher_id):
    pitcher = get_object_or_404(Pitcher, id=pitcher_id)

    context = {
        'pitcher': pitcher
    }
    return JsonResponse(context);

def get_pitcher_data(request):
    pitchers = list(Pitcher.objects.all().values())
    context = {
        'pitchers': pitchers
    }
    return JsonResponse(context)

def update_database(request):
    clear = Pitcher.objects.all().delete()
    try:
        populate_pitcher_db()
        pitchers = list(Pitcher.objects.all().values())
        context = {
            'pitchers': pitchers
        }
        return JsonResponse(context, status=200)
    except Exception as e:
        return JsonResponse(
            {"error": e},
            status=400
        )
