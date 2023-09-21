import React, { useState } from "react";
import axios from "axios";
import { Modal } from "antd";
import { useNavigate } from "react-router-dom";
import "./Announcement.css";

export default function Announcement(props) {
  const navigate = useNavigate();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const token = localStorage.getItem("token");
  let config = {
    headers: {
      Authorization: `Token ${token}`,
    },
  };
  let datestring;
  let full_info;
  let who_complete_data;

  if (props.recordsJS.who_complete_id) {
    axios
      .get(
        `https://95.140.148.239/user/${props.recordsJS.who_complete_id}/`,
        config
      )
      .then((res) => {
        who_complete_data = JSON.parse(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  if (props.recordsJS.deadline_date !== undefined) {
    datestring = `${props.recordsJS.deadline_date.substr(
      8,
      2
    )}.${props.recordsJS.deadline_date.substr(
      5,
      2
    )}.${props.recordsJS.deadline_date.substr(
      0,
      4
    )} ${props.recordsJS.deadline_date.substr(11, 8)}`;

    full_info = props.recordsJS.full_info.split("\r\n");
  }

  const handleModalOk = () => {
    setIsModalVisible(false);
    navigate("/requests", { replace: true });
  };

  console.log(props.recordsJS);

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
          <div>
            <p className="date_time">Срок выполнения:</p>
            <time>{datestring}</time>
          </div>
          {props.recordsJS.who_complete_id ? (
            <span>
              {props.recordsJS.username === props.username ? (
                <div className="btn3">
                  <button
                    className="answer"
                    onClick={() => {
                      props.apiFunc(
                        `https://95.140.148.239/help/${props.recordsJS.id}/`,
                        "POST",
                        token
                      );
                      navigate("/requests", { replace: true });
                    }}
                  >
                    Завершить
                  </button>
                  <button
                    className="edit"
                    onClick={() => {
                      navigate("/editing", { replace: true });
                    }}
                  >
                    Редактировать
                  </button>
                  <button
                    className="delete"
                    onClick={() => {
                      props.apiFunc(
                        `https://95.140.148.239/help/${props.recordsJS.id}/`,
                        "DELETE",
                        token
                      );
                      navigate("/requests", { replace: true });
                    }}
                  >
                    Удалить
                  </button>
                </div>
              ) : (
                <div className="btn">
                  <p className="anstxt">Вы откликнулись на эту просьбу</p>
                  <button
                    className="delete"
                    onClick={() => {
                      props.apiFunc(
                        `https://95.140.148.239/help/${props.recordsJS.id}/`,
                        "DELETE",
                        token
                      );
                      navigate("/requests", { replace: true });
                    }}
                  >
                    Отказаться
                  </button>
                </div>
              )}
            </span>
          ) : (
            <span>
              {props.recordsJS.username === props.username ? (
                <div className="btn3">
                  <button
                    className="answer"
                    onClick={() => {
                      props.apiFunc(
                        `https://95.140.148.239/help/${props.recordsJS.id}/`,
                        "POST",
                        token
                      );
                      navigate("/requests", { replace: true });
                    }}
                  >
                    Завершить
                  </button>
                  <button
                    className="edit"
                    onClick={() => {
                      navigate("/editing", { replace: true });
                    }}
                  >
                    Редактировать
                  </button>
                  <button
                    className="delete"
                    onClick={() => {
                      props.apiFunc(
                        `https://95.140.148.239/help/${props.recordsJS.id}/`,
                        "DELETE",
                        token
                      );
                      navigate("/requests", { replace: true });
                    }}
                  >
                    Удалить
                  </button>
                </div>
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
            </span>
          )}
        </div>
        <div className="answer_info">
          {props.recordsJS.username === props.username &&
          props.recordsJS.who_complete_id ? (
            <div>
              <p style={{ marginTop: "40px", fontWeight: "400" }}>
                На вашу просьбу откликнулись
              </p>
              <div className="org_info_2">
                <div>
                  <p className="orgData">{who_complete_data.username}</p>
                  <p className="orgData">ОГРН: {who_complete_data.ogrn}</p>
                  <p className="orgData">ИНН: {who_complete_data.inn}</p>
                </div>
                <div>
                  <p className="orgData">
                    Ген. директор: {who_complete_data.head}
                  </p>
                  <p className="orgData">Email: {who_complete_data.email}</p>
                  <p className="orgData">Тел: {who_complete_data.phone_no}</p>
                </div>
              </div>
            </div>
          ) : (
            <span></span>
          )}
        </div>
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
    );
  }
}
