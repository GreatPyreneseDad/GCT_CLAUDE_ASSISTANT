# GCT Assistant Deployment Guide

This guide will help you deploy the GCT Assistant with backend on Render and frontend on Vercel.

## Backend Deployment (Render)

1. **Create a Render Account**
   - Sign up at [render.com](https://render.com)

2. **Create a New Web Service**
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Select the `GCT_CLAUDE_ASSISTANT` repository

3. **Configure the Service**
   - **Name**: `gct-assistant-backend`
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn gct_backend:app`

4. **Environment Variables**
   - Add the following environment variables:
     ```
     DATABASE_PATH=/opt/render/project/src/gct_data.db
     PORT=10000
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for the deployment to complete
   - Note your backend URL (e.g., `https://gct-assistant-backend.onrender.com`)

## Frontend Deployment (Vercel)

1. **Create a Vercel Account**
   - Sign up at [vercel.com](https://vercel.com)

2. **Import Project**
   - Click "New Project"
   - Import your GitHub repository
   - Select the `GCT_CLAUDE_ASSISTANT` repository

3. **Configure the Project**
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

4. **Environment Variables**
   - Add the following environment variable:
     ```
     NEXT_PUBLIC_API_URL=https://gct-assistant-backend.onrender.com
     ```
   - Replace with your actual Render backend URL

5. **Deploy**
   - Click "Deploy"
   - Wait for the deployment to complete
   - Your frontend will be available at the provided Vercel URL

## Post-Deployment Setup

1. **Test the Integration**
   - Visit your Vercel frontend URL
   - Complete a Tier 1 assessment
   - Verify that results are saved and displayed

2. **CORS Configuration**
   - The backend is configured to accept requests from any origin
   - For production, update the CORS settings in `backend/gct_backend.py` to restrict to your Vercel domain

3. **Database Persistence**
   - The SQLite database is stored locally on Render
   - For production use, consider migrating to PostgreSQL or another hosted database

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
python gct_backend.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Troubleshooting

### Backend Issues
- Check Render logs for errors
- Ensure all environment variables are set correctly
- Verify Python version compatibility

### Frontend Issues
- Check Vercel build logs
- Ensure NEXT_PUBLIC_API_URL is set correctly
- Check browser console for API connection errors

### CORS Issues
- Backend is configured to allow all origins by default
- Check that API endpoints are accessible directly
- Verify frontend is using correct API URL

## Security Considerations

For production deployment:
1. Restrict CORS to specific domains
2. Add authentication/authorization
3. Use HTTPS for all communications
4. Implement rate limiting
5. Use environment variables for sensitive data
6. Consider data encryption for personal assessments