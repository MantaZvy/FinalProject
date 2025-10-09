import { useState } from "react";
import React from "react";
import "./App.css";
import DataResponseList from "./components/DataResponse";

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Data Management App</h1>
      </header>
      <main>
        <DataResponseList />
      </main>
    </div>
  );
};

export default App;
