import request from '../utils/request';

export const addUser = (data: { username: string; name: string; gender: string; birthday: string; role?: string; }) => {
    return request.post('/api/users', data);
};

export const deleteUser = (userId: number) => {
    return request.delete(`/api/users/${userId}`);
};

export const fetchUsers = () => {
    return request.get('/api/users');
};

export const fetchMembers = () => {
    return request.get('/api/users/members');
};

export const fetchUserById = (userId: number) => {
    return request.get(`/api/users/${userId}`);
};

export const updateUserInfo = (userId: number, data: { username: string; name: string; gender: string; birthday: string; role?: string; }) => {
    return request.put(`/api/users/${userId}/info`, data);
};

export const updateUserStatus = (userId: number, status: boolean) => {
    return request.put(`/api/users/${userId}/status`, { account_status: status });
};

export const exportUsers = (userIds: string[]) => {
    return request.post('/api/users/export', { userIds }, { responseType: 'blob' });
};
