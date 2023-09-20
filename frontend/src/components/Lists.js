import React, { useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import List from "./List";
import "./List.css";

export default function Lists(props) {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  let config = {
    headers: {
      Authorization: `Token ${token}`,
    },
  };

  // https://95.140.148.239
  // http://127.0.0.1:8000

  useEffect(() => {
    props.apiFunc("https://95.140.148.239/help/list/", "GET", token);
    axios
      .get("https://95.140.148.239/user/profile/", config)
      .then((res) => {
        const data = JSON.parse(res.data);
        props.handler(data.is_rest, data.username);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [token]);

  console.log(props.recordsJS);

  if (token === null) {
    navigate("/login", { replace: true });
  } else {
    return (
      <div className="mainpg">
        <div className="firstbaner">
          <div className="txt">
            <p className="maintxt">У вас есть больше, чем вам нужно?</p>
            <p className="secondtxt">Вы можете помочь нуждающимся!</p>
          </div>
          <div class="arrow-7">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <img
            className="baner"
            src={require("../img/baner.jpg")}
            alt={"Банер"}
          />
        </div>
        <div className="announc">
          {(() => {
            const options = [];

            for (let i = 0; i < props.recordsJS.length; i++) {
              options.push(
                <List
                  key={i}
                  arrayId={i}
                  apiFunc={props.apiFunc}
                  recordsObj={props.recordsObj}
                  recordsJS={props.recordsJS}
                />
              );
            }

            return options;
          })()}
        </div>
      </div>
    );
  }
}
