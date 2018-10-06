# vue-flask-celery-docker-leaflet
Dockerized client-server application of Constraint Satisfaction Problems using Flask, Websockets, Celery, Vue and Leaflet.

# Stack
- **Vagrant & Ansible** for cloud deployment (on a VirtualBox machine).
- **Flask** to build the REST API (with GEvent to allow async requests).
  - **Gunicorn** to serve REST API with GEvent workers.
- **Celery** to delegate the execution of heavy tasks, with redis backend.
  - **MapTaskQueue** will route csp solver for map tasks. They are expected to be long-running tasks due to reverse geocoding.
  - **SudokuTaskQueue** will route csp solver for sudoku tasks. They are expected to be short-running tasks.
- **Flask-SocketIO** to notify the client ASAP of the solution with no polling (with GEvent to allow async requests).
  - **Gunicorn** to serve Websockets with GEventWebsocket workers respectively.
- **Vue** to build the frontend (with Vue-Router, Vuex, Vue-socketio, axios, vue2leaflet, etc).
- **Docker** to deploy each service on the private cloud.
- **Traeffik** as load balancer of dockerized services.

# Architecture

<p align="center">
  <img src="./img/csp_cloud.svg" width="70%">
</p>

The image shows the proposed architecture. The architecture expose several public endopoints:
- `flaskserver.docker` &rarr; This is the main entry point to the REST API.
- `frontend.docker` &rarr; This is the main entry point to the Frontend Web.
- `flasksocketio.docker` &rarr; This is the main entry point to the websocket subsystem.
- `192.168.33.20:8080` &rarr; This is the entry point to the Traeffik Dashboard, where you can see which services have been deployed.

Besides these endpoints, there are other private endpoints that are not accessible from outside the docker's internal network, like redis or celery.

# Installation
Before installing it, it is required to have installed vagrant and ansible:
- `Vagrant >= 2.0.1`
- `Ansible >= 2.6.2`

Once installed, clone this repository and go to the deploy directory and type the following command on a terminal:
```bash
/deploy$ vagrant up
```
Wait a few minutes and that's it! You'll have the whole application deployed and ready to use!

# Configuration and Usage
Endpoints exposed by traeffik require a domain name, so the IP address of the machine will not be valid. To do this, edit the `/etc/hosts` file and add the following line:
```bash
192.168.33.20 flaskserver.docker frontend.docker flasksocketio.docker
```

# Notes
In order to support map tasks, this application uses the following external services:
- In the backend side, a reverse geocoding system with Photon (limited service) and/or ArcGIS (full service) is used. In the first case, its terms of use indicate that *"You can use the API for your project, but please **be fair** - extensive usage will be throttled. We do not guarantee for the availability and usage might be subject of change in the future."*, whereas in the second one, *"(...) If you merely view the results of these operations on a map and discard them immediately afterward, you can use these operations free of charge. However, if you store the results, in a database for instance, these operations require a subscription"*. 
- On the other hand, in the frontend side, a free geolocation service is used (ip-api).

**Therefore, please respect their conditions and terms of use.**


### Work in progress....
