import React, { Component } from "react";
import Announcement from "./components/Announcement";
import Header from "./components/Header";
import List from "./components/List";

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      flag: false,
      recordsJS: [],
      recordsObj: [],
      list: [],
    };

    this.apiFunc = this.apiFunc.bind(this);
    this.onBtn = this.onBtn.bind(this);
  }

  componentDidMount() {
    this.apiFunc("http://127.0.0.1:8000/list/", "GET");
  }

  render() {
    return (
      <div>
        <Header />
        <div className="container">
          {!this.state.flag &&
            (() => {
              const options = [];

              console.log(this.state.recordsJS);

              for (let i = 0; i < this.state.recordsJS.length; i++) {
                options.push(
                  <List key={i} apiFunc={this.apiFunc} onBtn={this.onBtn} />
                );
              }

              return options;
            })()}
          {this.state.flag && (
            <Announcement
              apiFunc={this.apiFunc}
              recordsJS={this.state.recordsJS}
              recordsObj={this.state.recordsObj}
            />
          )}
        </div>
      </div>
    );
  }

  onBtn() {
    this.setState({ flag: !this.state.flag });
  }

  async apiFunc(url, method) {
    let requestOptions;

    requestOptions = {
      method: method,
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

  // apiFunc() {
  //   let requestOptions;

  //   requestOptions = {
  //     method: "GET",
  //   };

  //   fetch(`http://127.0.0.1:8000/help/2/`, requestOptions)
  //     .then((response) => response.json())
  //     .then((records) => {
  //       this.setState({
  //         records: records,
  //       });
  //       console.log(records);
  //     })
  //     .catch((error) => console.log(error));

  //   return this.state.records;
  // }
}

export default App;
