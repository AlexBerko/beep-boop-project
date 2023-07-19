import React from "react";
import "./Header.css";

export default function Header() {
  return (
    <header>
      <div className="head">
        <ul className="nav">
          <li>Главная</li>
          <li>Профиль</li>
          <li>Подать заявку</li>
        </ul>
        <ul className="login_logout">
          <li>Войти</li>
          <li>Выйти</li>
        </ul>
      </div>
    </header>
  );
}
