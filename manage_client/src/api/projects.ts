import instance from "@/utils/request";

export const fetchProjects = async () => {
    const response = await instance.get("/api/projects");
    return response;
};

export const fetchProjectById = async (id: number) => {
    const response = await instance.get(`/api/projects/${id}`);
    return response;
};

export const createProject = async (data: { name: string, description: string, start_date: string, end_date: string, status: string, priority: string }) => {
    const response = await instance.post("/api/projects", data);
    return response;
};

export const deleteProject = async (id: number) => {
    const response = await instance.delete(`/api/projects/${id}`);
    return response;
};

export const updateProject = async (id: number, data: { name: string, description: string, start_date: string, end_date: string, status: string, priority: string }) => {
    const response = await instance.put(`/api/projects/${id}`, data);
    return response;
};

export const exportProjects = async (ids: string[]) => {
    const response = await instance.post("/api/projects/export", { ids }, { responseType: 'blob' });
    return response;
};

export const fetchArchivedProjects = async () => {
    const response = await instance.get("/api/archived-project");
    return response;
};
