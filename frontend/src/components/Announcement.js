import React from "react";
import "./Announcement.css";

export default function Announcement(props) {
  let datestring;
  let full_info;

  if (props.recordsObj.pub_date !== undefined) {
    datestring = `${props.recordsObj.pub_date.substr(
      8,
      2
    )}.${props.recordsObj.pub_date.substr(
      5,
      2
    )}.${props.recordsObj.pub_date.substr(
      0,
      4
    )} ${props.recordsObj.pub_date.substr(11, 8)}`;

    full_info = props.recordsObj.full_info.split("\r\n");
  }

  console.log(props.recordsJS);
  console.log(props.recordsObj);

  if (
    props.recordsObj.title === undefined ||
    props.recordsJS.data === undefined
  ) {
    return <div className="loading">Loading...</div>;
  } else {
    return (
      <div className="container">
        <h1 className="title">{props.recordsObj.title}</h1>
        <div className="main">
          <div className="text_block">
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
          </div>
          <div className="org_info">
            <h2 className="second_block">Данные о компании</h2>
            <p className="orgData">
              {props.recordsJS.data.data.Записи[0].НаимПолн}
            </p>
            <p className="orgData">
              ОГРН: {props.recordsJS.data.data.Записи[0].ОГРН}
            </p>
            <p className="orgData">
              {props.recordsJS.data.data.Записи[0].ОКВЭД}
            </p>
            <p className="orgData">
              Статус: {props.recordsJS.data.data.Записи[0].Статус}
            </p>
            <p className="orgData">
              {props.recordsJS.data.data.Записи[0].Руковод[0].НаимДолжн}:{" "}
              {props.recordsJS.data.data.Записи[0].Руковод[0].ФИО}
            </p>
            <p className="orgData">
              Юр. адрес: {props.recordsJS.data.data.Записи[0].ЮрАдрес}
            </p>
          </div>
        </div>
        <div className="date">
          <time>{datestring}</time>
          <button className="answer">Откликнуться</button>
        </div>
      </div>
    );
  }
}
