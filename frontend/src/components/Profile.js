import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Announcement.css";
import "./Profile.css";

export default function Profile(props) {
  const token = localStorage.getItem("token");
  const navigate = useNavigate();

  useEffect(() => {
    props.apiFunc("https://95.140.148.239/user/profile/", "GET", token);
  }, [token]);

  console.log(props.recordsJS);
  return (
    <div>
      <h1 className="username">{props.recordsJS.username}</h1>
      <p className="useinfo">Руководитель: {props.recordsJS.head}</p>
      <p className="useinfo">Инн: {props.recordsJS.inn}</p>
      <p className="useinfo">ОГРН: {props.recordsJS.ogrn}</p>
      <p className="useinfo">Тел: +{props.recordsJS.phone_no}</p>
      <p className="useinfo">Email: {props.recordsJS.email}</p>
      <p className="useinfo">
        Вид деятельности:{" "}
        {props.recordsJS.is_ind_pred ? "ИП" : "Юридическое лицо"}
      </p>
      <p className="useinfo">
        Тип организации:{" "}
        {props.recordsJS.is_rest ? "Ресторан" : "Благотворительная организация"}
      </p>
      <p className="useinfo">
        Адрес регистрации: {props.recordsJS.address_fact}
      </p>
      <p className="useinfo">
        Фактический адрес: {props.recordsJS.address_reg}
      </p>
      <div className="btn3" style={{ marginTop: "15px" }}>
        <button
          className="edit"
          style={{ marginLeft: 0 }}
          onClick={() => {
            navigate("/editProfile", { replace: true });
          }}
        >
          Редактировать
        </button>
        <button
          className="delete"
          onClick={() => {
            props.apiFunc(
              `https://95.140.148.239/user/profile/`,
              "DELETE",
              token
            );
            props.logout();
            props.apiFunc(
              "https://95.140.148.239/user/auth/token/logout/",
              "POST",
              token
            );
            navigate("/login", { replace: true });
          }}
        >
          Удалить профиль
        </button>
      </div>
    </div>
  );
}
