# Railway Deployment Guide

This guide will walk you through deploying your Healthcare Translator Backend to Railway.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Groq API Key**: Get one from [console.groq.com](https://console.groq.com)

## Step 1: Prepare Your Repository

Ensure your repository contains these files:
- `main.py` - Your FastAPI application
- `requirements.txt` - Python dependencies
- `railway.json` - Railway configuration
- `Procfile` - Alternative deployment method
- `.railwayignore` - Files to exclude from deployment
- `runtime.txt` - Python version specification

## Step 2: Connect to Railway

1. **Login to Railway**: Go to [railway.app](https://railway.app) and sign in
2. **New Project**: Click "New Project"
3. **Connect Repository**: Choose "Deploy from GitHub repo"
4. **Select Repository**: Choose your healthcare translator repository
5. **Deploy**: Railway will automatically detect it's a Python project and start building

## Step 3: Configure Environment Variables

1. **Go to Variables Tab**: In your Railway project dashboard
2. **Add Required Variables**:
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   ENVIRONMENT=production
   ```

## Step 4: Deploy

1. **Automatic Deployment**: Railway will automatically deploy when you push to your main branch
2. **Manual Deployment**: You can also trigger manual deployments from the dashboard
3. **Monitor Build**: Watch the build logs for any errors

## Step 5: Access Your Application

1. **Get Domain**: Railway will provide you with a domain (e.g., `https://your-app-name.railway.app`)
2. **Test Endpoints**:
   - Health check: `https://your-app-name.railway.app/health`
   - API docs: `https://your-app-name.railway.app/docs`
   - Translation: `https://your-app-name.railway.app/translate`

## Step 6: Custom Domain (Optional)

1. **Add Custom Domain**: In Railway dashboard, go to Settings → Domains
2. **Configure DNS**: Point your domain to Railway's servers
3. **SSL Certificate**: Railway automatically provides SSL certificates

## Monitoring & Maintenance

### Health Checks
- Railway automatically monitors your `/health` endpoint
- Failed health checks trigger automatic restarts

### Logs
- View real-time logs in Railway dashboard
- Logs are automatically rotated and stored

### Scaling
- Railway automatically scales based on traffic
- You can manually adjust resources in the dashboard

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check `requirements.txt` for dependency issues
   - Verify Python version in `runtime.txt`
   - Check build logs for specific errors

2. **Runtime Errors**
   - Verify environment variables are set correctly
   - Check application logs for error details
   - Ensure `GROQ_API_KEY` is valid

3. **CORS Issues**
   - Verify CORS configuration in `main.py`
   - Check if your frontend domain is allowed

4. **Port Issues**
   - Railway automatically sets the `PORT` environment variable
   - Your app should use `os.getenv("PORT", 8000)`

### Debug Commands

```bash
# Check Railway CLI (if installed)
railway status

# View logs
railway logs

# Check environment variables
railway variables
```

## Performance Optimization

1. **Dependencies**: Keep `requirements.txt` minimal
2. **Caching**: Railway provides automatic caching
3. **Health Checks**: Keep health check endpoint lightweight
4. **Logging**: Use appropriate log levels

## Security Best Practices

1. **Environment Variables**: Never commit API keys to your repository
2. **CORS**: Restrict allowed origins to your actual domains
3. **Input Validation**: Your FastAPI app already handles this
4. **HTTPS**: Railway automatically provides SSL certificates

## Cost Management

1. **Free Tier**: Railway offers a generous free tier
2. **Usage Monitoring**: Track your usage in the dashboard
3. **Resource Limits**: Set appropriate limits for your needs

## Support

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **Community**: [discord.gg/railway](https://discord.gg/railway)
- **GitHub Issues**: For application-specific issues

## Next Steps

After successful deployment:
1. Test all API endpoints
2. Integrate with your frontend application
3. Set up monitoring and alerts
4. Configure custom domain if needed
5. Set up CI/CD for automatic deployments

Your Healthcare Translator Backend is now ready to serve users worldwide through Railway's global infrastructure!
