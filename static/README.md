# Repo Intel - Frontend

This is the frontend implementation for the Repo Intel project, a GitHub repository analysis tool.

## Project Structure

```
frontend/
├── index.html          # Main login/signup page
├── dashboard.html      # Post-login dashboard
├── css/
│   ├── styles.css      # Login/signup page styles
│   └── dashboard.css   # Dashboard styles
├── js/
│   ├── auth.js         # Authentication logic
│   └── dashboard.js    # Dashboard functionality
├── images/            # Images and assets
└── README.md          # This file
```

## Features

### Current Implementation
- **Login/Signup Forms**: Clean, responsive forms with validation
- **Real-time Validation**: Form validation with error messages
- **Session Management**: User session handling with sessionStorage
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, professional interface

### Form Validation
- **Login**: Username and password validation
- **Signup**: Username (max 50 chars), email (max 100 chars), password (min 6 chars), password confirmation
- **Real-time feedback**: Immediate validation feedback as users type

## Getting Started

### 1. Test the Current Setup
Open `index.html` in your browser to test the forms.

**Demo Credentials for Testing:**
- Username: `demo`
- Password: `password`

### 2. Development Setup
1. Use VS Code with Live Server extension for development
2. Right-click on `index.html` → "Open with Live Server"
3. The page will open at `http://localhost:5500/index.html`

### 3. File Structure
- Edit `index.html` for form structure changes
- Edit `css/styles.css` for styling changes
- Edit `js/auth.js` for authentication logic
- Edit `dashboard.html` for post-login interface

## Integration with Backend

### Current State
The frontend currently uses **simulated API calls** for testing. The `simulateApiCall()` function in `auth.js` mimics backend responses.

### Backend Integration Steps

1. **Replace Simulated API Calls**
   In `js/auth.js`, replace `simulateApiCall()` with `apiCall()` method:
   ```javascript
   // Change this:
   const response = await this.simulateApiCall('/auth/login', 'POST', data);
   
   // To this:
   const response = await this.apiCall('/auth/login', 'POST', data);
   ```

2. **Update API Base URL**
   ```javascript
   // In auth.js constructor:
   this.apiBaseUrl = 'http://localhost:5000/api';  // Your backend URL
   ```

3. **Expected Backend API Endpoints**
   Based on your `UserManager` class and recent backend updates, you need these endpoints:
   
   - `POST /api/auth/login`
     ```json
     // Request
     {
       "username": "string",
       "password": "string"
     }
     
     // Response
     {
       "success": true,
       "user": {
         "id": 1,
         "username": "demo",
         "email": "demo@example.com"
       }
     }
     ```
   
   - `POST /api/auth/signup`
     ```json
     // Request
     {
       "username": "string",
       "email": "string", 
       "password": "string"
     }
     
     // Response
     {
       "success": true,
       "message": "Account created successfully"
     }
     ```
   
   - `GET /api/user/bookmarks` (New: For dashboard bookmarks)
     ```json
     // Response
     {
       "success": true,
       "bookmarks": [
         {
           "id": 1,
           "repo_url": "https://github.com/user/repo",
           "repo_name": "user/repo",
           "created_at": "2025-07-16T10:00:00Z"
         }
       ]
     }
     ```
   
   - `POST /api/user/bookmarks` (New: Add bookmark)
     ```json
     // Request
     {
       "repo_url": "https://github.com/user/repo",
       "repo_name": "user/repo"
     }
     
     // Response
     {
       "success": true,
       "message": "Bookmark added"
     }
     ```
   
   - `GET /api/user/search-history` (New: For dashboard activity)
     ```json
     // Response
     {
       "success": true,
       "history": [
         {
           "id": 1,
           "repo_url": "https://github.com/user/repo",
           "analysis_type": "summary",
           "created_at": "2025-07-16T10:00:00Z"
         }
       ]
     }
     ```
   
   - `POST /api/repo/analyze` (Enhanced: Now saves to user history)
     ```json
     // Request
     {
       "repo_url": "https://github.com/user/repo",
       "analysis_type": "summary" // or "file_scan"
     }
     
     // Response
     {
       "success": true,
       "analysis": {
         "repo_name": "user/repo",
         "type": "summary",
         "content": "Analysis results...",
         "cached": true
       }
     }
     ```

## Team Coordination

### Communication with Backend Team
✅ **Recent Backend Updates (Great news!):**
- User system is now implemented through CLI
- Bookmarks functionality is working for logged-in users
- Search history is being saved (summary and file scan)
- Cache system improved with updated_at tag for freshness

### Next Steps for Backend Team:
Ask your backend teammate to create these API endpoints:

1. **Authentication endpoints** that call `UserManager.authenticate_user()` and `UserManager.create_user()`
2. **Bookmarks endpoints** for dashboard bookmark management
3. **Search history endpoint** for dashboard activity display
4. **Repository analysis endpoint** that integrates with existing CLI functionality
5. **Session management** for user authentication

### Dashboard Integration Opportunities:
Now that the backend has user functionality, your dashboard can show:
- **Real bookmarks** from the user's saved repositories
- **Actual search history** from summary and file scan activities
- **Repository analysis** with improved caching

### Testing Your Changes
1. **Test forms locally** using the demo credentials
2. **Validate all form fields** work correctly
3. **Test responsive design** on different screen sizes
4. **Create screenshots** to share with your team

### Git Workflow
```bash
# Work on your feature branch
git checkout feature/login-signup-ui

# Make your changes
git add .
git commit -m "Add login/signup frontend interface"

# Push to your branch
git push origin feature/login-signup-ui

# Create pull request for team review
```

## Customization

### Styling Changes
- Colors: Edit CSS custom properties in `styles.css`
- Layout: Modify the grid and flexbox layouts
- Animations: Add/modify CSS animations and transitions

### Form Validation
- Add new validation rules in `validateLoginForm()` and `validateSignupForm()`
- Customize error messages
- Add additional field validation

### Features to Add Later
- Password strength indicator
- "Remember me" functionality
- Password recovery
- Email verification
- Social login options

## Browser Compatibility
- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile browsers: Responsive design included

## Notes for Development
1. **Form validation** follows the `UserManager` database constraints
2. **Session management** uses sessionStorage (temporary) - consider localStorage for persistence
3. **Error handling** includes both field-level and form-level validation
4. **Responsive design** works on screens from 320px to 1200px+

## Next Steps
1. **Test thoroughly** with different inputs
2. **Share screenshots** with your team
3. **Coordinate with backend** for API integration - **PRIORITY: Backend has user system ready!**
4. **Plan dashboard features** for post-login functionality - **bookmarks and history are now possible!**
5. **Integrate repository analysis** - connect with existing CLI functionality

## Questions for Your Team
1. What's the backend API URL structure?
2. Are there any specific design requirements?
3. **NEW: Can you expose the bookmark and search history data through API endpoints?**
4. **NEW: How should the repository analysis integrate with the existing CLI functionality?**
5. How should user sessions be managed long-term?
