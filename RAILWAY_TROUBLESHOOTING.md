# Railway Deployment Troubleshooting Guide

This guide addresses common Railway deployment issues, especially healthcheck failures.

## 🚨 Healthcheck Failure Issues

### Problem: "Deployment failed during network process" with healthcheck failure

**Symptoms:**
- Build succeeds ✅
- Deploy succeeds ✅
- Healthcheck fails ❌ (Network > Healthcheck step fails)

**Common Causes:**
1. **Environment Variables Missing**: `GROQ_API_KEY` not set
2. **Port Binding Issues**: App not binding to `$PORT` correctly
3. **Startup Time**: App takes too long to start
4. **Dependency Issues**: Missing or incompatible packages

## 🔧 Solutions

### 1. Check Environment Variables

In Railway dashboard, ensure these are set:
```
GROQ_API_KEY=your_actual_groq_api_key_here
ENVIRONMENT=production
```

**Note**: Never commit API keys to your repository!

### 2. Verify Port Configuration

Your app must use the `PORT` environment variable:
```python
port = int(os.getenv("PORT", 8000))
```

### 3. Test Health Endpoint Locally

Before deploying, test locally:
```bash
# Start your app
python start_railway.py

# Test health endpoint
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}
```

### 4. Check Railway Logs

In Railway dashboard:
1. Go to your project
2. Click on the failed deployment
3. Check the "Logs" tab for error messages

### 5. Common Error Messages & Fixes

#### "ModuleNotFoundError: No module named 'langchain'"
**Fix**: Update `requirements.txt` with correct package names:
```
langchain>=0.1.0
langchain-groq>=0.0.1
```

#### "Address already in use"
**Fix**: Ensure your app uses `$PORT` environment variable, not hardcoded port.

#### "GROQ_API_KEY not configured"
**Fix**: Set `GROQ_API_KEY` in Railway environment variables.

#### "Connection refused" in healthcheck
**Fix**: Ensure your app binds to `0.0.0.0`, not `127.0.0.1`.

## 🚀 Deployment Checklist

Before deploying to Railway:

- [ ] All dependencies in `requirements.txt`
- [ ] `GROQ_API_KEY` set in Railway (not in code)
- [ ] App uses `os.getenv("PORT", 8000)`
- [ ] App binds to `0.0.0.0` (not `127.0.0.1`)
- [ ] Health endpoint `/health` returns quickly
- [ ] Tested locally with `python start_railway.py`

## 🔍 Debug Commands

### Check Railway Status
```bash
railway status
```

### View Logs
```bash
railway logs
```

### Check Environment Variables
```bash
railway variables
```

### Test Locally
```bash
# Test startup script
python start_railway.py

# Test health endpoint
curl http://localhost:8000/health
```

## 📊 Healthcheck Configuration

Current Railway configuration:
```json
{
  "healthcheckPath": "/health",
  "healthcheckTimeout": 600
}
```

This gives your app 10 minutes to start up and respond to health checks.

## 🆘 Still Having Issues?

1. **Check Railway Status**: [status.railway.app](https://status.railway.app)
2. **Community Support**: [discord.gg/railway](https://discord.gg/railway)
3. **Documentation**: [docs.railway.app](https://docs.railway.app)

## 🎯 Quick Fixes

### If healthcheck times out:
1. Increase `healthcheckTimeout` in `railway.json`
2. Ensure health endpoint responds quickly
3. Check if app is binding to correct port

### If build fails:
1. Check `requirements.txt` for syntax errors
2. Verify Python version in `runtime.txt`
3. Check build logs for specific errors

### If deploy fails:
1. Verify startup command in `Procfile`
2. Check if all required files are present
3. Ensure no hardcoded paths or ports

## 🚀 Redeploy After Fixes

After making changes:
1. Commit and push to GitHub
2. Railway will automatically redeploy
3. Monitor the new deployment logs
4. Check if healthcheck passes

Your app should now deploy successfully! 🎉
