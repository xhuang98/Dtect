import React from 'react';
import { observer } from 'mobx-react';
import UserStore from './stores/UserStore';
import LoginForm from './LoginForm';
import SubmitButton from './SubmitButton';
import Admin from './layouts/Admin';
import './App.css';

import { createBrowserHistory } from "history";
import { Router, Route, Switch, Redirect } from "react-router-dom";
import "assets/css/material-dashboard-react.css?v=1.9.0";

const hist = createBrowserHistory();

class App extends React.Component {

    async componentDidMount() {

        UserStore.loading = false;
        UserStore.isLoggedIn = false;
    }

    async doLogout() {
        try {

            let res = await fetch('/logout', {
                method: 'post',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            });

            let result = await res.json();

            if (result && result.success) {
                UserStore.loading = false;
                UserStore.isLoggedIn = false;
                UserStore.username = '';
            }

        } catch (e) {
            console.log("Error logging out", e);
        }
    }


    render() {
        if (UserStore.loading) {
            return (
                <div className="app">
                    <div className="container">
                        Loading...
                    </div>
                </div>
            );
        }
        return (
            <div className="app">
                <Router history={hist}>
                    <Switch>
                        <Route path="/admin" component={Admin} />
    
                    </Switch>
                    <LoginForm />
                </Router>
            </div>
        );
    }

  
}

export default observer(App);
