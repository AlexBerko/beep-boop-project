import React, { Component } from "react";
import List from "./List";

class Lists extends Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  componentDidMount() {
    const token = localStorage.getItem("token");
    this.props.apiFunc("http://127.0.0.1:8000//help/list/", "GET", token);
  }

  render() {
    return (
      <div>
        {(() => {
          const options = [];

          for (let i = 0; i < this.props.recordsObj.length; i++) {
            options.push(
              <List
                key={i}
                arrayId={i}
                apiFunc={this.props.apiFunc}
                recordsObj={this.props.recordsObj}
                handler={this.props.handler}
              />
            );
          }

          return options;
        })()}
      </div>
    );
  }
}

export default Lists;
