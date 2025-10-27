FROM nginx:alpine

# Create a beautiful landing page
RUN echo '<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Invitaciones</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .container {
            text-align: center;
            padding: 2rem;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            max-width: 600px;
            margin: 2rem;
        }
        h1 { font-size: 3rem; margin-bottom: 1rem; }
        .emoji { font-size: 4rem; margin-bottom: 1rem; }
        p { font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9; }
        .btn {
            display: inline-block;
            padding: 1rem 2rem;
            margin: 0.5rem;
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            border: 2px solid rgba(255,255,255,0.3);
            transition: all 0.3s ease;
            font-weight: 600;
        }
        .btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .status {
            background: rgba(0,255,0,0.2);
            padding: 0.5rem 1rem;
            border-radius: 25px;
            margin: 1rem 0;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">🎉</div>
        <h1>Sistema de Invitaciones</h1>
        <div class="status">✅ Funcionando Correctamente</div>
        <p>Tu aplicación está desplegada y funcionando en AWS EC2</p>
        <a href="/docs" class="btn">📚 Ver API Docs</a>
        <a href="/health" class="btn">❤️ Health Check</a>
        <p style="margin-top: 2rem; font-size: 1rem; opacity: 0.7;">
            Servidor: AWS EC2 • IP: 3.140.201.39 • Puerto: 80
        </p>
    </div>
</body>
</html>' > /usr/share/nginx/html/index.html

# Configure nginx to proxy API calls
RUN echo 'server {
    listen 80;
    server_name localhost;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /docs {
        proxy_pass http://backend:8000/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /health {
        proxy_pass http://backend:8000/health;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
