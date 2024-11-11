import React from 'react';
import Board from './components/Board';
import { BoardProvider } from './BoardContext';
export default function App() {
  return (
    <BoardProvider >
      <h1 className="text-3xl font-bold underline">Caro Tài Dõ</h1>
      <div className="text-center mt-10">
      <Board />
      </div>

    </BoardProvider>
  );
}