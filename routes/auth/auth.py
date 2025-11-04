from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from models.user import UserRegister,UserLogin
from datetime import datetime
from config.database import engine
from sqlalchemy import text
from models.common import MasterResponse
# from app.models import RequestData

router = APIRouter(prefix="/auth", tags=["Auth Route"])

@router.get("/")
def get_auth_basic():
    return {"message": "Entry to auth"}

@router.post("/register")
def register_user(user: UserRegister):
    current_time = datetime.now()
    user_data = user.dict()
    user_data['created_on'] = current_time
    user_data['updated_on'] = current_time
    try:
        with engine.begin() as conn:  # ✅ use engine.begin() to auto-commit
            insert_query = text("""
                INSERT INTO user (firstname, lastname, mobileno, emailid, password, dateofbirth,
                                  gender, photo, status, created_on, updated_on)
                VALUES (:firstname, :lastname, :mobileno, :emailid, :password, :dateofbirth,
                        :gender, :photo, :status, :created_on, :updated_on)
            """)
            conn.execute(insert_query, user_data)
        return {"message": "User inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Entry to auth register"}

@router.post("/login")
def login_user(user: UserLogin):
    try:
        with engine.begin() as conn:  # ✅ use engine.begin() to auto-commit
            _query = text("""
                SELECT * FROM user WHERE mobileno=:mobileno AND password=:password
            """)
            result = conn.execute(_query, {"mobileno": user.mobileno,"password":user.password})
            resp = result.fetchone()
            if resp:
                return {"message": "User Found successfully"}
            return {"message": "User not Found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-profile/{userId}")
def getProfile(userId:int):
    print("userId",userId)
    try:
        with engine.begin() as conn: 
            _query = text("""SELECT * FROM user WHERE user_id=:user_id""")
            result = conn.execute(_query,{"user_id":userId})
            row = result.mappings().fetchone()
            user_data = UserRegister(
                firstname=row["firstname"],
                lastname=row["lastname"],
                emailid=row["emailid"],
                mobileno=row["mobileno"],
                password=row["password"],
                dateofbirth=row["dateofbirth"],
                gender=row["gender"],
                photo=row["photo"],
                status=row["status"]
            )

        return MasterResponse(
                message="User Profile Found Successfully",
                status="200",
                data=user_data.dict()
            ) 
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))