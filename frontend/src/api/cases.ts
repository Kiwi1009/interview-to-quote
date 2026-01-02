import apiClient from './client'

export interface Case {
  id: number
  user_id: number
  title: string
  industry: string | null
  status: 'draft' | 'extracting' | 'reviewing' | 'quoted' | 'archived'
  created_at: string
  updated_at: string | null
}

export interface CaseCreate {
  title: string
  industry?: string
}

export const casesApi = {
  list: () => apiClient.get<Case[]>('/cases'),
  get: (id: number) => apiClient.get<Case>(`/cases/${id}`),
  create: (data: CaseCreate) => apiClient.post<Case>('/cases', data),
  update: (id: number, data: Partial<CaseCreate>) => apiClient.put<Case>(`/cases/${id}`, data),
}

