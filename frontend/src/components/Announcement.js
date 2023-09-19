import React, { useState } from "react";
import { Modal } from "antd";
import { useNavigate } from "react-router-dom";
import "./Announcement.css";

export default function Announcement(props) {
  const navigate = useNavigate();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const token = localStorage.getItem("token");
  let datestring;
  let full_info;

  if (props.recordsJS.pub_date !== undefined) {
    datestring = `${props.recordsJS.pub_date.substr(
      8,
      2
    )}.${props.recordsJS.pub_date.substr(
      5,
      2
    )}.${props.recordsJS.pub_date.substr(
      0,
      4
    )} ${props.recordsJS.pub_date.substr(11, 8)}`;

    full_info = props.recordsJS.full_info.split("\r\n");
  }

  const handleModalOk = () => {
    setIsModalVisible(false);
    navigate("/requests", { replace: true });
  };

  console.log(props.recordsJS);
  console.log(props.recordsObj);

  if (props.recordsJS.title === undefined) {
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
            <p className="orgData">{props.recordsJS.username}</p>
            <p className="orgData">ОГРН: {props.recordsJS.ogrn}</p>
            <p className="orgData">ИНН: {props.recordsJS.inn}</p>
            <p className="orgData">Ген. директор: {props.recordsJS.head}</p>
            <p className="orgData">Email: {props.recordsJS.email}</p>
            <p className="orgData">Юр. адрес: {props.recordsJS.address_reg}</p>
            <p className="orgData">
              Факт. адрес: {props.recordsJS.address_fact}
            </p>
          </div>
        </div>
        <div className="date">
          <time>{datestring}</time>
          {props.recordsJS.who_complete_id ? (
            <p>Вы откликнулись на эту просьбу</p>
          ) : (
            <button
              className="answer"
              onClick={() => {
                props.apiFunc(
                  `https://95.140.148.239/help/${props.recordsJS.id}/`,
                  "POST",
                  token
                );
                setIsModalVisible(true);
              }}
            >
              Откликнуться
            </button>
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
