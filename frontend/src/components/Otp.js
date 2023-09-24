import React from "react";
import { Button, Form, Input, Spin } from "antd";
import { LoadingOutlined } from "@ant-design/icons";
import { connect } from "react-redux";
import { NavLink } from "react-router-dom";
import * as actions from "../store/actions/auth";
import "./Otp.css";

const antIcon = (
  <LoadingOutlined
    style={{
      fontSize: 24,
    }}
    spin
  />
);

const App = (props) => {
  const onFinish = (values) => {
    console.log("Received values of form: ", values);
    props.onAuth(values.otp);
  };

  let errorMessage = null;
  if (props.error) {
    errorMessage = <p>{props.error.message}</p>;
  }

  return (
    <div className="otp">
      {errorMessage}
      <p>Двухфакторная аутентификация</p>
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
            name="otp"
            rules={[
              {
                required: true,
                message: "Please input your secret code from email!",
              },
            ]}
          >
            <Input />
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
    error: state.error,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onAuth: (otp) => dispatch(actions.authOtp(otp)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(App);
