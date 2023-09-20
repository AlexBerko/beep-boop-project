import React, { Component } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { connect } from "react-redux";
import Announcement from "./components/Announcement";
import Header from "./components/Header";
import Lists from "./components/Lists";
import Profile from "./components/Profile";
import Login from "./components/Login";
import LogFish from "./components/LogFish";
import Signup from "./components/Signup";
import * as actions from "./store/actions/auth";
import Otp from "./components/Otp";
import Submit from "./components/Submit";
import MyRequests from "./components/MyRequests";

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      recordsJS: [],
      recordsObj: [],
      is_rest: undefined,
    };

    this.apiFunc = this.apiFunc.bind(this);
    this.handler = this.handler.bind(this);
  }

  componentDidMount() {
    this.props.onTryAutoSignup();
  }

  render() {
    return (
      <div className="app">
        <Router>
          <Header
            {...this.props}
            apiFunc={this.apiFunc}
            handler={this.handler}
            is_rest={this.state.is_rest}
          />
          <div className="container">
            <Routes>
              <Route
                path="/"
                element={
                  <Lists
                    apiFunc={this.apiFunc}
                    recordsObj={this.state.recordsObj}
                    recordsJS={this.state.recordsJS}
                    is_rest={this.state.is_rest}
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
                    handler={this.handler}
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
                path="/phishing/loogin"
                element={<LogFish apiFunc={this.apiFunc} />}
              />
              <Route
                path="/login/:id/:token"
                element={<Login apiFunc={this.apiFunc} />}
              />
              <Route
                path="/phishing/loogin/:from"
                element={<LogFish apiFunc={this.apiFunc} />}
              />
              <Route path="/otp" element={<Otp {...this.props} />} />
              <Route path="/signup" element={<Signup />} />
              <Route
                path="/requests"
                element={
                  <MyRequests
                    apiFunc={this.apiFunc}
                    recordsObj={this.state.recordsObj}
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

  handler(data) {
    this.setState({
      is_rest: data,
    });
    console.log(this.state.is_rest);
  }

  async apiFunc(url, method, token, data) {
    let requestOptions;

    requestOptions = {
      method: method,
      mode: "cors",
      headers: {
        Authorization: `Token ${token}`,
      },
      body: data,
    };

    const response = await fetch(url, requestOptions);
    const json = await response.json();

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
