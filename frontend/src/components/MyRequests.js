import React, { useEffect, useState } from "react";
import "./Announcement.css";
import "./MyRequests.css";
import List from "./List";

export default function MyRequests(props) {
  const token = localStorage.getItem("token");
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    props.apiFunc("https://95.140.148.239/help/my/", "GET", token);
  }, [token]);

  console.log(props.recordsJS);

  return (
    <div className="announc">
      <h1 className="title">Ваши заявки</h1>
      <div className="completChange">
        <p
          className={`completed ${!isCompleted && "active"}`}
          onClick={setIsCompleted(false)}
        >
          В работе
        </p>
        <p
          className={`completed ${isCompleted && "active"}`}
          onClick={setIsCompleted(true)}
        >
          Завершённые
        </p>
      </div>
      {isCompleted ? (
        <span>
          {(() => {
            const options = [];

            for (let i = 0; i < props.recordsJS.length; i++) {
              if (props.recordsJS[i].is_completed) {
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
            }

            return options;
          })()}
        </span>
      ) : (
        <span>
          {(() => {
            const options = [];

            for (let i = 0; i < props.recordsJS.length; i++) {
              if (!props.recordsJS[i].is_completed) {
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
            }

            return options;
          })()}
        </span>
      )}
    </div>
  );
}
