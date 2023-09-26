import React from "react";
import { LockOutlined, UserOutlined } from "@ant-design/icons";
import { NavLink } from "react-router-dom";
import { connect } from "react-redux";
import { Button, Form, Input, Radio } from "antd";
import * as actions from "../store/actions/auth";

const App = (props) => {
  const [form] = Form.useForm();

  const onFinish = (values) => {
    props.onAuth(
      values.username,
      values.email,
      values.phone_no,
      values.head,
      values.ogrn,
      values.inn,
      values.address_reg,
      values.address_fact,
      values.is_rest,
      values.is_ind_pred,
      values.password1,
      values.password2,
      props.regDone
    );
  };

  let errorMessage = null;
  if (props.error) {
    console.log(props.error);
    errorMessage = <p className="error">{props.error.response.data.error}</p>;
  }

  return (
    <div style={{ display: "flex", justifyContent: "space-between" }}>
      {errorMessage}
      <Form
        form={form}
        name="register"
        onFinish={onFinish}
        style={{
          maxWidth: 700,
        }}
        scrollToFirstError
        id="regForm"
      >
        <h1 style={{ marginBottom: "10px" }}>Регистрация</h1>
        <Form.Item
          name="username"
          label="Полное имя организации:"
          tooltip="Введите название и форму организации без сокращений. Например: ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ 'ДИВА'"
          rules={[
            {
              required: true,
              message: "Пожалуйста введите полное имя вашей организации!",
              whitespace: true,
            },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          name="email"
          label="E-mail"
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
          <Input prefix={<UserOutlined className="site-form-item-icon" />} />
        </Form.Item>

        <Form.Item
          name="phone_no"
          label="Телефон"
          rules={[
            {
              required: true,
              message: "Please input your phone number!",
            },
          ]}
        >
          <Input
            style={{
              width: "100%",
            }}
            prefix={"+"}
          />
        </Form.Item>

        <Form.Item
          name="head"
          label="Руководитель организации:"
          rules={[
            {
              message: "Пожалуйста введите руководителя вашей организации!",
              whitespace: true,
            },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          name="ogrn"
          label="ОГРН/ОГРНИП:"
          rules={[
            {
              required: true,
              message: "Пожалуйста введите ОГРН/ОГРНИП вашей организации!",
              whitespace: true,
            },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          name="inn"
          label="ИНН:"
          rules={[
            {
              required: true,
              message: "Пожалуйста введите ИНН вашей организации!",
              whitespace: true,
            },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          name="address_reg"
          label="Юридический регистрации:"
          rules={[
            {
              message:
                "Пожалуйста введите Адрес регистрации вашей организации!",
              whitespace: true,
            },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          name="address_fact"
          label="Фактический адрес:"
          rules={[
            {
              message:
                "Пожалуйста введите Фактический адрес вашей организации!",
              whitespace: true,
            },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Тип организации:"
          name="is_rest"
          rules={[
            {
              required: true,
            },
          ]}
        >
          <Radio.Group>
            <Radio value="True"> Ресторан </Radio>
            <Radio value="False"> Благотворительная организация </Radio>
          </Radio.Group>
        </Form.Item>

        <Form.Item
          label="Вид деятельности:"
          name="is_ind_pred"
          rules={[
            {
              required: true,
            },
          ]}
        >
          <Radio.Group>
            <Radio value="True"> ИП </Radio>
            <Radio value="False"> Юридическое лицо </Radio>
          </Radio.Group>
        </Form.Item>

        <Form.Item
          name="password1"
          label="Пароль:"
          tooltip="1. Пароль не должен быть слишком похож на другую вашу личную информацию.
        2. Ваш пароль должен содержать как минимум 8 символов.
        3. Пароль не должен быть слишком простым и распространенным.
        4. Пароль не может состоять только из цифр."
          rules={[
            {
              required: true,
              message: "Please input your password!",
            },
          ]}
          hasFeedback
        >
          <Input.Password
            prefix={<LockOutlined className="site-form-item-icon" />}
            type="password"
            placeholder="Password"
            autoComplete="off"
          />
        </Form.Item>

        <Form.Item
          name="password2"
          label="Подтверждение пароля: "
          dependencies={["password"]}
          hasFeedback
          rules={[
            {
              required: true,
              message: "Please confirm your password!",
            },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue("password1") === value) {
                  return Promise.resolve();
                }
                return Promise.reject(
                  new Error("The new password that you entered do not match!")
                );
              },
            }),
          ]}
        >
          <Input.Password
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
            Зарегистрироваться
          </Button>
          Или
          <NavLink style={{ marginRight: "10px" }} to="/login/">
            {" "}
            Войти
          </NavLink>
        </Form.Item>
      </Form>
      <div style={{ width: 600 }}>
        <h2>Инструкция</h2>
        <p style={{ marginTop: "10px" }}>
          Для того, чтобы посмотреть все необходимые для регистрации данные вы
          можете воспользоваться сайтом https://checko.ru/.
        </p>
        <img
          className="checko"
          src={require("../img/checko.png")}
          alt="checko"
          style={{ marginTop: "10px" }}
          width={600}
        />
        <p style={{ marginTop: "10px" }}>
          В строке поиска введите свои фамилию, имя, отчество или название
          организации. Затем в результатах поиска выберите свою компанию,
          перейдите на её страницу и там вы сможете найти всю необходимую
          информацию.
        </p>
        <img
          className="checko"
          src={require("../img/checkoData.png")}
          alt="checkoData"
          style={{ marginTop: "10px" }}
          width={600}
        />
        <p style={{ marginTop: "10px" }}>
          Кроме того эти данные вы можете найти в своём аккаунте на госуслугах
          или в регистрационных документах. При возникновении трудностей просим
          вас обращаться по адресу тех. поддержки: berko_aleksandr@mail.ru.
        </p>
      </div>
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
    onAuth: (
      username,
      email,
      phone_no,
      head,
      ogrn,
      inn,
      address_reg,
      address_fact,
      is_rest,
      is_ind_pred,
      password1,
      password2,
      regDone
    ) =>
      dispatch(
        actions.authSignup(
          username,
          email,
          phone_no,
          head,
          ogrn,
          inn,
          address_reg,
          address_fact,
          is_rest,
          is_ind_pred,
          password1,
          password2,
          regDone
        )
      ),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(App);
