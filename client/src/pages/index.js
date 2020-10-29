import React from 'react'
import { Formik, Field, Form, ErrorMessage } from 'formik';

const Home = () => {
    return (
        <div style = {{
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '90vh'
            }}
        >
        <Formik
            initialValues={{ firstName: "", lastName: ""}}
            validate={values => {
              const errors = {};
              if(!values.firstName) {
                errors.firstName = "required";
              }
              return errors;
            }}
            onSubmit={(values, {setSubmitting}) => {
              setTimeout(() => {
                alert(JSON.stringify(values, null, 2));
                setSubmitting(false);
              }, 400);
            }}
          >
            {({isSubmitting}) => (
              <Form>
                <Field type="text" name="firstName" />
                <br/>
                <ErrorMessage name="firstName" component="div" />
                <br/>
                <Field type="text" name="lastName" />
                <br/>
                <ErrorMessage name="lastName" component="div" />
                <br/>
                <button type="submit" disabled={isSubmitting}>
                  submit
                </button>
              </Form> 
              )}
          </Formik>
        </div>
    )
}

export default Home
