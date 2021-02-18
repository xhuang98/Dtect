import React from 'react';
import InputField from './InputField'
import UserStore from './stores/UserStore'
import logo from "assets/img/logo-full.png";
import Button from "components/CustomButtons/Button.js";

import { withRouter} from "react-router-dom";
import "assets/css/material-dashboard-react.css?v=1.9.0";


class LoginForm extends React.Component {



    constructor(props) {
        super(props)
        this.state = {
            username: '',
            password: '',
            buttonDisabled: false
        }
    }

    setInputValue(property, val) {
        val = val.trim();
        if (val.length > 12) {
            return;
        }
        this.setState({[property]: val})
    }

    resetForm() {
        this.setState({
            username: '',
            password: '',
            buttonDisabled: false
        })
    }

    async doLogin() {
        if (!this.state.username || !this.state.password) {
            return;
        }

        this.setState({buttonDisabled: true})

        try {
            let res = await fetch('/login', {
                method: 'post',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: this.state.username,
                    password: this.state.password
                })
            });

            let result = await res.json();

            if (result && result.success) {
                UserStore.isLoggedIn = true;
                UserStore.username = result.username;
                this.toDashboard();
            }

            else if (result && result.success === false) {
                this.resetForm();
                alert(result.message);
            }

        } catch (e) {
            console.log(e);
            this.resetForm();
        }

    }

    render() {
        return (
            <div className="loginForm" align="center" >
                <img src={logo} height="349px" width="492px" margin-top='50px'></img>
                <InputField
                    type='text'
                    placeholder="Username"
                    value={this.state.username ? this.state.username : ''}
                    onChange={ (val) => this.setInputValue('username', val)}
                />
                <br></br>
                <InputField
                    type='password'
                    placeholder="Password"
                    value={this.state.password ? this.state.password : ''}
                    onChange={ (val) => this.setInputValue('password', val) }
                />
                <br></br>
                
                <Button
                    color="info"
                    onClick={() => this.doLogin()}
                >
                Login
                </Button> 
            </div>
        );
    }

    toDashboard = () => {
        this.props.history.push('/admin/dashboard');
    }
  
}

export default withRouter(LoginForm);
