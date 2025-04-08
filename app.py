from flask import Flask, request
import time
import logging
import requests
import os
import dotenv
import json

dotenv.load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

if not os.getenv("ABUSEIPDB_API_KEY"):
    logging.error("ABUSEIPDB_API_KEY is not set. Please set it in the environment variables.")
    exit(1)

ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")
abuse_ip_list = set()
last_ip_report_time = {}
REPORT_INTERVAL = 15 * 60

@app.route('/robots.txt')
def robots():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    path = request.path

    logging.info(f"Access to robots.txt from {ip} - {user_agent}")

    robots_txt = "User-agent: *\nDisallow: /"
    return robots_txt, 200, {'Content-Type': 'text/plain'}

@app.route('/')
@app.route('/favicon.ico')
def not_suspicious():
    return "get out", 200

def report_to_abuse_ipdb(ip, user_agent, path):
    now = time.time()
    last_report = last_ip_report_time.get(ip, 0)

    if now - last_report < REPORT_INTERVAL:
        logging.info(f"Skipping AbuseIPDB report for {ip} (last reported {(now - last_report)/60:.1f} minutes ago)")
        return

    last_ip_report_time[ip] = now

    logging.info(f"Reporting {ip} to AbuseIPDB")

    url = "https://api.abuseipdb.com/api/v2/report"
    headers = {
        'Key': ABUSEIPDB_API_KEY,
        'Accept': 'application/json',
    }
    data = {
        'ip': ip,
        'categories': '19',
        'comment': f"Does not respect robots.txt: {user_agent} on {path}"
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        logging.info(f"Reported {ip} to AbuseIPDB: {response.json()}")
    except requests.RequestException as e:
        logging.error(f"Failed to report {ip} to AbuseIPDB: {e}")

def handle_bad_bots(ip, user_agent, path):
    logging.warning(f"[HONEYPOT] Detected bad bot: {ip} - {user_agent} - {path}")
    report_to_abuse_ipdb(ip, user_agent, path)

@app.errorhandler(404)
def handle_404(e):
    ip = request.headers.get('X-Real-IP', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    path = request.path

    handle_bad_bots(ip, user_agent, path)
    return "", 200

