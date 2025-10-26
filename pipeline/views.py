import joblib
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Node
from .serializers import NodeSerializer
from .tasks import run_node


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):
        node = self.get_object()
        # run_node.delay(node.id) # async execution
        # return Response({"message": f"Node {node.name} is scheduled to run."}, status=status.HTTP_200_OK)

        from .tasks import run_node as run_node_sync
        run_node_sync(node.id) # sync execution
        return Response({"message": f"Node {node.name} has run."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def predict(request):
    """
    expects JSON payload: {'input_data': [[...], [...], ...]}
    returns predictions using trained model
    """
    input_data = request.data.get('input_data')
    if input_data is None:
        return Response({"error": "Please provide input_data"}, status=400)

    model_path = 'models/model.pkl'
    try:
        model = joblib.load(model_path) # load latest trained model
        predictions = model.predict(input_data)
        return Response({"predictions": predictions.tolist()})
    except FileNotFoundError:
        return Response({"error": "Model not found. Train a model first."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)