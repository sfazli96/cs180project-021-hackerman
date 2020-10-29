import React from 'react'
import { Formik, Field, Form, ErrorMessage } from 'formik';

const World = () => {
    return (
        <div style = {{
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '90vh'
            }}
        >
        <Formik
            initialValues={{ country: "", video_id: "", channel_title: "", trending_date: "", category_id: "", tag: ""}}
            validate={values => {
              const errors = {};
              if(!values.country) {
                errors.country = "required";
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
                <Field type="text" name="country" placeholder="Country" />
                <br/>
                <ErrorMessage name="country" component="div" />
                <br/>
                <Field type="text" name="video_id" placeholder="Video ID" />
                <br/>
                <ErrorMessage name="video_id" component="div" />
                <br/>
                <Field type="text" name="channel_title" placeholder="Channel Title" />
                <br/>
                <ErrorMessage name="channel_title" component="div" />
                <br/>
                <Field type="date" name="trending_date" placeholder="Trending Date"/>
                <br/>
                <ErrorMessage name="trending_date" component="div" />
                <br/>
                <Field type="text" name="category_id" placeholder="Category"/>
                <br/>
                <ErrorMessage name="category_id" component="div" />
                <br/>
                <Field type="text" name="tag" placeholder="Tags"/>
                <br/>
                <ErrorMessage name="tag" component="div" />
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

export default World