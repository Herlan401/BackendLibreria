const { postLogin, postRefresh } = require("../services/auth.service");
const { createSessionCookie } = require("../utils/cookie.utils");

exports.login = (req, res) => {
    const { email, password } = req.body;
    if (!email || !password) {
        return res.status(400).json({ message: 'Email and password are required' });
    }
    postLogin(email, password)
        .then((response) => {
            const token = response.access;
            const refreshToken = response.refresh;
            createSessionCookie(res, token, refreshToken);
            res.send({
                message: 'Login successful'
            });
        })
        .catch((error) => {
            console.log(error);
            res.status(401).send({
                message: 'Unauthorized'
            })
        })

}
exports.refresh = (req, res) => {
    const refreshToken = req.cookies.refresh;
    if (!refreshToken) {
        return res.status(401).json({ message: 'Refresh token is required' });
    }
    postRefresh(refreshToken)
        .then((response) => {
            const token = response.access;
            createSessionCookie(res, token);
            res.send({
                message: 'Refresh token successful'
            });
        })
        .catch((error) => {
            console.log(error);
            res.status(401).send({
                message: 'Unauthorized'
            })
        })
}
exports.logout = (req, res) => {
    res.clearCookie('access');
    res.clearCookie('refresh');
    res.send({
        message: 'Logout successful'
    });
}