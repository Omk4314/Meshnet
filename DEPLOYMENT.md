# Deployment Guide for Excel Row Processor

## 🚀 Quick Deployment Steps

### Option 1: Streamlit Cloud (Recommended - FREE)

1. **Create GitHub Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/excel-processor.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub account
   - Select your repository: `excel-processor`
   - Main file path: `app.py`
   - Click "Deploy!"

3. **Your app will be live at:**
   `https://excel-processor-YOUR_USERNAME.streamlit.app`

### Option 2: Railway (FREE Tier Available)

1. **Push to GitHub** (same as above)

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Connect GitHub
   - Select your repository
   - Railway will automatically detect the `railway.json` config
   - Click "Deploy"

3. **Your app will be live at:**
   `https://excel-processor-production.up.railway.app`

### Option 3: Render (FREE Tier Available)

1. **Push to GitHub** (same as above)

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect GitHub
   - Select your repository
   - Render will use the `render.yaml` config
   - Click "Create Web Service"

3. **Your app will be live at:**
   `https://excel-processor.onrender.com`

### Option 4: Heroku (PAID - No Free Tier)

1. **Push to GitHub** (same as above)

2. **Deploy on Heroku:**
   - Go to [heroku.com](https://heroku.com)
   - Create new app
   - Connect GitHub
   - Select your repository
   - Heroku will use the `Procfile`
   - Click "Deploy"

## 📋 Pre-Deployment Checklist

- [ ] All files are committed to GitHub
- [ ] `requirements.txt` includes all dependencies
- [ ] App works locally (`streamlit run app.py`)
- [ ] No hardcoded local paths in code
- [ ] Environment variables are properly configured

## 🔧 Configuration Files Created

- `railway.json` - Railway deployment config
- `Procfile` - Heroku deployment config  
- `render.yaml` - Render deployment config
- `runtime.txt` - Python version specification

## 🌐 After Deployment

1. **Share the URL** with others
2. **Test the app** from different devices
3. **Monitor usage** through the platform dashboard
4. **Update the README** with your live URL

## 💡 Tips

- **Streamlit Cloud** is the easiest and most reliable free option
- **Railway** offers more customization options
- **Render** has good free tier limits
- **Heroku** requires payment but is very stable

## 🆘 Troubleshooting

### Common Issues:

1. **App won't start:**
   - Check `requirements.txt` has all dependencies
   - Verify Python version compatibility

2. **File upload not working:**
   - Check file size limits
   - Verify file format support

3. **Download issues:**
   - Test with different browsers
   - Check popup blockers

### Getting Help:

- Check platform-specific documentation
- Look at deployment logs
- Test locally first
- Use platform support channels
