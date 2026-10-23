# Spec: Registration

## Overview

Implement the user registration flow so visitors can create an account.
The register form (`register.html`) already exists and POSTs to `/register`,
but the route currently only handles GET. This step adds the POST handler,
server-side validation, password hashing, duplicate-email detection, session
setup, and the DB helper to insert a new user. On success the user is logged
in automatically and redirected to the landing page (profile page is not yet
built).

## Depends on

- **Step 1 — Database Setup** (complete): `users` table and `get_db()` must
  exist.

## Routes

- `POST /register` — validates form input, creates user, starts session,
  redirects — public

The existing `GET /register` route remains but needs a minor update to
preserve form values on validation failure.

## Database changes

No new tables or columns. The existing `users` table is sufficient.

## Templates

- **Modify:** `templates/register.html`
  - Fix hardcoded form action (`/register`) to use `url_for('register')`
  - Display field-level or flash error messages from the server
  - Preserve user input (name, email) on validation failure so the user
    does not have to re-type

- **Modify:** `templates/base.html`
  - Add flash message rendering block so flashes work site-wide
  - Update nav links to show user name + "Log out" when logged in,
    hide "Sign in / Get started" when logged in

## Files to change

- `app.py` — add POST handler to `/register`, configure `secret_key`,
  import `session`, `redirect`, `url_for`, `request`, `flash`, `abort`
- `database/db.py` — add `create_user()` helper
- `templates/register.html` — use `url_for()`, show errors, preserve input
- `templates/base.html` — flash messages, session-aware nav

## Files to create

None.

## New dependencies

No new dependencies. `werkzeug.security` (for `generate_password_hash`) and
`flask` (for `session`, `flash`, `redirect`, `request`) are already
installed.

## Rules for implementation

- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterized queries only — never interpolate user input into SQL
- Hash passwords with `werkzeug.security.generate_password_hash`
- Use CSS variables from `style.css` — never hardcode hex colour values
- All templates extend `base.html`
- Form validation must happen server-side (do not rely on HTML5 `required`
  alone)
- `create_user()` lives in `database/db.py`, not inline in the route
- Use Flask `session` for login state — store `user_id` and `user_name`
- Set `app.secret_key` from an environment variable with a dev fallback
- Duplicate email must return a clear error, not a 500

## Validation rules

| Field    | Rule                                     | Error message                        |
|----------|------------------------------------------|--------------------------------------|
| name     | Required, non-empty after strip          | "Name is required."                  |
| email    | Required, must contain `@`               | "A valid email is required."         |
| password | Required, minimum 8 characters           | "Password must be at least 8 characters." |
| email    | Must not already exist in `users` table  | "An account with that email already exists." |

## Definition of done

- [ ] `POST /register` with valid data creates a new row in `users`
- [ ] Password is stored as a hash, never in plain text
- [ ] Duplicate email shows an error and does not create a second row
- [ ] Missing or invalid fields re-render the form with error messages and
      preserved input
- [ ] On success, `session['user_id']` and `session['user_name']` are set
- [ ] On success, user is redirected (not rendered) away from the register
      page
- [ ] Nav bar shows the user's name and a "Log out" link when logged in
- [ ] Nav bar shows "Sign in / Get started" when logged out
- [ ] Flash messages render correctly on any page
- [ ] `register.html` form action uses `url_for('register')`, not a
      hardcoded path
- [ ] App starts without errors on port 5001
- [ ] No new pip packages added
