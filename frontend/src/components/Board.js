import React, { useState, useEffect } from 'react';
import { useBoard } from '../BoardContext';
import Square from './Square';
import XSquare from './XSquare';
import OSquare from './OSquare';

function resolveIndex(id) {
  var i = Math.floor(id / 20);  // Chỉ số hàng
  var j = id % 20;              // Chỉ số cột
  return { i: i, j: j };
}

//const ip = '172.24.16.1'
export default function Board() {
  const { board, setBoard } = useBoard();
  const [turn, setTurn] = useState(true); 
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    fetchBoard();

    
    const newSocket = new WebSocket(`ws://localhost:8000/ws`);
    newSocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setBoard(data.board);
      setTurn(data.turn);
      if (data.win) {
        alert(`Player ${data.piece} wins!`);
      }
    };
    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  const fetchBoard = async () => {
    try {
      const response = await fetch(`http://localhost:8000/`);
      if (!response.ok) {
        throw new Error('Error fetching board');
      }
      const data = await response.json();
      setBoard(data.board);
      setTurn(data.turn);
    } catch (error) {
      console.error('Error fetching board:', error);
    }
  };

  function handleMove(event) {
    const id = parseInt(event.target.id);
    const { i, j } = resolveIndex(id);

    let piece = turn ? "X" : "O";

    executeMove(i, j, piece);
  }

  const executeMove = async (i, j, piece) => {
    try {
      const response = await fetch(`http://localhost:8000/${i}/${j}/${piece}`, {
        method: 'PUT',
      });
      if (!response.ok) {
        throw new Error('Error executing move');
      }
      const { win, board: updatedBoard, turn: newTurn } = await response.json();
      setBoard(updatedBoard);
      setTurn(newTurn);
      if (socket) {
        socket.send(JSON.stringify({ board: updatedBoard, win, piece, turn: newTurn }));
      }
    } catch (error) {
      console.error('Error executing move:', error);
    }
  };

  const reSetBoard = async () => {
    try {
      const response = await fetch(`http://localhost:8000/reset`, {
        method: 'PUT',
      });
      if (!response.ok) {
        throw new Error('Error resetting board');
      }
      const data = await response.json();
      setBoard(data.board);
      setTurn(data.turn);
      if (socket) {
        socket.send(JSON.stringify({ board: data.board, win: false, turn: data.turn }));
      }
    } catch (error) {
      console.error('Error resetting board:', error);
    }
  };

  if (!board || board.length === 0) {
    return <div>Loading...</div>;
  }

  const rows = board.length;
  const cols = board[0].length;

  const tableRows = [];

  let id = 0;
  for (let rowIndex = 0; rowIndex < rows; rowIndex++) {
    const rowCols = [];
    for (let colIndex = 0; colIndex < cols; colIndex++) {
      let PrintComponent;
      let hoverStr;
      if (board[rowIndex][colIndex] === '*') {
        PrintComponent = Square;
        hoverStr = "hover:bg-sky-300";
      } else if (board[rowIndex][colIndex] === 'X') {
        PrintComponent = XSquare;
        hoverStr = "hover:bg-red-300";
      } else {
        PrintComponent = OSquare;
        hoverStr = "hover:bg-green-300";
      }

      rowCols.push(
        <td key={id} className={`mx-auto mt-8 border-solid border-2 border-indigo-600 h-35px w-32px ${hoverStr}`} id={id} onClick={handleMove}>
          <PrintComponent />
        </td>
      );
      id++;
    }
    tableRows.push(<tr key={rowIndex}>{rowCols}</tr>);
  }

  return (
    <div className="game">
      <div className="info">
        <div className="m-10">Current Turn: {turn ? <XSquare /> : <OSquare />}</div>
        <button onClick={reSetBoard} type="button" className="focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800">Start New Game</button>
      </div>
      <table className="mx-auto mt-8 border-solid border-2 border-indigo-600">
        <tbody>
          {tableRows}
        </tbody>
      </table>
    </div>
  );
}
