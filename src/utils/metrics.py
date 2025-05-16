from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
import time

from routes.auth_routes import router 

REQUEST_COUNTER=Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY=Histogram('http_request_duration_seconds', 'HTTP Request Latency', ['method', 'endpoint'])

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, next_call):
        start=time.time()

        response=await next_call(request)

        duration=time.time()-start
        endpoint=request.url.path

        REQUEST_COUNTER(method=request.method, endpoint=endpoint, status=response.status_code).inc()
        REQUEST_LATENCY(method=request.method, endpoint=endpoint).observe(duration)

        return response

    def setup_metrics(app: FastAPI):
        app.add_middleware(PrometheusMiddleware)

        @app.get("/metrics", include_in_schema=False)
        async def metrics():
            return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)