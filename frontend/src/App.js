import React, { Component } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Announcement from "./components/Announcement";
import Header from "./components/Header";
import Lists from "./components/Lists";
import Profile from "./components/Profile";

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      recordsJS: [],
      recordsObj: [],
    };

    this.apiFunc = this.apiFunc.bind(this);
  }

  render() {
    return (
      <div className="App">
        <Router>
          <Header />
          <div className="container">
            <Routes>
              <Route
                path="/"
                element={
                  <Lists
                    apiFunc={this.apiFunc}
                    recordsObj={this.state.recordsObj}
                    changeId={this.changeId}
                  />
                }
              />
              <Route
                path="/announcement"
                element={
                  <Announcement
                    apiFunc={this.apiFunc}
                    recordsJS={this.state.recordsJS}
                    recordsObj={this.state.recordsObj}
                    id={this.state.id}
                  />
                }
              />
              <Route
                path="/profile"
                element={
                  <Profile
                    apiFunc={this.apiFunc}
                    recordsJS={this.state.recordsJS}
                  />
                }
              />
            </Routes>
          </div>
        </Router>
      </div>
    );
  }

  async apiFunc(url, method) {
    let requestOptions;

    requestOptions = {
      method: method,
    };

    const response = await fetch(url, requestOptions);
    const json = await response.json();
    console.log(json);

    if (typeof json === "string") {
      this.setState({
        recordsJS: JSON.parse(json),
      });
      return JSON.parse(json);
    } else {
      this.setState({
        recordsObj: json,
      });
      return json;
    }
  }
}

export default App;
