import json
import time

import requests


def data_create_certs(num):
    data = {
        "privateKeyHex": "bf52e1d1221ac207d90aa109224e09e2b9d1b40fb3b9cf806c4631b37f7ffd8a",
        "certificates": []
    }
    for i in range(num):
        data["certificates"].append({
            "school": "Viện Công nghệ thông tin và truyền thông",
            "eduProgramId": "MI1110" + str(i),
            "studentPublicKey": "0286bdc0501ea9625d83b535021faf29a3b3bf563d4fed85ffd63ede0b498304ed",
            "cipher": "qerqwrqweafads",
            "hash": "asdfasdfasdfasdfasfdasdf"
        })
    return data


def data_create_subjects(num):
    data = {
        "privateKeyHex": "24749245e0ffbf01f03ed1b3539dcbc535104fd30acfd220cd1c917e05ce12ab",
        "classId": "123121",
        "universityPublicKey": "0216d0568a0a8624e56b183237354a71fc5ea1b357476a2276fff798db7fef9830",
        "grades": []
    }

    for i in range(num):
        data["grades"].append({
            "studentPublicKey": "03924ce3e1b561daef9ac6aad57477aeeeac29f8cbdb1fa0cf5930875b534e6598",
            "eduProgramId": "MI1110" + str(i),
            "cipher": "pr1",
            "hash": "asdfasdf"
        })
    return data


def submit(url, data):
    parsed = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'Content-Length': '<calculated when request is sent>',
        'Connection': 'keep-alive'
    }
    start = time.time()
    response = requests.request("POST", url, headers=headers, data=parsed)
    end = time.time()
    duration = end - start
    return response, duration


def submit_certs(data):
    url = "http://localhost:8005/staff/create-certificates"
    return submit(url, data)


def submit_subjects(data):
    url = "http://localhost:8005/teacher/submit-grade"
    return submit(url, data)


def test_transcript(expose=21, step=250):
    f = open('./result.csv', 'w')
    f.write(f"number_transaction,cert_duration,subject_duration\n")
    for i in range(1, expose):
        num_tran = i * step
        certs_data = data_create_certs(num_tran)
        subjects_data = data_create_subjects(num_tran)
        while True:
            res, duration1 = submit_certs(certs_data)
            if res.status_code == 200:
                break
            time.sleep(i)
        while True:
            res, duration2 = submit_subjects(subjects_data)
            if res.status_code == 200:
                break
            time.sleep(i)
        f.write(f"{num_tran},{duration1},{duration2}\n")

    print("done !")


test_transcript(21,250)
