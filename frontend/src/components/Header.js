import React from "react";
import "./Header.css";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import * as actions from "../store/actions/auth";

function Header(props) {
  const token = localStorage.getItem("token");

  return (
    <header>
      <div className="head">
        {props.isAuthenticated ? (
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
            {props.is_rest ? (
              <span></span>
            ) : (
              <li>
                <Link to="/submit" className="link">
                  Подать заявку
                </Link>
              </li>
            )}
            <li>
              <Link to="/requests" className="link">
                Мои заявки
              </Link>
            </li>
          </ul>
        ) : (
          <ul></ul>
        )}
        <ul className="login_logout">
          {props.isAuthenticated ? (
            <li>
              <Link
                className="link"
                onClick={() => {
                  props.logout();
                  props.apiFunc(
                    "https://95.140.148.239/user/auth/token/logout/",
                    "POST",
                    token
                  );
                }}
                to="/login"
              >
                Выйти
              </Link>
            </li>
          ) : (
            <li>
              <Link to="/login" className="link">
                Войти
              </Link>
            </li>
          )}
        </ul>
      </div>
    </header>
  );
}

const mapDispatchToProps = (dispatch) => {
  return {
    logout: () => dispatch(actions.logout()),
  };
};

export default connect(null, mapDispatchToProps)(Header);
