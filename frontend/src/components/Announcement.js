import React from "react";
import "./Announcement.css";

export default function Announcement(props) {
  let datestring;
  let full_info;
  if (props.records.pubdate !== undefined) {
    datestring = `${props.records.pubdate.substr(
      8,
      2
    )}.${props.records.pubdate.substr(5, 2)}.${props.records.pubdate.substr(
      0,
      4
    )} ${props.records.pubdate.substr(11, 8)}`;

    full_info = props.records.full_info.split("\r\n");
  }

  if (props.records.title === undefined) {
    return <div className="loading">Loading...</div>;
  } else {
    return (
      <div className="container">
        <h1 className="title">{props.records.title}</h1>
        {(() => {
          const options = [];

          for (let i = 0; i < full_info.length; i++) {
            options.push(
              <p key={i} className="info">
                {full_info[i]}
              </p>
            );
          }

          return options;
        })()}
        <div className="date">
          <time>{datestring}</time>
          <button className="answer">Откликнуться</button>
        </div>
      </div>
    );
  }
}
