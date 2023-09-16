import React, { useEffect } from "react";
import axios from "axios";
import "./List.css";
import { Link } from "react-router-dom";

export default function List(props) {
  const token = localStorage.getItem("token");
  let full_info;

  if (props.recordsJS.length > 0) {
    full_info = props.recordsJS[props.arrayId].full_info.split("\r\n");
  }

  useEffect(() => {
    props.apiFunc("https://95.140.148.239/user/profile/", "GET", token);
  }, [token]);

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
            props.apiFunc(
              `https://95.140.148.239/help/${
                props.recordsJS[props.arrayId].id
              }/`,
              "GET",
              token
            );
            axios
              .get(
                `https://api.checko.ru/v2/search?key=CAYR4QAsioUmKS5o&by=name&obj=${
                  props.recordsJS.is_ind_pred ? "ent" : "org"
                }&query=${props.recordsJS.username}&limit=1/`
              )
              .then((res) => {
                console.log(res);
                props.handler(res);
              })
              .catch((err) => {
                console.log(err);
              });
          }}
        >
          Открыть
        </button>
      </Link>
    </div>
  );
}
