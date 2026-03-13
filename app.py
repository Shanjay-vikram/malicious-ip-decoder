from flask import Flask, render_template, request
import requests
import datetime

app = Flask(__name__)

def check_ip(ip):

    try:

        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        data = response.json()

        org = data.get("org")

        # Simple threat detection
        threat = "LOW"

        if org:
            org_lower = org.lower()

            if "vpn" in org_lower or "proxy" in org_lower:
                threat = "MEDIUM"

            if "tor" in org_lower or "hosting" in org_lower:
                threat = "HIGH"

        result = {
            "ip": ip,
            "city": data.get("city"),
            "region": data.get("regionName"),
            "country": data.get("country"),
            "org": org,
            "asn": data.get("as"),
            "threat": threat
        }

        return result

    except:
        return None


@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":

        ip = request.form["ip"].strip()

        result = check_ip(ip)

        if result:

            with open("info.txt", "a") as f:

                f.write(
                    str(datetime.datetime.now()) +
                    " | " +
                    str(result) +
                    "\n"
                )

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)