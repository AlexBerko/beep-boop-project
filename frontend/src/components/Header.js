import React from "react";
import "./Header.css";
import { Link } from "react-router-dom";

export default function Header() {
  return (
    <header>
      <div className="head">
        <ul className="nav">
          <li>
            <Link to="/" className="link">
              Главная
            </Link>
          </li>
          <li>
            <Link to="/profile" className="link">
              Профиль
            </Link>
          </li>
          <li>
            <Link to="/submit" className="link">
              Подать заявку
            </Link>
          </li>
        </ul>
        <ul className="login_logout">
          <li>
            <Link to="/signin" className="link">
              Войти
            </Link>
          </li>
          <li>Выйти</li>
        </ul>
      </div>
    </header>
  );
}
