import { APICall } from './API';
import { SpyCat, SpyCatUpdates } from '../types/spy-cat';

export const addCat = async (catData: SpyCat) => {
    const response = await APICall({
        method: 'POST',
        path: '/spy-cat',
        headers: null,
        body: catData
    });

    return response;
};

export const getAllCats = async () => {
    const response = await APICall({
        method: 'GET',
        path: '/spy-cat/all',
        headers: null,
        body: null
    });

    return response;
};

export const getCat = async (catID: string) => {
    const response = await APICall({
        method: 'GET',
        path: `/spy-cat/${catID}`,
        headers: null,
        body: null
    });

    return response;
};

export const updateCat = async (catData: SpyCatUpdates) => {
    const response = await APICall({
        method: 'PUT',
        path: `/spy-cat/${catData.catID}?newSalary=${catData.salary}`,
        headers: null,
        body: null
    });

    return response;
};

export const deleteCat = async (catID: string) => {
    const response = await APICall({
        method: 'DELETE',
        path: `/spy-cat/${catID}`,
        headers: null,
        body: null
    });

    return response;
};