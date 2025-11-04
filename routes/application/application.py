from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from datetime import datetime
from config.database import engine
from sqlalchemy import text
from models.application import AuctionRegister,TeamRegister,ApplyToAuction,AddToTeam
from models.common import MasterResponse

# from app.models import RequestData

router = APIRouter(prefix="/application", tags=["App Route"])

@router.get("/")
def get_auth_basic():
    return {"message": "Entry to auth"}

@router.post("/addAuction")
def addAuction(AuctionRegister: AuctionRegister):
    current_time = datetime.now()
    auction_data = AuctionRegister.dict()
    auction_data['created_on'] = current_time
    auction_data['updated_on'] = current_time
    try:
        with engine.begin() as conn:  # ✅ use engine.begin() to auto-commit
            insert_query = text("""
                INSERT INTO auction (auction_name, auctioner_id, noofteams, noofplayers, start_date, end_date,
                                  venue, budget_per_team, bid_increment, base_value, status,created_on,updated_on)
                VALUES (:auction_name, :auctioner_id, :noofteams, :noofplayers, :start_date, :end_date,
                        :venue, :budget_per_team, :bid_increment, :base_value, :status, :created_on, :updated_on)
            """)
            conn.execute(insert_query, auction_data)
        return MasterResponse(
                    message="Aucton added successfully",
                    status="200",
                    data={}
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/updateAuction/{auction_id}")
def addAuction(auction_id: int, AuctionRegister: AuctionRegister):
    current_time = datetime.now()
    auction_data = AuctionRegister.dict()
    auction_data['updated_on'] = current_time
    auction_data['auction_id'] = auction_id   # ✅ include auction_id in parameters

    try:
        with engine.begin() as conn:  # auto-commit
            update_query = text("""
                UPDATE auction 
                SET auction_name=:auction_name,
                    auctioner_id=:auctioner_id,
                    noofteams=:noofteams,
                    noofplayers=:noofplayers,
                    start_date=:start_date,
                    end_date=:end_date,
                    venue=:venue,
                    budget_per_team=:budget_per_team,
                    bid_increment=:bid_increment,
                    base_value=:base_value,
                    status=:status,
                    updated_on=:updated_on 
                WHERE auction_id=:auction_id
            """)
            conn.execute(update_query, auction_data)   # ✅ pass only once
        return MasterResponse(
            message="Auction Updated successfully",
            status="200",
            data={}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/removeAuction/{auction_id}")
def removeAuction(auction_id: int):
    try:
        with engine.begin() as conn:  # auto-commit
            delete_query = text("""
                DELETE FROM auction
                WHERE auction_id=:auction_id
            """)
            conn.execute(delete_query, {"auction_id": auction_id})  # ✅ only pass auction_id
        return MasterResponse(
            message="Auction deleted successfully",
            status="200",
            data={}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    
@router.post("/addTeam")
def addTeam(TeamRegister: TeamRegister):
    team_data = TeamRegister.dict()
    try:
        with engine.begin() as conn:  # ✅ use engine.begin() to auto-commit
            insert_query = text("""
                INSERT INTO team (team_auction_id, team_name, team_owner_id, team_total_value, team_balance_value)
                VALUES (:team_auction_id, :team_name, :team_owner_id, :team_total_value, :team_balance_value)
            """)
            conn.execute(insert_query, team_data)
        return MasterResponse(
                    message="Team added successfully",
                    status="200",
                    data={}
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/updateTeam/{team_id}")
def updateTeam(team_id:int,TeamRegister: TeamRegister):
    team_data = TeamRegister.dict()
    team_data["team_id"]=team_id
    try:
        with engine.begin() as conn:  # ✅ use engine.begin() to auto-commit
            update_query = text("""
                UPDATE team 
                SET team_name=:team_name, 
                    team_owner_id=:team_owner_id, 
                    team_balance_value=:team_balance_value
                WHERE team_id=:team_id
                
            """)
            conn.execute(update_query, team_data)
        return MasterResponse(
                    message="Team updated successfully",
                    status="200",
                    data={}
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/applyToAuction")
def applyToAuction(ApplyToAuction: ApplyToAuction):
    applytoauction_data = ApplyToAuction.dict()
    try:
        with engine.begin() as conn:  # ✅ use engine.begin() to auto-commit

            if applytoauction_data["applyAs"] in ["O", "PO"]:
                insert_ownership = text("""INSERT INTO team (team_auction_id, team_owner_id,team_total_value) VALUES (:f_auction_id, :f_player_id,:team_total_value)""")
                result = conn.execute(insert_ownership,  {
                        "f_auction_id": applytoauction_data["f_auction_id"],
                        "f_player_id": applytoauction_data["f_player_id"],
                        "team_total_value": applytoauction_data["team_total_value"]
                    })
                team_id = result.lastrowid
                print("team_id",team_id)
                if applytoauction_data["applyAs"] =="PO":
                    print("team_id",team_id)
                    addToTeam({
                            "f_team_id": team_id,
                            "f_player_id": applytoauction_data["f_player_id"],
                            "auction_value":0
                        })
            if applytoauction_data["applyAs"] != "O":
                insert_query = text("""
                    INSERT INTO bidding (f_auction_id, f_player_id,base_value,current_value,isauctioned)
                    VALUES (:f_auction_id, :f_player_id,:base_value,:current_value,:isauctioned)
                """)
                conn.execute(insert_query, applytoauction_data)
            
            return MasterResponse(
                    message="Successfully Applied to Auction",
                    status="200",
                    data={}
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/updateBidding/{bidding_id}")
def updateTeam(bidding_id:int,ApplyToAuction: ApplyToAuction):
    bidding_data = ApplyToAuction.dict()
    bidding_data["bidding_id"]=bidding_id
    try:
        with engine.begin() as conn:  # ✅ use engine.begin() to auto-commit
            update_query = text("""
                UPDATE bidding 
                SET base_value=:base_value, 
                    current_value=:current_value, 
                    isauctioned=:isauctioned
                WHERE bidding_id=:bidding_id
            """)
            conn.execute(update_query, bidding_data)
        return MasterResponse(
                    message="Bidding updated successfully",
                    status="200",
                    data={}
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/addToTeam")
def addToTeam(AddToTeam: AddToTeam | dict):
    addtoteam_data = AddToTeam.dict() if hasattr(AddToTeam, "dict") else AddToTeam
    try:
        with engine.begin() as conn:  # ✅ use engine.begin() to auto-commit
            insert_query = text("""
                INSERT INTO team_player (f_team_id, f_player_id,auction_value)
                VALUES (:f_team_id, :f_player_id,:auction_value)
            """)
            conn.execute(insert_query, addtoteam_data)
        return MasterResponse(
                    message="Successfully Added to Team",
                    status="200",
                    data={}
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/listActiveAuction")
def listActiveAuction():
    try:
        with engine.begin() as conn:
            select_query=text("""SELECT * FROM auction WHERE STR_TO_DATE(end_date, '%d/%m/%Y') <= CURDATE()""")
            result = conn.execute(select_query)
            rows = result.mappings().all()  # Converts to list of dicts
            data = [dict(row) for row in rows]
        return MasterResponse(
                    message="List Active Auction Successfully",
                    status="200",
                    data=data
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/listMyAuction/{user_id}")
def listMyAuction(user_id:int):
    try:
        with engine.begin() as conn:
            select_query=text("""SELECT * FROM auction WHERE auctioner_id=:user_id""")
            result = conn.execute(select_query,{"user_id": user_id})
            rows = result.mappings().all()  # Converts to list of dicts
            data = [dict(row) for row in rows]
        return MasterResponse(
                    message="List My Auction Successfully",
                    status="200",
                    data=data
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

