import React from "react";
import axios from "axios";
import { LockOutlined, UserOutlined } from "@ant-design/icons";
import { Button, Form, Input, Spin } from "antd";
import { LoadingOutlined } from "@ant-design/icons";
import { connect } from "react-redux";
import { NavLink, useNavigate, useParams } from "react-router-dom";
import * as actions from "../store/actions/auth";

const antIcon = (
  <LoadingOutlined
    style={{
      fontSize: 24,
    }}
    spin
  />
);

const App = (props) => {
  const navigate = useNavigate();
  console.log(useParams());
  const { id, token } = useParams();
  console.log(id, token);

  const onFinish = (values) => {
    // console.log("Received values of form: ", values);
    props.onAuth(values.email, values.password);
    navigate("/otp", { replace: true });
  };

  let errorMessage = null;
  if (props.error) {
    errorMessage = <p>{props.error.message}</p>;
  }

  if (id !== undefined && token !== undefined) {
    axios
      .get(`http://127.0.0.1:8000/user/activate/${id}/${token}/`)
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  return (
    <div>
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
              {" "}
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
