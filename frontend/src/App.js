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
import Editing from "./components/Editing";
import MyRequests from "./components/MyRequests";
import Footer from "./components/Footer";
import EditProfile from "./components/EditProfile";

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      recordsJS: [],
      recordsObj: [],
      is_rest: undefined,
      username: undefined,
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
                    username={this.state.username}
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
              <Route
                path={`/otp/${localStorage.getItem("hash")}`}
                element={<Otp {...this.props} />}
              />
              <Route path="/signup" element={<Signup />} />
              <Route path="/editProfile" element={<EditProfile />} />
              <Route
                path="/editing"
                element={
                  <Editing
                    apiFunc={this.apiFunc}
                    recordsJS={this.state.recordsJS}
                  />
                }
              />
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
          <Footer />
        </Router>
      </div>
    );
  }

  handler(is_rest, username) {
    this.setState({
      is_rest: is_rest,
      username: username,
    });
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
