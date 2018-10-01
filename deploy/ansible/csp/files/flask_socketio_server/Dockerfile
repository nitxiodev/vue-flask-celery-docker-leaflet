FROM python:2

RUN mkdir -p app/csp_solver_cloud
COPY ./csp_solver_cloud /app/csp_solver_cloud
RUN pip install -r /app/csp_solver_cloud/requirements.txt
RUN pip install gunicorn
RUN pip install gevent-websocket
ENV PYTHONPATH "${PYTHONPATH}:/app"
# /gunicorn  --chdir csp_solver_cloud/src/server/ flask_socketio_server:socketio_app -w 1 -b 127.0.0.1:8000 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker --preload --worker-connections 1024
CMD ["gunicorn", "--chdir", "/app/csp_solver_cloud/src/server/", "flask_socketio_server:socketio_app", "-w", "1", "-b", "0.0.0.0:8000", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "--preload", "--worker-connections", "1024"]
EXPOSE 8000
