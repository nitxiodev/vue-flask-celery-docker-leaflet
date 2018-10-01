# build stage
FROM node:8.11.3-alpine as build-stage
WORKDIR /app
#COPY ./csp_solver_cloud-frontend/package*.json ./
#RUN npm install
COPY ./csp_solver_cloud-frontend .
#RUN npm run build

FROM nginx:1.15.2-alpine
COPY --from=build-stage /app/dist /usr/share/nginx/html
RUN chown -R nginx /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]