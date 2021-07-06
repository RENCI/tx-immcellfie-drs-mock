import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import PlainTextResponse, FileResponse

from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta 

app = FastAPI()

security = HTTPBasic()

AUTHENTICATION_TOKEN = "mock_irods_athentication_token"
SECRET_KEY = "111"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10000000000
API_HOST = os.environ.get("API_HOST", "localhost")
API_PORT = os.environ.get("API_PORT", "8000")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

objects = {
    "mock_obj1": 
    {
        "id":"mock_obj1",
        "name":"/devImmcellfieZone/home/test1/study",
        "self_uri":"drs://localhost/b670ec6a-78d2-438f-a180-885f49a016b4",
        "size":0,
        "created_time":"2019-09-06T15:28:03Z",
        "updated_time":"2019-09-06T15:28:03Z",
        "version":"0",
        "mime_type":"text/directory",
        "checksums":[
            {
                "checksum":"736e715a72017f1e6ce67e9e5d7d0dc4e6b6d29e6150f7dc1f011697910c3bdf",
                "type":"sha256"
            }
        ],
        "access_methods":[
            
        ],
        "contents":[
            {
                "name":"phenotype.csv",
                "id":"phonetype_csv",
                "drs_uri":[
                    "drs://localhost/39e87c10-dbb6-4d45-9e21-1257ea337104"
                ],
                "contents":[
                    
                ]
            },
            {
                "name":"gene.csv",
                "id":"gene_data",
                "drs_uri":[
                    "drs://localhost/ca8d9a9c-c3d1-417a-8663-6904d9870be1"
                ],
                "contents":[
                    
                ]
            }
        ],
        "description":"study data",
        "aliases":[
            "/devImmcellfieZone/home/test1/study"
        ]
    },
    "mock_obj2": {},
    "mock_obj3": {}
}

access = {
    "phenotype_csv": {
        "url": "http://{API_HOST}:{API_PORT}/irods-rest2/fileStream?path=/devImmcellfieZone/home/test1/study/phenotype.csv",
        "headers": [
            "X-API-KEY iU7Gc3dmeC1ECQ3"
        ]
    },
    "gene_data": {
        "url": f"http://{API_HOST}:{API_PORT}/irods-rest2/fileStream?path=/devImmcellfieZone/home/test1/study/gene.csv",
        "headers": [
            "X-API-KEY iU7Gc3dmeC1ECQ3"
        ]
    }
}

file_content = {
    "/devImmcellfieZone/home/test1/study/phenotype.csv": "phenotype.csv",
    "/devImmcellfieZone/home/test1/study/gene.csv": "gene.csv"
}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return username


@app.post("/irods-rest2/token")
async def post_irods_rest2_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "rods")
    correct_password = secrets.compare_digest(credentials.password, "woot")
    if not (correct_password and correct_username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect usernsme or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    access_token = create_access_token(
        data={"sub": credentials.username}
    )
    return PlainTextResponse(access_token)


@app.get("/ga4gh/drs/v1/objects/{guid}")
async def get_object(guid: str, current_user: str = Depends(get_current_user)):
    return objects[guid]

@app.get("/ga4gh/drs/v1/objects/{guid}/access/irods-rest")
async def get_object(guid: str, current_user: str = Depends(get_current_user)):
    return access[guid]


@app.get("/irods-rest2/fileStream")
async def get_object(path: str, current_user: str = Depends(get_current_user)):
    return FileResponse(file_content[path])
