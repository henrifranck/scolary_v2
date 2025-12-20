import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { apiRequest } from './api-client';

export interface University {
  id: number;
  province: string;
  department_name?: string | null;
  department_other_information?: string | null;
  department_address?: string | null;
  email: string;
  logo_university?: string | null;
  logo_departement?: string | null;
  phone_number?: string | null;
  admin_signature?: string | null;
}

export type UniversityPayload = Omit<University, 'id'>;

type UniversityListResponse = {
  count: number;
  data?: University[] | null;
};

const universityInfoKey = ['university', 'info'] as const;

export const fetchUniversityInfo = async (): Promise<University | null> => {
  const response = await apiRequest<UniversityListResponse>('/universitys/', {
    query: { limit: 1, offset: 0 }
  });

  return response.data?.[0] ?? null;
};

export const createUniversity = (payload: UniversityPayload): Promise<University> =>
  apiRequest<University>('/universitys/', {
    method: 'POST',
    json: payload
  });

export const updateUniversity = (
  id: number,
  payload: UniversityPayload
): Promise<University> =>
  apiRequest<University>(`/universitys/${id}`, {
    method: 'PUT',
    json: payload
  });

export const useUniversityInfo = () =>
  useQuery({
    queryKey: universityInfoKey,
    queryFn: fetchUniversityInfo
  });

export const useSaveUniversity = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id?: number; payload: UniversityPayload }) =>
      id ? updateUniversity(id, payload) : createUniversity(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: universityInfoKey });
    }
  });
};

export const universityService = {
  fetchUniversityInfo,
  createUniversity,
  updateUniversity,
  useUniversityInfo,
  useSaveUniversity
};
