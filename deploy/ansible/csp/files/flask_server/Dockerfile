FROM python:2

RUN mkdir -p app/csp_solver_cloud
COPY ./csp_solver_cloud /app/csp_solver_cloud
RUN pip install -r /app/csp_solver_cloud/requirements.txt
RUN pip install gunicorn
ENV PYTHONPATH "${PYTHONPATH}:/app"
# gunicorn  --chdir csp_solver_cloud/src/server/ flask_server:app -w 4 -b 127.0.0.1:8888 -k gevent --preload --worker-connections 1024
CMD ["gunicorn", "--chdir", "/app/csp_solver_cloud/src/server/", "flask_server:app", "-w", "4", "-b", "0.0.0.0:8888", "-k", "gevent", "--preload", "--worker-connections", "1024"]
EXPOSE 8888
