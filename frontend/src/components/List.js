import React from "react";
import "./List.css";

export default function List(props) {
  let full_info;

  if (props.recordsObj.length > 0) {
    full_info = props.recordsObj[props.arrayId].full_info.split("\r\n");
  }

  return (
    <div className="list">
      <h2>{props.recordsObj[props.arrayId].title}</h2>
      <div className="summary">
        {(() => {
          const options = [];

          for (let i = 0; i < full_info.length; i++) {
            options.push(
              <p key={i} className="sum_info">
                {full_info[i]}
              </p>
            );
          }

          return options;
        })()}
      </div>
      <button
        className="open"
        onClick={() => {
          props.onBtn();
          props.apiFunc(
            `http://127.0.0.1:8000/help/${props.recordsObj[props.arrayId].id}/`,
            "GET"
          );
          props.apiFunc(
            "https://api.checko.ru/v2/search?key=CAYR4QAsioUmKS5o&by=name&obj=org&query=ПАО Ростелеком&limit=1",
            "GET"
          );
        }}
      >
        Открыть
      </button>
    </div>
  );
}
