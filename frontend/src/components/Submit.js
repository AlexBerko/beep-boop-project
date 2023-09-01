import React from "react";
import { Button, Form, Input, DatePicker } from "antd";

const { RangePicker } = DatePicker;
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

const rangeConfig = {
  rules: [
    {
      type: "array",
      required: true,
      message: "Please select time!",
    },
  ],
};

const App = (props) => {
  const onFinish = (values) => {
    // Should format date value before submit.
    //   const rangeValue = fieldsValue["range-picker"];
    //   const values = {
    //     ...fieldsValue,
    //     "range-picker": [
    //       rangeValue[0].format("YYYY-MM-DD"),
    //       rangeValue[1].format("YYYY-MM-DD"),
    //     ],
    //   };
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("title", values.title);
    formData.append("full_info", values.full_info);
    formData.append("date", values.range_picker);

    props.apiFunc(
      "http://127.0.0.1:8000/help/create/",
      "POST",
      token,
      formData
    );

    console.log(values);
  };

  return (
    <div>
      Введите данные заявки
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
          <Input.TextArea />
        </Form.Item>

        <Form.Item
          name="range_picker"
          label="Сроки выполнения"
          {...rangeConfig}
        >
          <RangePicker />
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
    </div>
  );
};
export default App;
