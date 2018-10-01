FROM python:2

RUN mkdir -p app/csp_solver_cloud
COPY ./csp_solver_cloud /app/csp_solver_cloud
WORKDIR /app
RUN pip install -r ./csp_solver_cloud/requirements.txt
