import apiClient from './client'

export interface Upload {
  id: number
  case_id: number
  type: 'transcript' | 'photo'
  filename: string
  path: string
  sha256: string | null
  created_at: string
}

export const uploadsApi = {
  list: (caseId: number) => apiClient.get<Upload[]>(`/cases/${caseId}/uploads`),
  upload: (caseId: number, file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post<Upload>(`/cases/${caseId}/uploads`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

