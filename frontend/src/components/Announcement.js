import React from "react";
import "./Announcement.css";

export default function Announcement(props) {
  let datestring;
  let full_info;

  if (props.recordsJS.pubdate !== undefined) {
    datestring = `${props.recordsJS.pubdate.substr(
      8,
      2
    )}.${props.recordsJS.pubdate.substr(5, 2)}.${props.recordsJS.pubdate.substr(
      0,
      4
    )} ${props.recordsJS.pubdate.substr(11, 8)}`;

    full_info = props.recordsJS.full_info.split("\r\n");
  }

  if (
    props.recordsJS.title === undefined ||
    props.recordsObj.data === undefined
  ) {
    return <div className="loading">Loading...</div>;
  } else {
    return (
      <div className="container">
        <h1 className="title">{props.recordsJS.title}</h1>
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
              {props.recordsObj.data.Записи[0].НаимПолн}
            </p>
            <p className="orgData">
              ОГРН: {props.recordsObj.data.Записи[0].ОГРН}
            </p>
            <p className="orgData">{props.recordsObj.data.Записи[0].ОКВЭД}</p>
            <p className="orgData">
              Статус: {props.recordsObj.data.Записи[0].Статус}
            </p>
            <p className="orgData">
              {props.recordsObj.data.Записи[0].Руковод[0].НаимДолжн}:{" "}
              {props.recordsObj.data.Записи[0].Руковод[0].ФИО}
            </p>
            <p className="orgData">
              Юр. адрес: {props.recordsObj.data.Записи[0].ЮрАдрес}
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
