# 🚀 Deployment Guide

This guide covers deploying the Agentic AI Focus Group Workflow to various platforms.

## 🎯 Quick Deployment (Replit - Recommended)

### Prerequisites
- OpenAI API key with GPT-4 access
- Replit account

### Steps
1. **Import Repository**
   - Go to [replit.com](https://replit.com)
   - Click "Create Repl" → "Import from GitHub"
   - Paste your repository URL
   - Click "Import"

2. **Configure Environment**
   - Click "Secrets" tab (🔒 icon)
   - Add required secrets:
     ```
     OPENAI_API_KEY = your_openai_api_key_here
     FLASK_SECRET_KEY = any_random_string_here
     ```

3. **Deploy**
   - Click "Run" button
   - Replit auto-installs dependencies
   - Your app will be live at the generated URL

4. **Verify**
   - Test the web interface
   - Check `/health` endpoint
   - Try generating personas

**✅ Done! Your workflow is live in ~5 minutes.**

---

## 🐳 Docker Deployment

### Prerequisites
- Docker installed
- OpenAI API key

### Steps

1. **Build Image**
   ```bash
   docker build -t agentic-focus-group .
   ```

2. **Run Container**
   ```bash
   docker run -d \
     --name agentic-workflow \
     -p 5000:5000 \
     -e OPENAI_API_KEY=your_key_here \
     -e FLASK_SECRET_KEY=your_secret_here \
     -v ./data:/app/cache \
     agentic-focus-group
   ```

3. **Using Docker Compose (Recommended)**
   ```bash
   # Create .env file first
   cp .env.example .env
   # Edit .env with your API key
   
   # Start services
   docker-compose up -d
   ```

4. **Verify**
   ```bash
   curl http://localhost:5000/health
   ```

---

## ☁️ Cloud Deployment

### AWS (EC2 + Application Load Balancer)

1. **Launch EC2 Instance**
   ```bash
   # Amazon Linux 2
   sudo yum update -y
   sudo yum install -y python3 python3-pip git
   ```

2. **Setup Application**
   ```bash
   git clone <your-repo>
   cd agentic-focus-group-workflow
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run with Gunicorn**
   ```bash
   gunicorn -c deployment/gunicorn_config.py web_interface:app
   ```

5. **Setup as Service**
   ```bash
   sudo cp deployment/agentic-workflow.service /etc/systemd/system/
   sudo systemctl enable agentic-workflow
   sudo systemctl start agentic-workflow
   ```

### Google Cloud Platform (Cloud Run)

1. **Build and Push**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/agentic-workflow
   ```

2. **Deploy**
   ```bash
   gcloud run deploy agentic-workflow \
     --image gcr.io/YOUR_PROJECT/agentic-workflow \
     --platform managed \
     --region us-central1 \
     --set-env-vars OPENAI_API_KEY=your_key \
     --memory 2Gi \
     --timeout 900
   ```

### Azure (Container Instances)

1. **Create Resource Group**
   ```bash
   az group create --name agentic-workflow --location eastus
   ```

2. **Deploy Container**
   ```bash
   az container create \
     --resource-group agentic-workflow \
     --name agentic-workflow \
     --image your-registry/agentic-workflow \
     --environment-variables OPENAI_API_KEY=your_key \
     --ports 5000 \
     --memory 2 \
     --cpu 1
   ```

---

## 🖥️ Local Development

### Prerequisites
- Python 3.8+
- OpenAI API key

### Setup
```bash
# Clone repository
git clone <your-repo>
cd agentic-focus-group-workflow

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Or manual setup:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API key

# Run application
python main.py
```

### Development Mode
```bash
# Enable debug mode
export FLASK_DEBUG=True

# Run with auto-reload
python main.py
```

---

## 🔧 Production Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ | - | OpenAI API key |
| `OPENAI_MODEL` | ❌ | gpt-4 | OpenAI model to use |
| `FLASK_SECRET_KEY` | ❌ | auto-generated | Flask secret key |
| `FLASK_DEBUG` | ❌ | False | Debug mode |
| `FLASK_PORT` | ❌ | 5000 | Server port |
| `TINYTROUPE_CACHE_DIR` | ❌ | ./cache | TinyTroupe cache directory |
| `MAX_PERSONAS` | ❌ | 8 | Maximum personas per session |

### Security Considerations

1. **API Key Security**
   - Never commit API keys to version control
   - Use environment variables or secrets management
   - Rotate keys regularly

2. **Input Validation**
   - All user inputs are validated and sanitized
   - Rate limiting recommended for production
   - Consider adding authentication for sensitive deployments

3. **Resource Limits**
   - Monitor memory usage during AI operations
   - Set appropriate timeouts for long-running operations
   - Consider implementing request queuing for high load

### Performance Optimization

1. **Caching**
   - TinyTroupe caches conversation states
   - Consider Redis for session management at scale
   - Implement response caching for repeated queries

2. **Scaling**
   - Use Gunicorn with multiple workers
   - Consider load balancing for high traffic
   - Monitor resource usage and scale accordingly

3. **Monitoring**
   ```bash
   # Health check endpoint
   curl http://your-domain/health
   
   # System diagnostics
   python monitoring/health_check.py
   ```

---

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# Automated health check
python monitoring/health_check.py

# API health check
curl http://localhost:5000/health
```

### Log Management
```bash
# View application logs
tail -f app_$(date +%Y%m%d).log

# View access logs (if using Gunicorn)
tail -f access.log
```

### Backup Strategy
```bash
# Backup session data
tar -czf backup_$(date +%Y%m%d).tar.gz exports/ cache/ logs/

# Automated backup script
0 2 * * * /path/to/backup_script.sh
```

---

## 🚨 Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   ```
   Error: Invalid API key
   Solution: Check OPENAI_API_KEY in environment variables
   ```

2. **Memory Issues**
   ```
   Error: Out of memory during discussion
   Solution: Reduce num_personas or increase server memory
   ```

3. **Import Errors**
   ```
   Error: Module 'tinytroupe' not found
   Solution: pip install -r requirements.txt
   ```

4. **Permission Errors**
   ```
   Error: Cannot write to cache directory
   Solution: chmod 755 cache/ or check directory permissions
   ```

### Debug Mode
```bash
# Enable verbose logging
export FLASK_DEBUG=True

# Run with detailed output
python main.py --verbose
```

### Performance Issues
```bash
# Check system resources
python monitoring/health_check.py

# Monitor during operation
htop  # or top on systems without htop
```

---

## 📈 Scaling Considerations

### Single Server Scaling
- Use Gunicorn with multiple workers
- Implement request queuing
- Add Redis for session management

### Multi-Server Scaling
- Load balancer (nginx, HAProxy)
- Shared storage for session data
- Database for persistent session management

### Cloud Auto-Scaling
- Configure auto-scaling groups
- Set up health check endpoints
- Implement graceful shutdown handling

---

## 🔐 Security Hardening

### Production Security Checklist
- [ ] API keys stored securely (not in code)
- [ ] HTTPS enabled with valid certificates
- [ ] Input validation and sanitization enabled
- [ ] Rate limiting configured
- [ ] Access logging enabled
- [ ] Error messages don't expose sensitive info
- [ ] Dependencies regularly updated
- [ ] Security headers configured

### Network Security
```nginx
# Example nginx configuration
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📞 Support

For deployment issues:
1. Check logs: `tail -f app_*.log`
2. Run health check: `python monitoring/health_check.py`
3. Verify configuration: `python scripts/deploy_replit.py`
4. Check API connectivity: `curl http://localhost:5000/health`

For questions and support, refer to the main README.md or create an issue in the repository.