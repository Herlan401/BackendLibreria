const createSessionCookie = (res, token, refreshToken) => {
    const baseOptions = {
        httpOnly: true,
        secure: false,
        sameSite: 'Lax',
    };

    res.cookie('access', token, {
        ...baseOptions,
        maxAge: 10 * 60 * 1000, // 10 minutes
    });

    if (refreshToken) {
        res.cookie('refresh', refreshToken, {
            ...baseOptions,
            maxAge: 24 * 60 * 60 * 1000, // 1 day
        });
    }
};

module.exports = {
    createSessionCookie,
};

