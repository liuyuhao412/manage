import instance from "@/utils/request";

export const login = async (account: string, password: string) => {
    const response = await instance.post('/api/login', { account, password });
    return response;
};

export const checkEmailRegistered = async (email: string) => {
    const response = await instance.post('/api/check-email-registered', { email });
    return response;
};


export const sendVerificationCode = async (email: string) => {
    const response = await instance.post('/api/send-verification-code', { email });
    return response;
};

export const register = async (data: { email: string; password: string }) => {
    const response = await instance.post('/api/register', data);
    return response;
};

export const recoverAccount = async (data: { email: string; newPassword: string }) => {
    const response = await instance.post('/api/recover-account', data);
    return response;
};

export const fetchUserRole = async (token: string) => {
    const response = await instance.get('/api/user-role');
    return response;
};

export const fetchCurrentUserName = async () => {
    const response = await instance.get('/api/current-user-name');
    return response;
};
