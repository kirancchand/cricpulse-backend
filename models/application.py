from pydantic import BaseModel
from typing import List, Dict, Any,Optional

class AuctionRegister(BaseModel):
    auction_name: str
    auctioner_id: int
    noofteams: int
    noofplayers: int
    start_date: str
    end_date: str
    venue: str
    budget_per_team: int
    bid_increment: int
    base_value: int
    status:str

class TeamRegister(BaseModel):
    team_auction_id:Optional[int] = None
    team_name:str
    team_owner_id:int
    team_total_value:Optional[int] = None
    team_balance_value:int

class ApplyToAuction(BaseModel):
    f_auction_id:Optional[int] = None
    f_player_id:Optional[int] = None
    base_value:int
    current_value:int
    isauctioned:bool = False
    team_total_value:int
    applyAs:str

class AddToTeam(BaseModel):
    f_team_id:int
    f_player_id:int
    auction_value:int