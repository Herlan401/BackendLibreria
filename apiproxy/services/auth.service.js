const { default: axios, post } = require("axios")

const postLogin = (email, password) => {
    return new Promise((resolve, reject) => {
        axios.post('http://localhost:8000/api/token/', {
            email:email,
            password: password
        })
            .then(response => {
                resolve(response.data);
            })
            .catch(error => {
                reject(error);
            });
    });
}
const postRefresh = (refresh) => {
    return new Promise((resolve, reject) => {
        axios.post('http://localhost:8000/api/token/refresh/', {
            refresh
        })
            .then(response => {
                resolve(response.data);
            })
            .catch(error => {
                reject(error);
            });
    });
}

module.exports = {
    postLogin,
    postRefresh
}