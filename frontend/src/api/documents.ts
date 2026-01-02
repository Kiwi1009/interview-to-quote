import apiClient from './client'

export interface Document {
  id: number
  case_id: number
  run_id: number | null
  doc_type: 'spec' | 'report' | 'quote'
  format: 'docx' | 'pdf'
  path: string
  created_at: string
}

export const documentsApi = {
  generate: (caseId: number, runId?: number, types?: string, formats?: string) =>
    apiClient.post<Document[]>(`/cases/${caseId}/documents`, null, {
      params: { run_id: runId, types, formats },
    }),
  list: (caseId: number, runId?: number) =>
    apiClient.get<Document[]>(`/cases/${caseId}/documents`, { params: { run_id: runId } }),
  download: (docId: number) =>
    apiClient.get(`/documents/${docId}/download`, { responseType: 'blob' }),
}

