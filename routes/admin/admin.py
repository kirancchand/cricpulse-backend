from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from models.admin import AddRole,AddUserRole
from models.common import MasterResponse
from datetime import datetime
from config.database import engine
from sqlalchemy import text
from typing import List, Dict, Any,Optional
# from app.models import RequestData

router = APIRouter(prefix="/admin", tags=["Auth Route"])

@router.get("/")
def get_auth_basic():
    return {"message": "Entry to auth"}

@router.post("/addRole")
def add_role(role:AddRole):
    role_data = role.dict()
    try:
        with engine.begin() as conn:  # ✅ use engine.begin() to auto-commit
            insert_query = text("""INSERT INTO role(role)VALUES (:role)""")
            conn.execute(insert_query, role_data)
        return MasterResponse(
                    message="Roles added successfully",
                    status="200",
                    data={}
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getAllRole")
def getAllRole():
    try:
        with engine.begin() as conn:  # ✅ use engine.begin() to auto-commit
            _query = text("""SELECT * FROM role""")
            result = conn.execute(_query)
            rows = [dict(row._mapping) for row in result]
            print(result)
            return MasterResponse(
                    message="Roles Found successfully",
                    status="200",
                    data=rows
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/updateUserRole")
def updateUserRole(req: AddUserRole):
    try:
        with engine.begin() as conn:
            # 1️⃣ Remove old roles for this user
            delete_query = text("DELETE FROM user_role WHERE user_id = :user_id")
            conn.execute(delete_query, {"user_id": req.user_id})

            # 2️⃣ Insert new roles
            insert_query = text("INSERT INTO user_role (user_id, role_id) VALUES (:user_id, :role_id)")
            for role_id in req.role_id:
                conn.execute(insert_query, {"user_id": req.user_id, "role_id": role_id})

        return MasterResponse(
            message="User roles updated successfully",
            status="200",
            data={"user_id": req.user_id, "roles": req.role_id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# @router.post("/register")
# def register_user(user: UserRegister):
#     current_time = datetime.now()
#     user_data = user.dict()
#     user_data['created_on'] = current_time
#     user_data['updated_on'] = current_time
#     try:
#         with engine.begin() as conn:  # ✅ use engine.begin() to auto-commit
#             insert_query = text("""
#                 INSERT INTO user (firstname, lastname, mobileno, emailid, password, dateofbirth,
#                                   gender, photo, status, created_on, updated_on)
#                 VALUES (:firstname, :lastname, :mobileno, :emailid, :password, :dateofbirth,
#                         :gender, :photo, :status, :created_on, :updated_on)
#             """)
#             conn.execute(insert_query, user_data)
#         return {"message": "User inserted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     return {"message": "Entry to auth register"}

# @router.post("/login")
# def login_user(user: UserLogin):
#     try:
#         with engine.begin() as conn:  # ✅ use engine.begin() to auto-commit
#             _query = text("""
#                 SELECT * FROM user WHERE mobileno=:mobileno AND password=:password
#             """)
#             result = conn.execute(_query, {"mobileno": user.mobileno,"password":user.password})
#             resp = result.fetchone()
#             if resp:
#                 return {"message": "User Found successfully"}
#             return {"message": "User not Found"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))