# Web UI Quick Reference Guide

## Application Flow Diagram

```
┌─────────────────┐
│   http://localhost:8000   │
│   ↓
├─────────────────┤
│ Not Authenticated    │
├─────────────────┤
│  Home Page (/)       │
│  ├─ Login Link       │
│  └─ About Info       │
│                      │
│  Login Page (/login) │
│  ├─ Username Field   │
│  ├─ Password Field   │
│  └─ Submit Button    │
└─────────────────┘
        ↓
    [Authenticate]
        ↓
┌─────────────────┐
│  Authenticated      │
├─────────────────┤
│  Dashboard (/dashboard)      │
│  ├─ Total Students Count     │
│  ├─ Total Courses Count      │
│  └─ Quick Action Links       │
│                              │
│  Students (/students)        │
│  ├─ Students Table           │
│  ├─ Search/Filter            │
│  ├─ Pagination               │
│  └─ Action Buttons           │
│     ├─ Add New Student       │
│     ├─ Edit Student          │
│     └─ Delete Student        │
│                              │
│  Add Student (/add-student)  │
│  ├─ First Name Field         │
│  ├─ Last Name Field          │
│  ├─ Email Field              │
│  ├─ Phone Field              │
│  └─ Submit Button            │
│                              │
│  Edit Student (/edit-student/{id}) │
│  ├─ Pre-filled Form Fields       │
│  ├─ Update Student Button        │
│  └─ Cancel Button                │
│                              │
│  Courses (/courses)          │
│  ├─ Courses Table            │
│  ├─ Create Course            │
│  ├─ Edit Course              │
│  └─ Delete Course            │
│                              │
│  Attendance (/attendance)    │
│  ├─ Select Student           │
│  ├─ Select Course            │
│  ├─ Mark Attendance          │
│  ├─ Attendance Report        │
│  └─ Generate Report          │
│                              │
│  Navigation Bar (All Pages)  │
│  ├─ Home Link                │
│  ├─ Dashboard Link           │
│  ├─ Students Link            │
│  ├─ Courses Link             │
│  ├─ Attendance Link          │
│  └─ Logout Link              │
└─────────────────┘
```

---

## Page Routes Reference

| Page Name | Route | Auth Required | Purpose |
|-----------|-------|---|---------|
| Home | `/` | No | Landing page with intro |
| Login | `/login` | No | Admin authentication |
| Dashboard | `/dashboard` | ✅ Yes | Overview & quick access |
| Students | `/students` | ✅ Yes | Manage students (list) |
| Add Student | `/add-student` | ✅ Yes | Create new student |
| Edit Student | `/edit-student/{id}` | ✅ Yes | Modify student info |
| Courses | `/courses` | ✅ Yes | Manage courses |
| Attendance | `/attendance` | ✅ Yes | Track attendance |

---

## Component Breakdown

### Navigation Bar (Appears on All Pages)
```
[📚 Student Management System] | [Home] [Dashboard] [Students] [Courses] [Attendance] [Logout]
```

**When Logged Out:**
- Shows: Home, Login links
- Hides: Dashboard, Students, Courses, Attendance, Logout

**When Logged In:**
- Shows: Home, Dashboard, Students, Courses, Attendance, Logout
- Displays: "Logout (username)" with current user's name

### Footer (Appears on All Pages)
```
© 2024 Student Management System. All rights reserved.
```

---

## Typical User Journey

### First-Time User
1. Open http://127.0.0.1:8000
2. See home page with "Login here" link
3. Click login link → /login
4. See option to register
5. Click "Register here"
6. Fill registration form
7. Submit → Registered successfully
8. Redirected to login page
9. Enter credentials
10. Click Login
11. Stored JWT token in browser
12. Redirected to /dashboard

### Regular Admin User
1. Open http://127.0.0.1:8000
2. Automatically redirected to dashboard (if already logged in)
3. View statistics
4. Navigate using top menu
5. Perform CRUD operations on students/courses
6. Track attendance
7. Logout when done

---

## Key Features

### 1. Student Management
- **List Students**: View all enrolled students with pagination
- **Add Student**: Create new student record
- **Edit Student**: Modify student information
- **Delete Student**: Remove student from system
- **Enroll Course**: Assign student to course

### 2. Course Management
- **List Courses**: View all available courses
- **Add Course**: Create new course
- **Edit Course**: Update course details
- **Delete Course**: Remove course

### 3. Attendance Tracking
- **Mark Attendance**: Record student attendance for course
- **View Reports**: See attendance statistics
- **Calculate Percentage**: Automatic calculation of attendance %

### 4. Admin Dashboard
- **Statistics**: Total students and courses count
- **Quick Links**: Fast access to main features
- **Recent Activity**: Can be extended to show recent actions

---

## UI/UX Features

### Responsive Design
- Works on desktop, tablet, and mobile
- Adjusts layout for screens ≤480px, ≤768px
- Touch-friendly buttons and inputs

