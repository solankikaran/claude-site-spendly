# Spec: Login and Logout

## Overview
Step 03 adds login and logout functionality to Spendly. Users who registered in Step 02 can now sign in with their email and password, maintain a session while browsing, and sign out when done. The login template already exists; this step wires up the POST handler and replaces the logout stub with a real session-clearing route.

## Depends on
- Step 01 — Database Setup (`get_db`, `init_db`, schema)
- Step 02 — Registration (`create_user`, `get_user_by_email`, `users` table, session pattern)

## Routes
- `POST /login` — validate credentials, start session — public
- `GET /logout` — clear session, redirect to landing — logged-in

The existing `GET /login` route already renders `login.html` but must be updated to accept `POST` as well.

## Database changes
No database changes.

## Templates
- **Modify:** `templates/login.html`
  - Change hardcoded `action="/login"` to `action="{{ url_for('login') }}"`
  - Add `value="{{ email }}"` to the email input to preserve input on validation failure

No new templates.

## Files to change
- `app.py` — update `/login` route to handle POST; replace `/logout` stub with real implementation; import `check_password_hash`
- `database/db.py` — add `verify_user(email, password)` helper that returns the user dict or `None`
- `templates/login.html` — fix form action URL and preserve email on error

## Files to create
- `tests/test_login_logout.py` — tests for login and logout flows

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw SQL with `?` parameterised queries only
- Passwords verified with `werkzeug.security.check_password_hash`
- Password verification logic lives in `database/db.py`, not in routes
- Session keys must match registration pattern: `session["user_id"]` and `session["user_name"]`
- Use `session.clear()` for logout to remove all session data
- Use `flash()` for success and error feedback
- All templates extend `base.html`
- Use `url_for()` for every internal link — never hardcode URLs
- Use CSS variables — never hardcode hex values

## Validation rules

| Field    | Rule                          | Error message                    |
|----------|-------------------------------|----------------------------------|
| email    | Must not be empty             | "Email is required."             |
| email    | Must match a registered user  | "Invalid email or password."     |
| password | Must not be empty             | "Password is required."          |
| password | Must match stored hash        | "Invalid email or password."     |

Note: use the same generic error for wrong email and wrong password to avoid leaking which field was incorrect.

## Definition of done
- [ ] `POST /login` with valid credentials sets `session["user_id"]` and `session["user_name"]`, flashes a welcome message, and redirects to `/`
- [ ] `POST /login` with unknown email re-renders login page with "Invalid email or password." error and preserves the entered email
- [ ] `POST /login` with wrong password re-renders login page with "Invalid email or password." error and preserves the entered email
- [ ] `POST /login` with empty email shows "Email is required."
- [ ] `POST /login` with empty password shows "Password is required."
- [ ] `GET /logout` clears the session, flashes a goodbye message, and redirects to `/`
- [ ] After logout, nav bar shows "Sign in" and "Get started" instead of user name
- [ ] `login.html` form action uses `url_for('login')`, not a hardcoded path
- [ ] `verify_user()` helper exists in `database/db.py` and is used by the login route
- [ ] All tests in `tests/test_login_logout.py` pass
