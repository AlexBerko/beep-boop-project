import React, { useState } from "react";
import axios from "axios";
import { LockOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { Button, Form, Input, Modal } from "antd";

const App = (props) => {
  const [form] = Form.useForm();
  const [isModalVisible, setIsModalVisible] = useState(false);
  let [phoneField, setPhoneField] = useState(props.recordsJS.phone_no);
  let [adrRegField, setAdrRegField] = useState(props.recordsJS.address_reg);
  let [adrFactField, setAdrFactField] = useState(props.recordsJS.address_fact);
  const token = localStorage.getItem("token");
  const navigate = useNavigate();
  let config = {
    headers: {
      Authorization: `Token ${token}`,
    },
  };

  const onFinish = (values) => {
    const formData = new FormData();
    formData.append("phone_no", values.phone_no);
    formData.append("address_reg", values.address_reg);
    formData.append("address_fact", values.address_fact);

    const formPswd = new FormData();
    if (
      values.old_password === undefined &&
      values.new_password === undefined
    ) {
      formPswd.append("old_password", props.recordsJS.password1);
      formPswd.append("new_password", props.recordsJS.password1);
    } else {
      formPswd.append("old_password", values.old_password);
      formPswd.append("new_password", values.new_password);
    }

    try {
      axios
        .put(`https://95.140.148.239/user/profile/`, config, formData)
        .then((res) => {})
        .catch((err) => {
          console.log(err);
        });
      axios
        .post(`https://95.140.148.239/user/profile/`, config, formPswd)
        .then((res) => {})
        .catch((err) => {
          console.log(err);
        });

      setIsModalVisible(true);
    } catch (error) {
      console.log(error);
    }
  };

  const handleModalOk = () => {
    setIsModalVisible(false);
    navigate("/profile", { replace: true });
  };

  const handleChangePhone = (e) => {
    setPhoneField(e.target.value);
  };

  const handleChangeAdrReg = (e) => {
    setAdrRegField(e.target.value);
  };

  const handleChangeAdrFact = (e) => {
    setAdrFactField(e.target.value);
  };

  return (
    <div>
      <h2>Редактирование профиля</h2>
      <Form
        form={form}
        name="register"
        onFinish={onFinish}
        style={{
          maxWidth: 800,
        }}
        scrollToFirstError
        id="regForm"
      >
        <Form.Item name="phone_no" label="Телефон">
          <Input
            style={{
              width: "100%",
            }}
            type="text"
            value={phoneField}
            onChange={handleChangePhone}
            prefix={"+"}
          />
        </Form.Item>

        <Form.Item name="address_reg" label="Юридический регистрации:">
          <Input
            type="text"
            value={adrRegField}
            onChange={handleChangeAdrReg}
          />
        </Form.Item>

        <Form.Item name="address_fact" label="Фактический адрес:">
          <Input
            type="text"
            value={adrFactField}
            onChange={handleChangeAdrFact}
          />
        </Form.Item>

        <Form.Item
          name="old_password"
          label="Введите старый пароль:"
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
          name="new_password"
          label="Введите новый пароль: "
          tooltip="1. Пароль не должен быть слишком похож на другую вашу личную информацию.
        2. Ваш пароль должен содержать как минимум 8 символов.
        3. Пароль не должен быть слишком простым и распространенным.
        4. Пароль не может состоять только из цифр."
        >
          <Input.Password
            prefix={<LockOutlined className="site-form-item-icon" />}
            type="password"
            placeholder="Password"
            autoComplete="off"
          />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit">
            Сохранить
          </Button>
        </Form.Item>
      </Form>
      <Modal
        title="Изменения сохранены"
        visible={isModalVisible}
        onOk={handleModalOk}
        closable={false}
        maskClosable={false}
        onCancel={handleModalOk}
      />
    </div>
  );
};

export default App;
