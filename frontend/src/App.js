import React, { Component } from "react";
import Announcement from "./components/Announcement";

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      flag: false,
      records: [],
    };

    this.apiFunc = this.apiFunc.bind(this);
    this.onBtn = this.onBtn.bind(this);
  }

  render() {
    return (
      <div className="container">
        {!this.state.flag && (
          <div>
            <p>Это страница со списком всех просьб</p>
            <button
              onClick={() => {
                this.onBtn();
                this.apiFunc();
              }}
            >
              Перейти к конкретному объявлению
            </button>
          </div>
        )}
        {this.state.flag && (
          <Announcement apiFunc={this.apiFunc} records={this.state.records} />
        )}
      </div>
    );
  }

  onBtn() {
    this.setState({ flag: !this.state.flag });
  }

  async apiFunc() {
    let requestOptions;

    requestOptions = {
      method: "GET",
    };

    const response = await fetch(
      `http://127.0.0.1:8000/help/2/`,
      requestOptions
    );
    const json = await response.json();
    console.log(JSON.parse(json));
    this.setState({
      records: JSON.parse(json),
    });
    return json;
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
