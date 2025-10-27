FROM nginx:alpine

# Copy static files
COPY index.html /usr/share/nginx/html/index.html
COPY confirmation.html /usr/share/nginx/html/confirmation.html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
