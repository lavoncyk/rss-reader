import React from "react";

import Board from "./components/Board";
import './App.css'

class App extends React.Component {

  render() {
    return (
      <div className="App">
        <div className="menu">
          <div className="menu-logo">
            <a href="/">NewsTerminal</a>
          </div>
          <div className="menu-center"></div>
          <div className="menu-theme-switcher"></div>
        </div>
        <Board />
      </div>
    );
  }

}

export default App