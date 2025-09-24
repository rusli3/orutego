# 🚀 Deployment Guide

This guide covers deploying orutego to various platforms for production use.

## 📋 Pre-deployment Checklist

### Security
- [ ] Change `app.secret_key` to a secure random key
- [ ] Set `debug=False` in production
- [ ] Restrict Google Maps API key with proper domains
- [ ] Enable HTTPS/SSL
- [ ] Review error handling and logging

### Configuration
- [ ] Update allowed hosts/domains
- [ ] Configure environment variables
- [ ] Set up proper logging
- [ ] Configure static file serving
- [ ] Test all features with production API key

## 🌐 Deployment Options

### 1. Heroku Deployment

#### Prerequisites
```bash
pip install gunicorn
```

#### Create Procfile
```
web: gunicorn app:app
```

#### Deploy Steps
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-orutego-app

# Set environment variables
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main
```

### 2. DigitalOcean App Platform

#### app.yaml
```yaml
name: orutego
services:
- name: web
  source_dir: /
  github:
    repo: yourusername/orutego
    branch: main
  run_command: gunicorn app:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  routes:
  - path: /
```

### 3. Railway Deployment

Simply connect your GitHub repository to Railway and it will auto-detect the Flask app.

### 4. Traditional VPS (Ubuntu/CentOS)

#### Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip nginx -y

# Install application dependencies
pip3 install -r requirements.txt
pip3 install gunicorn
```

#### Create Gunicorn Service
```bash
sudo nano /etc/systemd/system/orutego.service
```

```ini
[Unit]
Description=Orutego Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/orutego
Environment="PATH=/path/to/orutego/venv/bin"
ExecStart=/path/to/orutego/venv/bin/gunicorn --workers 3 --bind unix:orutego.sock -m 007 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Configure Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/orutego/orutego.sock;
    }

    location /static {
        alias /path/to/orutego/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 🔧 Production Configuration

### app.py Modifications
```python
import os
from flask import Flask

app = Flask(__name__)

# Production configuration
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
    app.secret_key = os.environ.get('SECRET_KEY', 'change-this-in-production')
else:
    app.config['DEBUG'] = True
    app.secret_key = 'development-key'

# Add security headers
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
```

### Environment Variables
```bash
# Required
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production

# Optional
PORT=5000
```

## 🔒 Security Hardening

### Google Maps API Key Restrictions

1. **HTTP Referrers**:
   ```
   https://yourdomain.com/*
   https://www.yourdomain.com/*
   ```

2. **API Restrictions**:
   - Geocoding API
   - Distance Matrix API
   - Directions API
   - Maps JavaScript API

### SSL/HTTPS Setup

#### Let's Encrypt (Free)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 📊 Monitoring & Logging

### Application Logging
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/orutego.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Orutego startup')
```

### Monitor Google Maps API Usage
- Set up billing alerts in Google Cloud Console
- Monitor API quotas and usage
- Set up alerts for unusual usage patterns

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python test_decimal_conversion.py
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "your-orutego-app"
        heroku_email: "your-email@example.com"
```

## 📈 Performance Optimization

### Caching Headers
```python
@app.route('/static/<path:filename>')
def static_files(filename):
    response = make_response(send_from_directory('static', filename))
    response.headers['Cache-Control'] = 'public, max-age=31536000'  # 1 year
    return response
```

### Database (if needed)
Consider adding Redis or Memcached for session storage in high-traffic scenarios.

## 🔍 Health Checks

### Health Check Endpoint
```python
from datetime import datetime
from flask import jsonify

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })
```

## 📞 Support & Maintenance

### Backup Strategy
- Regular backups of application code
- Monitor API key usage and quotas
- Keep dependencies updated
- Regular security updates

### Monitoring Checklist
- [ ] Application uptime monitoring
- [ ] API response times
- [ ] Google Maps API quota usage
- [ ] Server resource usage
- [ ] Error rate monitoring
- [ ] SSL certificate expiration