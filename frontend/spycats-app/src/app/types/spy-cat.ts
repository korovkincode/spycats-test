export type SpyCat = {
    ID: string | null // null for form
    name: string,
    experience: number,
    breed: string,
    salary: number
};

export type SpyCatUpdates = {
    catID: string,
    salary: number
};