from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from jose import jwt, JWTError


REFRESH_TOKEN_EXPIRE_DAYS = 7
# NOTE: For demo only — in production load from env / secrets manager
SECRET_KEY = "project"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

app = FastAPI(title="JWT Demo API")

class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenRequest(BaseModel):
	username: str
	password: str


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class TokenResponse(BaseModel):
	access_token: str
	token_type: str = "bearer"


class TokenValidation(BaseModel):
	valid: bool
	username: Optional[str] = None
	exp: Optional[int] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.now(timezone.utc) + expires_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


@app.post("/token", response_model=TokenResponse)
def issue_token(req: TokenRequest):
	# Very small demo authentication: accept any non-empty username/password
	if not req.username or not req.password:
		raise HTTPException(status_code=400, detail="username and password required")
	# In a real app validate credentials here
	token = create_access_token({"sub": req.username})
	return {"access_token": token}


def decode_token(token: str):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		return payload
	except JWTError:
		raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/validate", response_model=TokenValidation)
def validate_token(authorization: Optional[str] = Header(None)):
	# Accept either bare token in Authorization header or 'Bearer <token>'
	if not authorization:
		raise HTTPException(status_code=400, detail="Authorization header required")
	token = authorization.strip()
	if token.lower().startswith("bearer "):
		token = token.split(" ", 1)[1].strip()
	payload = decode_token(token)
	username = payload.get("sub")
	exp = payload.get("exp")
	return {"valid": True, "username": username, "exp": exp}


@app.get("/ping")
def ping():
	return {"ping": "pong"}
