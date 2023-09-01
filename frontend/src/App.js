import React, { Component } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { connect } from "react-redux";
import Announcement from "./components/Announcement";
import Header from "./components/Header";
import Lists from "./components/Lists";
import Profile from "./components/Profile";
import Login from "./components/Login";
import Signup from "./components/Signup";
import * as actions from "./store/actions/auth";
import Otp from "./components/Otp";
import Submit from "./components/Submit";

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      recordsJS: [],
      recordsObj: [],
    };

    this.apiFunc = this.apiFunc.bind(this);
    this.handler = this.handler.bind(this);
  }

  componentDidMount() {
    this.props.onTryAutoSignup();
  }

  render() {
    return (
      <div className="App">
        <Router>
          <Header {...this.props} apiFunc={this.apiFunc} />
          <div className="container">
            <Routes>
              <Route
                path="/"
                element={
                  <Lists
                    apiFunc={this.apiFunc}
                    recordsObj={this.state.recordsObj}
                    changeId={this.changeId}
                    handler={this.handler}
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
              <Route
                path="/submit"
                element={<Submit apiFunc={this.apiFunc} />}
              />
              <Route path="/login" element={<Login apiFunc={this.apiFunc} />} />
              <Route
                path="/login/:id/:token"
                element={<Login apiFunc={this.apiFunc} />}
              />
              <Route path="/otp" element={<Otp {...this.props} />} />
              <Route path="/signup" element={<Signup />} />
            </Routes>
          </div>
        </Router>
      </div>
    );
  }

  handler(res) {
    this.setState({
      recordsJS: res,
    });
  }

  async apiFunc(url, method, token, data) {
    let requestOptions;

    requestOptions = {
      method: method,
      headers: {
        Authorization: `Token ${token}`,
      },
      body: data,
    };

    const response = await fetch(url, requestOptions);
    const json = await response.json();
    // console.log(json);

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

const mapStateToProps = (state) => {
  return {
    isAuthenticated: state.token !== null,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onTryAutoSignup: () => dispatch(actions.authCheckState()),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(App);
