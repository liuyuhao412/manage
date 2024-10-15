import instance from "@/utils/request";

export const fetchTasks = async () => {
    const response = await instance.get("/api/tasks");
    return response;
};

export const fetchMemberTasks = async () => {
    const response = await instance.get("/api/tasks/member");
    return response;
};


export const fetchTaskById = async (id: number) => {
    const response = await instance.get(`/api/tasks/${id}`);
    return response;
};

export const createTask = async (data: { title: string; description: string; due_date: string; project_id: number | null, status: string }) => {
    const response = await instance.post("/api/tasks", data);
    return response;
};

export const updateTask = async (id: number, data: { title: string; description: string; due_date: string; project_id: number | null, status: string }) => {
    const response = await instance.put(`/api/tasks/${id}`, data);
    return response;
};

export const deleteTask = async (id: number) => {
    const response = await instance.delete(`/api/tasks/${id}`);
    return response;
};
export const downloadTaskFile = async (filename: string) => {
    const response = await instance.get(`/api/download/${filename}`, {
        responseType: 'blob',
    });
    return response;
};

export const updateTaskStatus = async (id: number, status: string) => {
    const response = await instance.put(`/api/tasks/${id}/status`, { status });
    return response;
};

export const getTaskComments = async (id: number) => {
    const response = await instance.get(`/api/tasks/${id}/comments`);
    return response;
};

export const submitTaskComment = async (id: number, data: { content: string }) => {
    const response = await instance.post(`/api/tasks/${id}/comments`, data);
    return response;
};