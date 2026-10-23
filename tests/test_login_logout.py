class TestLoginPage:
    def test_login_page_renders(self, client):
        resp = client.get("/login")
        assert resp.status_code == 200
        assert b"Sign in" in resp.data

    def test_login_success(self, client):
        resp = client.post("/login", data={
            "email": "demo@spendly.com",
            "password": "demo123",
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert b"Welcome back!" in resp.data
        assert b"Demo User" in resp.data

    def test_login_sets_session(self, client):
        with client:
            client.post("/login", data={
                "email": "demo@spendly.com",
                "password": "demo123",
            })
            from flask import session
            assert session["user_id"] is not None
            assert session["user_name"] == "Demo User"

    def test_login_wrong_password(self, client):
        resp = client.post("/login", data={
            "email": "demo@spendly.com",
            "password": "wrongpassword",
        })
        assert resp.status_code == 200
        assert b"Invalid email or password." in resp.data

    def test_login_nonexistent_email(self, client):
        resp = client.post("/login", data={
            "email": "nobody@example.com",
            "password": "anything",
        })
        assert resp.status_code == 200
        assert b"Invalid email or password." in resp.data

    def test_login_empty_email(self, client):
        resp = client.post("/login", data={
            "email": "",
            "password": "somepass",
        })
        assert resp.status_code == 200
        assert b"Email is required." in resp.data

    def test_login_empty_password(self, client):
        resp = client.post("/login", data={
            "email": "demo@spendly.com",
            "password": "",
        })
        assert resp.status_code == 200
        assert b"Password is required." in resp.data

    def test_login_preserves_email_on_error(self, client):
        resp = client.post("/login", data={
            "email": "bad@example.com",
            "password": "wrong",
        })
        assert resp.status_code == 200
        assert b'value="bad@example.com"' in resp.data


class TestLogout:
    def test_logout_clears_session(self, client):
        client.post("/login", data={
            "email": "demo@spendly.com",
            "password": "demo123",
        })
        resp = client.get("/logout", follow_redirects=True)
        assert resp.status_code == 200
        assert b"You have been logged out." in resp.data
        assert b"Sign in" in resp.data

    def test_logout_when_not_logged_in(self, client):
        resp = client.get("/logout")
        assert resp.status_code == 302
