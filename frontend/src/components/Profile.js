import React, { useEffect } from "react";

export default function Profile(props) {
  const token = localStorage.getItem("token");

  useEffect(() => {
    props.apiFunc("http://127.0.0.1:8000/user/profile/", "GET", token);
  }, [token]);

  console.log(props.recordsJS);
  return (
    <div>
      <h1>{props.recordsJS.username}</h1>
      <p>Руководитель: {props.recordsJS.head}</p>
      <p>Инн: {props.recordsJS.inn}</p>
      <p>ОГРН: {props.recordsJS.ogrn}</p>
      <p>Тел: +{props.recordsJS.phone_no}</p>
      <p>Email: {props.recordsJS.email}</p>
      <p>
        Вид деятельности:{" "}
        {props.recordsJS.is_ind_pred ? <p>ИП</p> : <p>Юридическое лицо</p>}
      </p>
      <p>
        Тип организации:{" "}
        {props.recordsJS.is_rest ? (
          <p>Ресторан</p>
        ) : (
          <p>Благотворительная организация</p>
        )}
      </p>
      <p>Адрес регистрации: {props.recordsJS.address_fact}</p>
      <p>Фактический адрес: {props.recordsJS.address_reg}</p>
    </div>
  );
}
