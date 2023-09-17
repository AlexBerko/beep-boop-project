import React from "react";
import "./List.css";
import { Link } from "react-router-dom";

export default function List(props) {
  const token = localStorage.getItem("token");
  let full_info;

  if (props.recordsJS.length > 0) {
    full_info = props.recordsJS[props.arrayId].full_info.split("\r\n");
  }

  console.log(props.recordsJS);

  return (
    <div className="list">
      <h2>{props.recordsJS[props.arrayId].title}</h2>
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
      <Link to="/announcement">
        <button
          className="open"
          onClick={() => {
            props.handlerObj(props.arrayId);
            // props.apiFunc(
            //   `https://95.140.148.239/help/${
            //     props.recordsJS[props.arrayId].id
            //   }/`,
            //   "GET",
            //   token
            // );
          }}
        >
          Открыть
        </button>
      </Link>
    </div>
  );
}
