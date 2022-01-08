import React, {useState, useEffect} from 'react';
import { Input, Alert, Typography, notification } from 'antd';
import "./homePage.css";
import logo from '../assets/logo-svg.png'
const axios = require('axios');
const isReachable = require('is-reachable');

const { Search } = Input;
const { Title } = Typography;

const HomePage = () => {
    const [url, setUrl] = useState("")
    const [bool, setBool] = useState(-1)
    const [waiting, setWaiting] = useState(false)
    const handleURLChange = (event) => {
        setUrl(event.target.value)
        if(event.target.value==''){
            setBool(-1)
        }
    } 

    const alertCloseHandler = () => {
        console.log("New URL")
        setBool(-1)
    }

    const openNotification = () => {
        notification.open({
          key: 'updatable',
          message: 'Invalid url (can\'t reach the url)!',
          description: 'Please check the url format.',
          duration: 2,
          style: {backgroundColor: 'rgba(255, 0, 0, 0.4)', color: "white"},
          type: "error"
        });
    }

    const openNotificationError = () => {
        notification.open({
          key: 'updatable',
          message: 'Error!!',
          description: 'Error occured ib the server!',
          duration: 2,
          style: {backgroundColor: 'rgba(255, 0, 0, 0.4)', color: "white"},
          type: "error"
        });
    }
    
    const onSearch = async (value) => {
        //send the URL to the python backend and receive response
        //0 means the URL is safe
        //1 means the URL is phishing url
        
        //check if the url is valid or not
        setWaiting(true)
            axios.get('http://127.0.0.1:5000/predict?url='+ url)
            .then((res) => {
                let prediction = parseInt(res.data[0])
                console.log("prediction : ", prediction)
                setBool(prediction)
                setWaiting(false)
                if(prediction==2){
                    openNotification()
                }
            })
            .catch((err) => {
                console.log("error : ", err)
                openNotificationError()
                setWaiting(false)
            })
    }

    return(
        <div className="container">
            <img className="logoImage" src={logo} />
            <div className="inputContainer">
            <Search
                    className="input"
                    placeholder="Enter URL..."
                    value={url}
                    onChange={handleURLChange}
                    enterButton="Check it!"
                    size="large"
                    onSearch={onSearch}
                    onClick={alertCloseHandler}
                    loading={waiting}
                    
                />
           </div>
            {   
                bool===1 ? (
                    <Alert
                        className="alert"
                        message="Success"
                        description="This website is safe."
                        type="success"
                        showIcon
                        style={{backgroundColor: 'rgba(0, 255, 0, 0.3)'}}
                    />
                ):(
                    bool===0?(
                        <Alert
                            className="alert"
                            message="Warning"
                            description="This is a phishing website."
                            type="warning"
                            showIcon
                            style={{backgroundColor: 'rgba(255, 0, 0, 0.3)'}}
                        />
                    ):
                    (
                        <Alert
                            className="alert"
                            message="How to use ?"
                            description="Type a website and press 'check it'. (example https://stackoverflow.com/)"
                            type="info"
                            showIcon
                        />
                    )
                )
            }      
        </div>
    );
}

export default HomePage;