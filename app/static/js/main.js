/**
 * Main JavaScript for Student Management System Frontend
 * Uses session-based auth (cookies) instead of JWT in localStorage.
 * Handles API interactions and UI management.
 */

// ============================
// Session-based Authentication Helpers
// ============================

/**
 * Clear authentication client-side artifacts and redirect to logout URL.
 * Server-side session will be cleared by the /logout route.
 */
function logout() {
    // Clean any leftover JWT token (legacy)
    localStorage.removeItem('token');
    localStorage.removeItem('token_type');

    // Redirect to server logout which clears the session cookie
    window.location.href = '/logout';
}

/**
 * Use fetch that includes cookies (session cookie) automatically.
 * opts is similar to fetch options (method, headers, body...).
 */
function fetchWithSession(url, opts = {}) {
    const defaultOpts = {
        credentials: 'include', // ensure cookies are sent
        headers: {
            'Content-Type': 'application/json'
        }
    };

    // Merge headers if provided
    opts.headers = Object.assign({}, defaultOpts.headers, opts.headers || {});
    const finalOpts = Object.assign({}, defaultOpts, opts);
    return fetch(url, finalOpts);
}

// ============================
// API Calls (session-based)
// ============================

/**
 * Fetch students list from API
 */
async function fetchStudents(skip = 0, limit = 10, search = null) {
    let url = `/api/students?skip=${skip}&limit=${limit}`;
    if (search) {
        url += `&search=${encodeURIComponent(search)}`;
    }

    try {
        const response = await fetchWithSession(url);
        if (response.status === 401) {
            // not authenticated
            window.location.href = '/login';
            return null;
        }
        if (response.ok) {
            return await response.json();
        } else {
            const err = await response.json().catch(() => ({}));
            console.error('API Error (fetchStudents):', err);
            return null;
        }
    } catch (error) {
        console.error('Fetch error (fetchStudents):', error);
        return null;
    }
}

/**
 * Fetch single student
 */
async function fetchStudent(studentId) {
    try {
        const response = await fetchWithSession(`/api/students/${studentId}`);
        if (response.status === 401) {
            window.location.href = '/login';
            return null;
        }
        if (response.ok) return await response.json();
    } catch (error) {
        console.error('Fetch error (fetchStudent):', error);
    }
    return null;
}

/**
 * Create a new student
 */
async function createStudent(studentData) {
    try {
        const response = await fetchWithSession('/api/students', {
            method: 'POST',
            body: JSON.stringify(studentData)
        });

        if (response.status === 401) {
            window.location.href = '/login';
            return null;
        }

        if (response.ok) return await response.json();

        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || 'Failed to create student');
    } catch (error) {
        console.error('Create error (createStudent):', error);
        throw error;
    }
}

/**
 * Update student
 */
async function updateStudent(studentId, studentData) {
    try {
        const response = await fetchWithSession(`/api/students/${studentId}`, {
            method: 'PUT',
            body: JSON.stringify(studentData)
        });

        if (response.status === 401) {
            window.location.href = '/login';
            return null;
        }

        if (response.ok) return await response.json();

        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || 'Failed to update student');
    } catch (error) {
        console.error('Update error (updateStudent):', error);
        throw error;
    }
}

/**
 * Delete student
 */
async function deleteStudent(studentId) {
    try {
        const response = await fetchWithSession(`/api/students/${studentId}`, {
            method: 'DELETE'
        });

        if (response.status === 401) {
            window.location.href = '/login';
            return false;
        }

        return response.ok;
    } catch (error) {
        console.error('Delete error (deleteStudent):', error);
        return false;
    }
}

/**
 * Fetch courses list from API
 */
async function fetchCourses(skip = 0, limit = 10) {
    try {
        const response = await fetchWithSession(`/api/courses?skip=${skip}&limit=${limit}`);
        if (response.status === 401) {
            window.location.href = '/login';
            return null;
        }
        if (response.ok) return await response.json();
    } catch (error) {
        console.error('Fetch error (fetchCourses):', error);
    }
    return null;
}

// ============================
// UI/UX Helpers (unchanged)
// ============================

/**
 * Show alert message to user
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="close-btn" onclick="this.parentElement.style.display='none';">&times;</button>
    `;

    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);

        if (type === 'success') {
            setTimeout(() => {
                if (alertDiv.parentElement) {
                    alertDiv.style.display = 'none';
                }
            }, 5000);
        }
    }
}

/**
 * Format date to readable format
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

/**
 * Format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

/**
 * Show loading spinner
 */
function showLoading() {
    document.body.style.opacity = '0.6';
    document.body.style.pointerEvents = 'none';
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    document.body.style.opacity = '1';
    document.body.style.pointerEvents = 'auto';
}

// ============================
// Page Redirect Helpers (unchanged)
// ============================

function goToStudents() { window.location.href = '/students'; }
function goToAddStudent() { window.location.href = '/add-student'; }
function goToEditStudent(studentId) { window.location.href = `/edit-student/${studentId}`; }
function goToCourses() { window.location.href = '/courses'; }
function goToAttendance() { window.location.href = '/attendance'; }
function goToDashboard() { window.location.href = '/dashboard'; }

// ============================
// Form Validation (unchanged)
// ============================

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidRequired(value) {
    return value && value.trim().length > 0;
}

function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) form.reset();
}

// ============================
// Initialize
// ============================

document.addEventListener('DOMContentLoaded', function () {
    // Navigation and auth state for UI are handled by server-side templates.
    // If you need client-side probes, call /api/auth/me (a session-check endpoint).
    updateNavigation();
});

/**
 * updateNavigation — keep minimal. Server templates handle the main nav.
 */
function updateNavigation() {
    // left intentionally minimal — server renders correct nav based on session
}

// Debug
console.log('Student Management System Frontend (session-mode) Loaded');
