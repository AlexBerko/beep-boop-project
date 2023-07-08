import React, { Component } from "react";

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      records: [],
      simpleText: "simple Text",
    };

    this.apiFunc = this.apiFunc.bind(this);
  }

  render() {
    return (
      <div>
        {this.state.records}
        <button
          onClick={() => {
            this.apiFunc();
          }}
        >
          Проверка api
        </button>
      </div>
    );
  }

  apiFunc() {
    let requestOptions;

    requestOptions = {
      method: "GET",
      mode: "no-cors",
    };

    fetch(`http://127.0.0.1:8000/main/`, requestOptions)
      .then((response) => response.json())
      .then((records) => {
        this.setState({
          records: records,
        });
      })
      .catch((error) => console.log(error));

    console.log(this.state.records);
    return this.state.records;
  }
}

export default App;
