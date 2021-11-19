import pprint

import requests

import addressing.b4e_addressing.addresser
from addressing.b4e_addressing import addresser


def submit_and_get_response(url, payload):
    response = requests.post(url=url, json=payload)

    res_data = response.json()

    return res_data, response.status_code


def registration(base_url="http://localhost:8005"):
    payload = {
        "privateKeyHex": "bf52e1d1221ac207d90aa109224e09e2b9d1b40fb3b9cf806c4631b37f7ffd8a",
        "profile": {
            "address": "so 1, dai co viet, hai ba trung, ha noi",
            "description": "lorem ipsum....",
            "email": "qwer@asdf.com",
            "nameInEnglish": "hust",
            "phone": "0345678901",
            "publicKey": "0216d0568a0a8624e56b183237354a71fc5ea1b357476a2276fff798db7fef9830",
            "universityName": "bkhn",
            "imgSrc": "data:image/png;base64,iVBORw0KGgoAAA..."
        }
    }
    url = f"{base_url}/staff/register"
    return submit_and_get_response(url, payload)


def ministry_accept(base_url="http://localhost:8005"):
    payload = {
        "privateKeyHex": "6cebf871e936d15b6540dc714dcff176839f73359d30ae49ae8ec1d44bd276db",
        "requesterPublicKey": "0216d0568a0a8624e56b183237354a71fc5ea1b357476a2276fff798db7fef9830",
        "decision": "accept"
    }
    url = f"{base_url}/vote"
    return submit_and_get_response(url, payload)


def create_teachers(base_url="http://localhost:8005"):
    """

    :param base_url:
    :return:
    """
    payload = {
        "privateKeyHex": "bf52e1d1221ac207d90aa109224e09e2b9d1b40fb3b9cf806c4631b37f7ffd8a",
        "profiles": [
            {
                "school": "KCNTT",
                "department": "CNPM",
                "teacherId": "GV00001",
                "name": "Vũ Văn Thiệu",
                "publicKey": "030bf4a5c4483e19fac45611f1e806bdac7bf0121104c5040ff88fc4c84d2fdefe"
            },
            {
                "school": "KCNTT",
                "department": "Innovation Centre",
                "teacherId": "GV00002",
                "name": "Nguyễn Phi Lê",
                "publicKey": "02ca0ff62709950e48ea2cec8c2968904d5275a8dc0db5dfe1bd01e321097227ec"
            }, {
                "school": "KCNTT",
                "department": "CNPM",
                "teacherId": "GV00003",
                "name": "Vũ Văn Thanh",
                "publicKey": "037d5320d8332384eaf9e7afbd6ca64b6491f24a4898046d01b0df57b16725a813"
            }
        ]
    }
    url = f"{base_url}/staff/create-teachers"
    return submit_and_get_response(url, payload)


def create_edu_program(base_url="http://localhost:8005"):
    payload = {
        "privateKeyHex": "bf52e1d1221ac207d90aa109224e09e2b9d1b40fb3b9cf806c4631b37f7ffd8a",
        "profiles": [
            {
                "publicKey": "0286bdc0501ea9625d83b535021faf29a3b3bf563d4fed85ffd63ede0b498304ed",
                "eduProgram": {
                    "eduProgramId": "MI1110",
                    "name": "Kỹ thuật máy tính - K64",
                    "totalCredit": 5,
                    "minYear": 0,
                    "maxYear": 8
                }
            },
            {
                "publicKey": "03924ce3e1b561daef9ac6aad57477aeeeac29f8cbdb1fa0cf5930875b534e6598",
                "eduProgram": {
                    "eduProgramId": "MI1110",
                    "name": "Khoa học máy tính - K64",
                    "totalCredit": 1,
                    "minYear": 0,
                    "maxYear": 8
                }
            }
        ]
    }

    url = f"{base_url}/staff/create-students"
    return submit_and_get_response(url, payload)


def create_classes(base_url="http://localhost:8005"):
    payload = {
        "privateKeyHex": "bf52e1d1221ac207d90aa109224e09e2b9d1b40fb3b9cf806c4631b37f7ffd8a",
        "classes": [
            {
                "classId": "123121",
                "subjectId": "MI1110",
                "credit": "4",
                "teacherPublicKey": "030bf4a5c4483e19fac45611f1e806bdac7bf0121104c5040ff88fc4c84d2fdefe",
                "studentPublicKeys": [
                    "0286bdc0501ea9625d83b535021faf29a3b3bf563d4fed85ffd63ede0b498304ed",
                    "03924ce3e1b561daef9ac6aad57477aeeeac29f8cbdb1fa0cf5930875b534e6598"
                ]
            },
            {
                "classId": "111132",
                "subjectId": "MI1110",
                "credit": "4",
                "teacherPublicKey": "038018863874ca359f5c3f508c7c73c5fc8a90b4b57af1caf19e1bef5369c0ec1e",
                "studentPublicKeys": [
                    "0286bdc0501ea9625d83b535021faf29a3b3bf563d4fed85ffd63ede0b498304ed",
                    "03924ce3e1b561daef9ac6aad57477aeeeac29f8cbdb1fa0cf5930875b534e6598"
                ]
            }, {
                "classId": "123",
                "subjectId": "MI1110",
                "credit": "4",
                "teacherPublicKey": "030bf4a5c4483e19fac45611f1e806bdac7bf0121104c5040ff88fc4c84d2fdefe",
                "studentPublicKeys": [
                    "0286bdc0501ea9625d83b535021faf29a3b3bf563d4fed85ffd63ede0b498304ed",
                    "03924ce3e1b561daef9ac6aad57477aeeeac29f8cbdb1fa0cf5930875b534e6598"
                ]
            },
            {
                "classId": "12345",
                "subjectId": "MI1110",
                "credit": "4",
                "teacherPublicKey": "038018863874ca359f5c3f508c7c73c5fc8a90b4b57af1caf19e1bef5369c0ec1e",
                "studentPublicKeys": [
                    "0286bdc0501ea9625d83b535021faf29a3b3bf563d4fed85ffd63ede0b498304ed",
                    "03924ce3e1b561daef9ac6aad57477aeeeac29f8cbdb1fa0cf5930875b534e6598"
                ]
            }
        ]
    }

    url = f"{base_url}/staff/create-classes"
    return submit_and_get_response(url, payload)


