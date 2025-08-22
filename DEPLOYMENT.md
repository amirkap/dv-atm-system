# 🚀 Deployment Guide - Render

This guide will help you deploy the DV ATM System to Render.

## Prerequisites

1. **GitHub Repository**: Your code must be in a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com)

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository containing your ATM system
   - Render will automatically detect `render.yaml`

3. **Deploy**:
   - Review the configuration
   - Click "Apply"
   - Wait for deployment to complete

### Option 2: Manual Setup

1. **Create Web Service**:
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configuration**:
   ```
   Name: dv-atm-system
   Runtime: Docker
   Region: Frankfurt (optimal for Middle East/Europe)
   Branch: main
   Dockerfile Path: ./Dockerfile
   
   Build Command: (automatic - Docker handles build)
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables**:
   ```
   MAX_ACCOUNTS=1000
   MAX_TRANSACTION_AMOUNT=10000.0
   LOG_LEVEL=INFO
   ENVIRONMENT=production
   ```

4. **Health Check**:
   ```
   Health Check Path: /health
   ```

## Post-Deployment

### 1. Verify Deployment
Once deployed, you'll get a URL like: `https://dv-atm-system.onrender.com`

Test the health endpoint:
```bash
curl https://your-app-name.onrender.com/health
```

### 2. Test API Endpoints

```bash
# Set your deployment URL
export API_URL="https://your-app-name.onrender.com"

# Create account
curl -X POST "$API_URL/accounts" \
  -H "Content-Type: application/json" \
  -d '{"initial_balance": 1000.0}'

# Check balance (replace with actual account number)
curl "$API_URL/accounts/ACCOUNT_NUMBER/balance"

# Make a deposit
curl -X POST "$API_URL/accounts/ACCOUNT_NUMBER/deposit" \
  -H "Content-Type: application/json" \
  -d '{"amount": 500.0}'
```

### 3. Run Tests Against Deployed Service

```bash
# Run tests against your deployed service
python tests/test_deployment.py https://your-app-name.onrender.com
python tests/test_api.py https://your-app-name.onrender.com
```

## Production Considerations

### Performance
- **Free Tier**: Service may sleep after 15 minutes of inactivity
- **Paid Tier**: Always-on with better performance
- **Scaling**: Render handles auto-scaling

### Monitoring
- Check Render Dashboard for logs and metrics
- Use the `/health` endpoint for uptime monitoring
- Monitor memory usage (512MB limit on free tier)

### Security
- HTTPS enabled by default
- Environment variables are encrypted
- CORS configured for web access

## Troubleshooting

### Common Issues

1. **Build Failures**:
   ```bash
   # Check build logs in Render Dashboard
   # Ensure all dependencies are in requirements.txt
   ```

2. **Memory Issues**:
   ```bash
   # Free tier has 512MB RAM limit
   # Consider reducing MAX_ACCOUNTS if needed
   ```

3. **Cold Starts**:
   ```bash
   # Free tier services sleep after 15 minutes
   # First request after sleep takes ~30 seconds
   ```

### Logs
```bash
# View logs in Render Dashboard
# Or use Render CLI:
render logs --service dv-atm-system
```

## Custom Domain (Optional)

1. Go to your service settings in Render
2. Add custom domain
3. Update DNS records as instructed
4. SSL certificate will be automatically provisioned

## Cost

- **Free Tier**: 750 hours/month, sleeps after 15 min
- **Starter Plan**: $7/month, always-on
- **Standard Plan**: $25/month, more resources

## Support

For deployment issues:
- Check [Render Documentation](https://render.com/docs)
- Review build and runtime logs
- Check this project's GitHub issues
