# from django.utils.decorators import method_decorator
from django.views.generic import View
from arches.app.models.models import Value, Tile
from django.http import JsonResponse
import uuid
import pandas as pd
import json

class Analysis(View):

    def get(self, request):

        node_id = "91eae474-c019-497a-bace-d4b7a775899a"
        tiles = Tile.objects.filter(nodegroup_id = node_id)

        value_id_strings = tiles.values_list(f'data__{node_id}', flat=True)
        value_ids = [uuid.UUID(value_id) for value_id in value_id_strings]

        values = dict(Value.objects.filter(valueid__in=value_ids).values_list('valueid', 'value'))

        final_values_list = [values.get(value_id, "Unknown") for value_id in value_ids]

        # frequency

        series = pd.Series(final_values_list)
        frequency_table = series.value_counts()

        series_json = frequency_table.to_dict()
        return JsonResponse(series_json)
    
    