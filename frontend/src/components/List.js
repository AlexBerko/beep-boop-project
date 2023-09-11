import React, { useEffect } from "react";
import axios from "axios";
import "./List.css";
import { Link } from "react-router-dom";

export default function List(props) {
  const token = localStorage.getItem("token");
  let full_info;

  if (props.recordsObj.length > 0) {
    full_info = props.recordsObj[props.arrayId].full_info.split("\r\n");
  }

  useEffect(() => {
    props.apiFunc("http://berkoaqg.beget.tech/user/profile/", "GET", token);
  }, [token]);

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
      <Link to="/announcement">
        <button
          className="open"
          onClick={() => {
            props.apiFunc(
              `http://berkoaqg.beget.tech/help/${
                props.recordsObj[props.arrayId].id
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
