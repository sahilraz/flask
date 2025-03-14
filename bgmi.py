from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

headersList = {
 "Host": "www.unipin.com",
 "accept": "application/json, text/javascript, */*; q=0.01",
 "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7,zh-CN;q=0.6,zh;q=0.5",
 "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
 "cookie": "_scid_r=okm3GRVlMDSopAmdJtVI97Dec5atBdmb4c1VWA;_ga_09T7E74QTG=GS1.1.1741959766.9.1.1741959849.57.0.0;_ym_uid=1741800271818708586;bgmi_cust_email=sahilraz9265%40gmail.com;_ga=GA1.2.2058187988.1741800271;redeem_banner=yes;cust_email=sahilraz9265%40gmail.com;_ScCbts=%5B%5D;_ym_d=1741800271;_fbp=fb.1.1741800271526.172389088134105812;_gcl_au=1.1.1942139497.1741800271;_gid=GA1.2.1256048317.1741800271;_scid=r0m3GRVlMDSopAmdJtVI97Dec5atBdmb4c1VNw;_sctr=1%7C1741717800000;_tt_enable_cookie=1;_ttp=01JPA19RGRSH184RH0MWFR0JBM_.tt.1;_ym_isad=1;bgmi_rgid=WURTVm0wM1FzNGR1WS9jMkp1d2puQT09;bgmi_userid=5299709743;CookieConsent={stamp:%272JazTRiEu056T4BkRM2x54Np06ltzoUypkAI5QPqTMhTpd1sZJjKbg==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1741800269106%2Cregion:%27in%27};region=IN;unipin_session=eyJpdiI6Ikh2Y2NOSFIzZjdaSjlMWTZKMnVvNlE9PSIsInZhbHVlIjoiaGd5czRLTnZJWmp1RHgyV3NLaXM5dzlaazROUDQrdWttbnJlRlpkUG1MZmVVK1wvTTQxbE9lUURGUk9ySjN4Y0tsZkl2Nk5xQVBHMDdDM1wvakVrTzBoc0FUMDBSY0FBQWNYMlVcL3FJSk9pclNLWlNac3o1eDRJZThITU1BUFV4UW4iLCJtYWMiOiJlODlkN2RiZDNjM2IxNGUzZjdiOGMxOGRkYThjMDE3MzViZTlkNzAwYzZiNGI2YzM5M2FmOTc3YjRjNmY0ZDBlIn0%3D;XSRF-TOKEN=eyJpdiI6IlhlNGNxcDJwbFhKOW1oK21vazZSWkE9PSIsInZhbHVlIjoiNmZCNXFxdk9wM0k3d2s4NE5rajhYaEQrZjhSZEc3OGZKemNIN0E2bmFwYkdTakFRV2ZiVEhLRlpPdTZZbFVFUCIsIm1hYyI6ImEwOTc5MzY1NGY2ODllY2VhNzhkNjM1MTBjYjM1ZjdhOGFmNjczNjJhZTA1ZDhjMGYzN2JhMDZkMTlhNGJkMGEifQ%3D%3D",
 "origin": "https://www.unipin.com",
 "priority": "u=1, i",
 "referer": "https://www.unipin.com/in/bgmi",
 "sec-fetch-dest": "empty",
 "sec-fetch-mode": "cors",
 "sec-fetch-site": "same-origin",
 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
 "x-csrf-token": "Qsqk0BoYXwBQZhWdo8sbZH7hcemEsanw4dONXuzi",
 "x-requested-with": "XMLHttpRequest" 
}


def get_checkout_details(dyn):
    url = f"https://www.unipin.com/in/bgmi/checkout/{dyn}"
    response = requests.get(url, headers=headersList)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("div", class_="details-row")
        for row in rows:
            label = row.find("div", class_="details-label text-white-50")
            value = row.find("div", class_="details-value")
            if label and value and "Username" in label.get_text(strip=True):
                return value.get_text(strip=True)
    return None


@app.route("/get_user", methods=["POST", "GET"])
def get_user():
    uid = request.args.get("uid") or request.json.get("uid")
    if not uid:
        return "Uid is Required", 400


    reqUrl = "https://www.unipin.com/in/bgmi/inquiry"
    payload = f"rgid=WURTVm0wM1FzNGR1WS9jMkp1d2puQT09&userid={uid}&did=5218&pid=764&influencer=&cust_email=sahilraz9265@gmail.com"
    response = requests.post(reqUrl, data=payload, headers=headersList)

    if response.status_code == 200:
        try:
            json_response = response.json()
            if json_response.get("status") == "1":
                dyn = json_response.get("message")
                username = get_checkout_details(dyn)
                return username if username else "Username not found", 200
            else:
                return "Incorrect Uid or Player Id", 400
        except requests.exceptions.JSONDecodeError:
            return jsonify({"error": "Failed to decode JSON response"}), 500
    else:
        return jsonify({"error": f"Request failed with status code {response.status_code}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
