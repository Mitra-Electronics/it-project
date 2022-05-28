from driver.jwt_driver import decode_access_token
from driver.mongodb_driver import room_create, room_get
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from game_handler import ConnectionManager
from schemas import Game, GameInfo, Token

router = APIRouter(
    prefix="/game",
    tags=["Game"],
)

@router.post("/game/verify/{room_code}")
async def verify_game(room_code: str):
    room = room_get(room_code)
    if room is None:
        return {"status":"not ok", "data":"room not found", "room_found":False}
    else:
        return {"status":"not ok", "data":"room not found", "room_found":False}

@router.post("/game/create")
def create_game(auth_token: Token, room: GameInfo):
    code = room_create(decode_access_token(auth_token.token), room)
    if code is False:
        return {"status":"not ok", "room_created":False}
    return {"status":"ok", "room_created":True, "room_code":code}

manager = ConnectionManager()

@router.websocket("/game/join/{room_code}")
async def handler(websocket: WebSocket, room_code: str):
    await manager.connect(websocket)
    room = Game(**room_get(room_code))
    if room is None:
        raise HTTPException(
            status_code=1007,
            detail="Room doesn't exist"
        )
    else:
        try:
            await manager.broadcast(room.get_dict())
            await websocket.close()
        except WebSocketDisconnect:
            await manager.disconnect(websocket) 