### Color Scheme
- **Primary**: Blue (#3498db) - Main actions
- **Danger**: Red (#e74c3c) - Delete operations
- **Success**: Green (#27ae60) - Confirmations
- **Info**: Light blue (#2980b9) - Information

### Forms
- All forms are client-side validated
- Error messages displayed inline
- Submit buttons disabled during processing
- Responsive field layout

### Tables
- Sortable columns (when enabled)
- Pagination controls
- Action buttons (Edit, Delete)
- Search/filter functionality

### Alerts
- Success messages (green)
- Error messages (red)
- Info messages (blue)
- Auto-dismiss after 3 seconds

---

## JavaScript Functions

### Authentication
```javascript
getToken()              // Retrieve JWT from localStorage
setToken(token)         // Store JWT in localStorage
logout()                // Clear token and redirect to home
getAuthHeaders()        // Return authorization headers
```

### API Calls
```javascript
fetchStudents()                                    // GET /api/students
createStudent(data)                                // POST /api/students
updateStudent(id, data)                            // PUT /api/students/{id}
deleteStudent(id)                                  // DELETE /api/students/{id}
fetchCourses()                                     // GET /api/courses
createCourse(data)                                 // POST /api/courses
updateCourse(id, data)                             // PUT /api/courses/{id}
deleteCourse(id)                                   // DELETE /api/courses/{id}
markAttendance(data)                               // POST /api/attendance
getAttendanceReport(studentId, courseId)           // GET /api/attendance/report/...
```

### UI Utilities
```javascript
showAlert(message, type)   // Display alert box
formatDate(dateString)     // Format date for display
```

---

## Error Handling

### Common Errors & Solutions

**404 - Page Not Found**
- Check URL is correct
- Verify authentication for protected routes
- Clear browser cache

**401 - Unauthorized**
- JWT token expired (re-login required)
- Invalid credentials
- Token not included in request

**400 - Bad Request**
- Missing required fields
- Invalid data format
- Duplicate email/username

**500 - Server Error**
- Check server console for details
- Verify database connection
- Review error logs

### Error Messages
- Displayed in red alert boxes
- Appear at top of page
- Auto-dismiss after 3 seconds
- Can be manually dismissed

---

## Performance Tips

### For Better Performance
1. **Clear Browser Cache** if seeing stale pages
2. **Use Modern Browser** (Chrome, Firefox, Edge, Safari)
3. **Fast Internet Connection** for optimal loading
4. **Close Unused Tabs** to free up resources
5. **Disable Browser Extensions** if experiencing issues

### Network Requests
- Average page load: 500ms-1s
- API calls: 100-500ms each
- Pagination: Load 10 records by default
- Maximum records per request: 100

---

## Keyboard Shortcuts (Planned)
- `Ctrl+K` - Search/Quick Command
- `Ctrl+L` - Logout
- `Ctrl+D` - Dashboard
- `Esc` - Close dialogs

---

## Accessibility Features

### Screen Reader Support
- Semantic HTML structure
- ARIA labels where needed
- Form labels associated with inputs

### Keyboard Navigation
- Tab through form fields
- Enter to submit forms
- Esc to close dialogs
- Arrow keys for pagination

### Visual Accessibility
- Sufficient color contrast
- Clear error messages
- Focus indicators on interactive elements

---

## Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Full Support |
| Firefox | 88+ | ✅ Full Support |
| Safari | 14+ | ✅ Full Support |
| Edge | 90+ | ✅ Full Support |
| IE | 11 | ⚠️ Limited (no CSS Grid) |

---

## File Dependencies

### CSS (style.css)
- Loaded on every page via `<link>` tag
- Contains styles for all components
- ~700 lines of responsive CSS

### JavaScript (main.js)
- Loaded on every page via `<script>` tag
- Provides API client and utilities
- ~400 lines of utility functions

### Jinja2 Variables Required
- `request` - FastAPI Request object
- `is_authenticated` - Boolean
- `username` - String or None

---

## Extending the UI

### To Add New Page:

1. **Create Template**: `app/templates/new_page.html`
   ```html
   {% extends "layout.html" %}
   {% block title %}New Page - Student Management System{% endblock %}
   {% block content %}
   <!-- Your content here -->
   {% endblock %}
   ```

2. **Add Route**: `app/routers/web_router.py`
   ```python
   @router.get("/new-page")
   def new_page(request: Request, current_admin: Admin = Depends(get_current_user_optional)):
       if not current_admin:
           return RedirectResponse(url="/login")
       context = {
           "request": request,
           "is_authenticated": True,
           "username": current_admin.username
       }
       return request.app.state.templates.TemplateResponse("new_page.html", context)
   ```

3. **Update Navigation**: Edit `app/templates/layout.html` navbar

---

**Last Updated:** January 2024  
**Version:** 2.0.0 (Full-Stack UI)
