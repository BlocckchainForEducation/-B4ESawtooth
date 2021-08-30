import os


class Config:
    HOST = '0.0.0.0'
    PORT = 8082


class SawtoothConfig:
    REST_API = 'http://localhost:8008'
    VALIDATOR_TCP = 'tcp://localhost:4004'
    MAX_BATCH_SIZE = 500


class ElasticSearchConfig:
    HOST = 'localhost'
    PORT = 9200
    USER_INDEX = 'b4e_users'
    STUDENT_INDEX = 'b4e_students'
    INSTITUTION_INDEX = 'b4e_institutions'
    MINISTRY_INDEX = 'b4e_ministries'
    CERT_INDEX = 'b4e_certs'
    SUBJECT_INDEX = 'b4e_subjects'
    TEACHER_INDEX = 'b4e_teachers'
    SERVICE_TEACHER_INDEX = 'b4e_service_teachers'
    COURSE_INDEX = "b4e_courses"
    RECORD_INDEX = "b4e_records"
    BLOCK_INDEX = "b4e_blocks"
    MANAGER_INDEX = 'b4e_managers'
    LANDING_PAGE = 'b4e_landing_pages'


class MongoDBConfig:
    DOCKER_HOST = "b4e_network"
    HOST = "localhost"
    PORT = 27017
    USER_NAME = ""
    PASSWORD = ""
    DATABASE = "B4E_blockchain"
    UNIVERSITY_PROFILE = "UniversityProfile"
    VOTE_REQUEST = "VoteRequest"
    USER_COLLECTION = 'b4e_users'
    ENVIRONMENT_COLLECTION = 'b4e_environments'
    CLASS_COLLECTION = 'b4e_classes'
    ACTOR_COLLECTION = 'b4e_actors'
    PORTFOLIO_COLLECTION = 'b4e_portfolio'
    CERT_COLLECTION = 'b4e_certs'
    SUBJECT_COLLECTION = 'b4e_subjects'
    VOTING_COLLECTION = 'b4e_votings'
    VOTE_COLLECTION = 'b4e_votes'
    SERVICE_TEACHER_COLLECTION = 'b4e_service_teachers'
    COURSE_COLLECTION = "b4e_courses"
    RECORD_COLLECTION = "b4e_records"
    BLOCK_COLLECTION = "b4e_blocks"
    MANAGER_COLLECTION = 'b4e_managers'
    REGISTRATION_COLLECTION = 'b4e_registrations'
    JOB_COLLECTION = 'b4e_job'


class Status:
    ACTIVE = 1
    REJECT = 0
    WAIT = 2
    DELETE = 3


class KeyDefault:
    TOKEN = "TOKEN_SHARE"
    PERMISSION = "token_permission_key"


class Role:
    MINISTRY = 1
    INSTITUTION = 2
    STUDENT = 3
    GUEST = 4
    TEACHER = 21
    MANAGER = 22


class EmailConfig:
    SMTP_SSL_HOST = 'smtp.gmail.com'  # smtp.mail.yahoo.com
    SMTP_SSL_PORT = 587
    USERNAME = 'vchain.bkc'
    PASSWORD = 'bkc@12345'
    SENDER = 'vchain.bkc@gmail.com'
    SMTP_SSL_PORT2 = 465
    B4E_EMAIL_VERIFY = 'b.cert.verify@gmail.com'
    B4E_EMAIL_VERIFY_PASSWORD = 'bcert01012020'


class JWT:
    JWT_SECRET_KEY = "B4E_app_authentication"


class Permission:
    YES = 1
    NO = 0


class LandingPage:
    QR_CODE_PATH = './static/qrcode/'
    BAR_CODE_PATH = './static/barcode/'
    URL = '202.191.56.247:8000/landingpage'
    CLOSE_LIST = "close_list"


class Ipfs:
    HOST = "https://ipfs.infura.io"
    PORT = 5001


class Test:
    MINISTRY_PRIVATE_KEY = "6cebf871e936d15b6540dc714dcff176839f73359d30ae49ae8ec1d44bd276db"
    INSTITUTION_PRIVATE_KEY = "c8f337e8b0259e52635309ebe32bd807511b7c7cdb64caf5f61594736b1fdbe4"
    CIPHER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    HASH_DATA = "WQRUY124YOU23Y40IIWUQROPWQERU"
    DATABASE = "test_db"
    TEST_COLLECTION = "test_collection"


class SubscriberConfig:
    HOST = "localhost"
    PORT = 1212
    PROTOCOL = "http://"
    HOST_URL = "http://localhost:1212"
