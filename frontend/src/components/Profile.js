import React, { useEffect } from "react";
import "./Profile.css";

export default function Profile(props) {
  const token = localStorage.getItem("token");

  useEffect(() => {
    props.apiFunc("http://berkoaqg.beget.tech/user/profile/", "GET", token);
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
    </div>
  );
}
