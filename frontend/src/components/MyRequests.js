import React, { useEffect } from "react";
import "./Announcement.css";
import List from "./List";

export default function MyRequests(props) {
  const token = localStorage.getItem("token");

  useEffect(() => {
    props.apiFunc("https://95.140.148.239/help/my/", "GET", token);
  }, [token]);

  console.log(props.recordsJS);

  return (
    <div className="announc">
      <h1 className="title">Ваши заявки</h1>
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
              handler={props.handler}
              handlerObj={props.handlerObj}
            />
          );
        }

        return options;
      })()}
    </div>
  );
}
