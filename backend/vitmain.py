from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

board = [
    ['*' for _ in range(20)] for _ in range(20)   
]
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
  
#return the board
@app.get("/")
async def read_root():
    return board

@app.put("//{x}/{y}/{piece}")
async def move(x: int, y: int, piece):
   if board[x][y] == "*":
        board[x][y] = piece
        if checkwin(x, y):
            return {"win": (board, True)}
        return {"win": (board, False)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)