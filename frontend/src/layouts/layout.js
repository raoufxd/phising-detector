import React, { useState } from "react";
import { Switch, Route, NavLink, withRouter } from "react-router-dom";
import { Layout, Menu, Button  } from 'antd';
import 'antd/dist/antd.css';
import "./layout.css";

import routes from '../routes';

const { Header, Content, Footer } = Layout;

const switchRoutes = (
  <Switch>
    {routes.map((route, key) => {
        return(
          <Route 
              path={route.path}
              component={route.component}
              key={key}
          />
        )
    })}
  </Switch>
);

const LayoutPage = ({ ...rest }) => {
    return (
      <Layout className="layout">
          <Content className="site-layout-content">
              
              {switchRoutes}
          
          </Content>
          <Footer className="footer" >
              &copy; {1900+ new Date().getYear()}{" "}, made with love
          </Footer>
      </Layout>
    );
}

export default LayoutPage;