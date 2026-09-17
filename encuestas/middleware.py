class CapturarPeticionMiddleware:
    def __init__(self, get_response):
        # Se ejecuta una sola vez cuando el servidor se inicia
        self.get_response = get_response

    def __call__(self, request):
        # 1. Código que se ejecuta ANTES de que la vista procese la petición:
        metodo = request.method  # Captura si es GET, POST, etc.
        ruta = request.path  # Captura la URL (ej: /encuestas/)

        # Imprime la información en la consola de tu terminal
        print(f"\n[INFO] Cliente solicita: {metodo} -> {ruta}")

        # Ejecuta la vista y obtiene la respuesta
        response = self.get_response(request)

        # 2. Código que se ejecuta DESPUÉS de la vista (opcional):
        # Aquí podrías ver el estatus de la respuesta (ej: 200 OK, 404 Not Found)
        print(f"[INFO] Respuesta enviada con código: {response.status_code}")

        return response