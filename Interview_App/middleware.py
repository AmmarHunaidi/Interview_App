from django.http import JsonResponse
import traceback

class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Log the error internally
        traceback.print_exc()
        return JsonResponse({'error': 'Unhandled exception', 'details': str(exception)}, status=500)
