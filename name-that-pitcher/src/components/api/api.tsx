import axios from 'axios';

export interface Pitcher {
    id: number;
    name: string;
    jersey_number: string;
    team: string;
    division: string;
    age: string;
    handedness: string;
    birthplace: string;
    position: string;
};

const Api = axios.create({
  baseURL: 'http://localhost:8000', // Replace with your Django URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getAllPitchers = async (): Promise<Pitcher[]> => {
  const response = await Api.get<Pitcher[]>('/pitchers/');
  return response.data;
};

export const getPitcherById = async (pitcherId: number): Promise<Pitcher> => {
  const response = await Api.post<Pitcher>('/pitchers/', pitcherId);
  return response.data;
};