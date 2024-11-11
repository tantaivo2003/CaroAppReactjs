from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List

app = FastAPI()
origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://172.24.16.1:3000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

clients: List[WebSocket] = []
board = [['*' for _ in range(20)] for _ in range(20)]
turn = True  # X goes first

def checkwinngang(xn, yn):
  xcheck = xn
  ycheck = yn
  rcheck = 0
  lcheck = 0

  while xcheck < 20:
    taocheck = board[ycheck][xcheck]
    if board[ycheck][xcheck] == board[yn][xn]:
      rcheck += 1
      xcheck += 1
    else:
      break

  xcheck=xn
  ycheck=yn

  while xcheck > -1:
    if board[ycheck][xcheck]==board[yn][xn]:
      lcheck+=1
      xcheck-=1
    else:
      break

  if lcheck > 4 or rcheck > 4 or lcheck + rcheck > 5:
    return True
  else:
    return False
  
def checkwindoc(xn,yn):
  xcheck=xn
  ycheck=yn
  topcheck=0
  botcheck=0

  while ycheck < 20:
    if board[ycheck][xcheck] == board[yn][xn]:
      topcheck+=1
      ycheck+=1
    else:
      break

  xcheck=xn
  ycheck=yn

  while ycheck>-1:
    if board[ycheck][xcheck]==board[yn][xn]:
      botcheck+=1
      ycheck-=1
    else:
      break

  if topcheck > 4 or botcheck > 4 or topcheck + botcheck > 5:
    return True
  else:
    return False
  
def checkwincheox(xn,yn):
  xcheck=xn
  ycheck=yn
  rcheck=0
  lcheck=0

  while xcheck < 20 and ycheck >- 1:
    if board[ycheck][xcheck]==board[yn][xn]:
      rcheck+=1
      xcheck+=1
      ycheck-=1
    else:
      break

  xcheck=xn
  ycheck=yn

  while xcheck > -1 and ycheck < 20:
    if board[ycheck][xcheck] == board[yn][xn]:
      lcheck+=1
      xcheck-=1
      ycheck+=1
    else:
      break

  if lcheck>4 or rcheck>4 or lcheck+rcheck>5:
    return True
  else:
    return False
  
def checkwincheol(xn,yn):
  xcheck=xn
  ycheck=yn
  rcheck=0
  lcheck=0

  while xcheck < 20 and ycheck < 20:
    if board[ycheck][xcheck]==board[yn][xn]:
      rcheck+=1
      xcheck+=1
      ycheck+=1
    else:
      break

  xcheck=xn
  ycheck=yn

  while xcheck>-1 and ycheck>-1:
    if board[ycheck][xcheck]==board[yn][xn]:
      lcheck+=1
      xcheck-=1
      ycheck-=1
    else:
      break

  if lcheck > 4 or rcheck > 4 or lcheck + rcheck > 5:
    return True
  else:
    return False
  
def checkwin(yn, xn):
  if checkwinngang(xn,yn) or checkwindoc(xn,yn) or checkwincheox(xn,yn) or checkwincheol(xn,yn):
    return True
  else:
    return False
  
def reset_board():
    global board
    board = [
        ['*' for _ in range(20)] for _ in range(20)   
    ]

@app.get("/")
async def read_root():
    return {"board": board, "turn": turn}

@app.put("/{x}/{y}/{piece}")
async def move(x: int, y: int, piece: str):
    global turn
    if board[x][y] == "*":
        board[x][y] = piece
        win = checkwin(x, y)
        turn = not turn
        return {"board": board, "win": win, "turn": turn}
    else:
        raise HTTPException(status_code=400, detail="Invalid move")

@app.put("/reset")
async def reset():
    reset_board()
    return {"board": board, "turn": turn}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                await client.send_text(data)
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)