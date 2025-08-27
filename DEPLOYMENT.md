 # Deployment Guide

This guide covers different options for deploying your Personal Blog Platform API.

## Option 1: Deploy to Render (Recommended - Free)

Render offers free hosting for web services with some limitations.

### Steps:

1. **Prepare your repository:**
   - Push your code to GitHub
   - Make sure all files are committed

2. **Create Render account:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

3. **Create new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Choose the repository with your blog platform

4. **Configure the service:**
   ```
   Name: personal-blog-platform
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   ```

5. **Set environment variables:**
   Go to "Environment" tab and add:
   ```
   SECRET_KEY=your-production-secret-key
   JWT_SECRET_KEY=your-production-jwt-secret
   DATABASE_URL=sqlite:///blog.db
   ```

6. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your API will be available at `https://your-service-name.onrender.com`

### Render Configuration File (Optional)

Create `render.yaml` in your repository root:

```yaml
services:
  - type: web
    name: personal-blog-platform
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY  
        generateValue: true
      - key: DATABASE_URL
        value: sqlite:///blog.db
```

## Option 2: Deploy to Railway

Railway provides easy deployment with a generous free tier.

### Steps:

1. **Create Railway account:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub:**
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect it's a Python app

3. **Set environment variables:**
   - Go to your project dashboard
   - Click "Variables" tab
   - Add:
     ```
     SECRET_KEY=your-production-secret-key
     JWT_SECRET_KEY=your-production-jwt-secret
     DATABASE_URL=sqlite:///blog.db
     PORT=5000
     ```

4. **Deploy:**
   - Railway will automatically deploy
   - Your API will be available at the provided URL

## Option 3: Deploy to Replit

Great for testing and development.

### Steps:

1. **Import from GitHub:**
   - Go to [replit.com](https://replit.com)
   - Click "Create Repl" → "Import from GitHub"
   - Enter your repository URL

2. **Configure:**
   - Replit will auto-detect the Python environment
   - Install dependencies: `pip install -r requirements.txt`

3. **Set environment variables:**
   - Create `.env` file in Replit
   - Add your environment variables

4. **Run:**
   - Click the "Run" button
   - Your API will be available at the Replit URL

## Option 4: Deploy to Heroku

Heroku requires a credit card but offers good free tier.

### Steps:

1. **Install Heroku CLI:**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku

   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku app:**
   ```bash
   heroku login
   heroku create your-blog-platform
   ```

3. **Add Procfile:**
   Create `Procfile` in your repository root:
   ```