import React, { useState } from "react";
import { Button, Form, Input, DatePicker, Modal } from "antd";
import { useNavigate } from "react-router-dom";

const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 16,
  },
};

/* eslint-disable no-template-curly-in-string */
const validateMessages = {
  required: "${label} is required!",
  types: {
    email: "${label} is not a valid email!",
    number: "${label} is not a valid number!",
  },
  number: {
    range: "${label} must be between ${min} and ${max}",
  },
};
/* eslint-enable no-template-curly-in-string */

const App = (props) => {
  const navigate = useNavigate();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const token = localStorage.getItem("token");

  const onFinish = (values) => {
    const formData = new FormData();
    formData.append("title", values.title);
    formData.append("full_info", values.full_info);
    formData.append(
      "deadline_date",
      new Intl.DateTimeFormat("ru", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }).format(values.deadline_date)
    );

    props.apiFunc(
      "https://95.140.148.239/help/create/",
      "POST",
      token,
      formData
    );
    setIsModalVisible(true);

    console.log(values);
  };

  const handleModalOk = () => {
    setIsModalVisible(false);
    navigate("/requests", { replace: true });
  };

  return (
    <div>
      <h2 style={{ marginBottom: "20px" }}>Введите данные заявки</h2>
      <Form
        {...layout}
        name="nest-messages"
        onFinish={onFinish}
        style={{
          maxWidth: 600,
        }}
        validateMessages={validateMessages}
      >
        <Form.Item
          name="title"
          label="Название"
          rules={[
            {
              required: true,
            },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item name="full_info" label="Описание">
          <Input.TextArea rows={9} />
        </Form.Item>

        <Form.Item name="deadline_date" label="Срок выполнения">
          <DatePicker />
        </Form.Item>

        <Form.Item
          wrapperCol={{
            ...layout.wrapperCol,
            offset: 8,
          }}
        >
          <Button type="primary" htmlType="submit">
            Подать
          </Button>
        </Form.Item>
      </Form>

      <Modal
        title="Отлично!"
        visible={isModalVisible}
        onOk={handleModalOk}
        closable={false}
        maskClosable={false}
        onCancel={handleModalOk}
      >
        <p>Вы подали заявку</p>
      </Modal>
    </div>
  );
};
export default App;
