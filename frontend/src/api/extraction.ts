import apiClient from './client'

export interface ExtractionRun {
  id: number
  case_id: number
  version: number
  model: string | null
  prompt_hash: string | null
  status: 'pending' | 'running' | 'completed' | 'failed'
  created_at: string
  finished_at: string | null
}

export interface Evidence {
  field_path: string
  segment_idx: number | null
  snippet: string
  start_char: number | null
  end_char: number | null
}

export interface Requirements {
  run_id: number
  jsonb_data: Record<string, any>
  confidence: Record<string, number> | null
  evidence: Evidence[]
  created_at: string
}

export const extractionApi = {
  start: (caseId: number) => apiClient.post<ExtractionRun>(`/cases/${caseId}/extract`),
  getRun: (runId: number) => apiClient.get<ExtractionRun>(`/cases/runs/${runId}`),
  getRequirements: (caseId: number, runId?: number) => 
    apiClient.get<Requirements>(`/cases/${caseId}/requirements`, { params: { run_id: runId } }),
  updateRequirements: (caseId: number, data: Record<string, any>, runId?: number) =>
    apiClient.put<Requirements>(`/cases/${caseId}/requirements`, data, { params: { run_id: runId } }),
}

