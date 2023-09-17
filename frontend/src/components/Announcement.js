import React, { useState, useEffect } from "react";
import axios from "axios";
import { Modal } from "antd";
import { useNavigate } from "react-router-dom";
import "./Announcement.css";

export default function Announcement(props) {
  const navigate = useNavigate();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const token = localStorage.getItem("token");
  let datestring;
  let full_info;

  useEffect(() => {
    props.apiFunc("https://95.140.148.239/user/profile/", "GET", token);
  }, [token]);

  if (props.recordsJS.username !== undefined) {
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
  }

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

  const handleModalOk = () => {
    setIsModalVisible(false);
    navigate("/requests", { replace: true });
  };

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
              {props.recordsJS.data.data.Записи[0].НаимПолн
                ? props.recordsJS.data.data.Записи[0].НаимПолн
                : props.recordsJS.data.data.Записи[0].Тип}
            </p>
            <p className="orgData">
              ОГРН:{" "}
              {props.recordsJS.data.data.Записи[0].ОГРН
                ? props.recordsJS.data.data.Записи[0].ОГРН
                : props.recordsJS.data.data.Записи[0].ОГРНИП}
            </p>
            <p className="orgData">
              ОКВЭД: {props.recordsJS.data.data.Записи[0].ОКВЭД}
            </p>
            <p className="orgData">
              Статус: {props.recordsJS.data.data.Записи[0].Статус}
            </p>
            <p className="orgData">
              {props.recordsJS.data.data.Записи[0].ОГРН
                ? "Директор: "
                : "ФИО: "}
              :{" "}
              {props.recordsJS.data.data.Записи[0].ОГРН
                ? props.recordsJS.data.data.Записи[0].Руковод[0].ФИО
                : props.recordsJS.data.data.Записи[0].ФИО}
            </p>
            <p className="orgData">
              Юр. адрес:{" "}
              {props.recordsJS.data.data.Записи[0].ЮрАдрес
                ? props.recordsJS.data.data.Записи[0].ЮрАдрес
                : "-"}
            </p>
          </div>
        </div>
        <div className="date">
          <time>{datestring}</time>
          {props.recordsObj.who_complete_id ? (
            <button
              className="answer"
              onClick={() => {
                props.apiFunc(
                  `https://95.140.148.239/help/${props.recordsObj.id}/`,
                  "POST",
                  token
                );
                setIsModalVisible(true);
              }}
            >
              Откликнуться
            </button>
          ) : (
            <p>Вы откликнулись на эту просьбу</p>
          )}
          <Modal
            title="Спасибо!"
            visible={isModalVisible}
            onOk={handleModalOk}
            closable={false}
            maskClosable={false}
            onCancel={handleModalOk}
          >
            <p>Вы откликнулись на просьбу</p>
          </Modal>
        </div>
      </div>
    );
  }
}
