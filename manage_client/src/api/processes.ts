import instance from "@/utils/request";

export const fetchProcesses = async () => {
    const response = await instance.get("/api/processes");
    return response;
};

export const fetchProcessById = async (id: number) => {
    const response = await instance.get(`/api/processes/${id}`);
    return response;
};


export const updateProcessAPI = async (id: number, completion_rate: number) => {
    const response = await instance.put(`/api/processes/${id}`, { completion_rate: completion_rate });
    return response;
};

