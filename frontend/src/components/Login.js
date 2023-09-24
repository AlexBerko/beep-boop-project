import React from "react";
import axios from "axios";
import { LockOutlined, UserOutlined } from "@ant-design/icons";
import { Button, Form, Input, Spin } from "antd";
import { LoadingOutlined } from "@ant-design/icons";
import { connect } from "react-redux";
import { NavLink, useParams } from "react-router-dom";
import * as actions from "../store/actions/auth";
import "./Login.css";

const antIcon = (
  <LoadingOutlined
    style={{
      fontSize: 24,
    }}
    spin
  />
);

const App = (props) => {
  console.log(useParams());
  const { id, token } = useParams();
  console.log(id, token);

  const onFinish = (values) => {
    props.onAuth(values.email, values.password);
  };

  let errorMessage = null;
  if (props.error) {
    console.log(props.error);
    console.log(props.error.response.data.error);
    errorMessage = <p>{props.error.message}</p>;
  }

  if (id !== undefined && token !== undefined) {
    axios
      .get(`https://95.140.148.239/user/activate/${id}/${token}/`)
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  return (
    <div className="login">
      {errorMessage}
      {props.regDone &&
        "На почту отправлено письмо для подтверждения регистрации!"}

      {props.loading ? (
        <Spin indicator={antIcon} />
      ) : (
        <Form
          name="normal_login"
          className="login-form"
          initialValues={{
            remember: true,
          }}
          onFinish={onFinish}
        >
          <Form.Item
            name="email"
            rules={[
              {
                type: "email",
                message: "The input is not valid E-mail!",
              },
              {
                required: true,
                message: "Please input your E-mail!",
              },
            ]}
          >
            <Input
              prefix={<UserOutlined className="site-form-item-icon" />}
              placeholder="Email"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[
              {
                required: true,
                message: "Please input your Password!",
              },
            ]}
          >
            <Input
              prefix={<LockOutlined className="site-form-item-icon" />}
              type="password"
              placeholder="Password"
              autoComplete="off"
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              style={{ marginRight: "10px" }}
            >
              Войти
            </Button>
            Или
            <NavLink style={{ marginRight: "10px" }} to="/signup/">
              {"  "}
              Зарегистрироваться
            </NavLink>
          </Form.Item>
        </Form>
      )}
    </div>
  );
};

const mapStateToProps = (state) => {
  return {
    loading: state.loading,
    regDone: state.regDone,
    error: state.error,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onAuth: (email, password) => dispatch(actions.authLogin(email, password)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(App);
