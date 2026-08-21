# from django.utils.decorators import method_decorator
from django.views.generic import View
from arches.app.models.models import Value, Tile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import uuid
from collections import Counter

class Analysis(View):

    def get(self, request, node_id):

        # node_id = "91eae474-c019-497a-bace-d4b7a775899a"
        tiles = Tile.objects.filter(nodegroup_id = node_id)

        value_id_strings = tiles.values_list(f'data__{node_id}', flat=True)
        value_ids = [uuid.UUID(value_id) for value_id in value_id_strings]

        values_lu = dict(Value.objects.filter(valueid__in=value_ids).values_list('valueid', 'value'))

        final_values_list = [values_lu.get(value_id, "Unknown") for value_id in value_ids]
        counter = Counter(final_values_list)

        return JsonResponse(dict(counter))
    
    