def setup_environment(base_url):
    registration(base_url)
    ministry_accept(base_url)
    create_teachers(base_url)
    create_edu_program(base_url)
    create_classes(base_url)


def submit_grate(base_url="http://localhost:8005"):
    payload = {
        "privateKeyHex": "24749245e0ffbf01f03ed1b3539dcbc535104fd30acfd220cd1c917e05ce12ab",
        "classId": "123121",
        "universityPublicKey": "0216d0568a0a8624e56b183237354a71fc5ea1b357476a2276fff798db7fef9830",
        "grades": [
            {
                "studentPublicKey": "03924ce3e1b561daef9ac6aad57477aeeeac29f8cbdb1fa0cf5930875b534e6598",
                "eduProgramId": "MI1110",
                "cipher": "k+HYsjQQXyymw5n+OhI3TlA1QX16beaypK/KVbNap/oiNyPI9fUjY7wpyoCfCSp9m9Dqarlkrq//ucsHdNfSEyTUAop0sA7b",
                "hash": "wWw3fqz28LXPimq4LRtUcw4wLO3g0/FOzS1gHB1Rj/0="
            },
            {
                "studentPublicKey": "0286bdc0501ea9625d83b535021faf29a3b3bf563d4fed85ffd63ede0b498304ed",
                "eduProgramId": "MI1110",
                "cipher": "k+HYsjQQXyymw5n+OhI3TlA1QX16beayPGr3gOnJB3MiNyPI9fUjY7wpyoCfCSp9m9Dqarlkrq//ucsHdNfSEyTUAop0sA7b",
                "hash": "kZUzG4evXJsUmQQ7RWyOslkCf3TdiWXuGqdIbSQSJlM="
            }
        ]
    }

    url = f"{base_url}/teacher/submit-grade"
    return submit_and_get_response(url, payload)


def edit_grade(base_url="http://localhost:8005"):
    payload = {
        "privateKeyHex": "24749245e0ffbf01f03ed1b3539dcbc535104fd30acfd220cd1c917e05ce12ab",
        "classId": "123121",
        "studentPublicKey": "03924ce3e1b561daef9ac6aad57477aeeeac29f8cbdb1fa0cf5930875b534e6598",
        "universityPublicKey": "0216d0568a0a8624e56b183237354a71fc5ea1b357476a2276fff798db7fef9830",
        "cipher": "UDATED CIPER k+HYsjQQXyymw5n+OhI3TlA1QX16beayPGr3gOnJB3MiNyPI9fUjY7wpyoCfCSp9fEQ7CgYdeS//ucsHdNfSEyTUAop0sA7b",
        "hash": "X/+aXznRQDnVdT7dRTS/vrY4R1Mskyw0TZAXSlIRKeI="
    }
    url = f"{base_url}/teacher/edit-grade"
    return submit_and_get_response(url, payload)


def invalid_edit_grade(base_url="http://localhost:8005"):
    payload = {
        "privateKeyHex": "4be7779ca413b3cd0548212e5c63486465a39f9c85b1e7a2ee27bf4d3589994d",
        "_publicKeyHex": "037d5320d8332384eaf9e7afbd6ca64b6491f24a4898046d01b0df57b16725a813",
        "classId": "123121",
        "studentPublicKey": "03924ce3e1b561daef9ac6aad57477aeeeac29f8cbdb1fa0cf5930875b534e6598",
        "universityPublicKey": "0216d0568a0a8624e56b183237354a71fc5ea1b357476a2276fff798db7fef9830",
        "cipher": "k+HYsjQQXyymw5n+OhI3TlA1QX16beayPGr3gOnJB3MiNyPI9fUjY7wpyoCfCSp9fEQ7CgYdeS//ucsHdNfSEyTUAop0sA7b",
        "hash": "/VvWV0B4/diHkunF/WDfXuPDXoytb7SVWJarLJjWF+I="
    }
    url = f"{base_url}/teacher/edit-grade"
    return submit_and_get_response(url, payload)


def get_record(address, base_url="http://localhost:8005"):
    url = f"{base_url}/record/{address}"

    response = requests.get(url=url)

    res_data = response.json()

    return res_data, response.status_code


def get_grade_in_state(class_id, student_public_key, university_public_key, base_url="http://localhost:2727"):
    address = addresser.get_record_address(class_id, student_public_key, university_public_key)
    return get_record(address, base_url)


def get_grade_in_script(base_url="http://localhost:2727"):
    class_id = "123121"
    student_public_key = "03924ce3e1b561daef9ac6aad57477aeeeac29f8cbdb1fa0cf5930875b534e6598"
    university_public_key = "0216d0568a0a8624e56b183237354a71fc5ea1b357476a2276fff798db7fef9830"
    return get_grade_in_state(class_id, student_public_key, university_public_key, base_url)
