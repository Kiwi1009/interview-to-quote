import { useParams } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { casesApi } from '../api/cases'
import { uploadsApi } from '../api/uploads'
import { extractionApi } from '../api/extraction'
import { plansApi } from '../api/plans'
import { documentsApi } from '../api/documents'
import UploadPanel from '../components/UploadPanel'
import RequirementsEditor from '../components/RequirementsEditor'
import PlansComparison from '../components/PlansComparison'
import DocumentsPanel from '../components/DocumentsPanel'
import './CaseDetail.css'

export default function CaseDetail() {
  const { caseId } = useParams<{ caseId: string }>()
  const caseIdNum = parseInt(caseId || '0')
  const queryClient = useQueryClient()
  const [activeTab, setActiveTab] = useState<'upload' | 'requirements' | 'plans' | 'documents'>('upload')

  const { data: caseData } = useQuery({
    queryKey: ['case', caseIdNum],
    queryFn: () => casesApi.get(caseIdNum).then(r => r.data),
  })

  const { data: uploads } = useQuery({
    queryKey: ['uploads', caseIdNum],
    queryFn: () => uploadsApi.list(caseIdNum).then(r => r.data),
  })

  const { data: requirements } = useQuery({
    queryKey: ['requirements', caseIdNum],
    queryFn: () => extractionApi.getRequirements(caseIdNum).then(r => r.data),
    enabled: !!caseIdNum,
  })

  const { data: plans } = useQuery({
    queryKey: ['plans', caseIdNum],
    queryFn: () => plansApi.list(caseIdNum).then(r => r.data),
    enabled: !!caseIdNum,
  })

  const { data: documents } = useQuery({
    queryKey: ['documents', caseIdNum],
    queryFn: () => documentsApi.list(caseIdNum).then(r => r.data),
    enabled: !!caseIdNum,
  })

  const extractMutation = useMutation({
    mutationFn: () => extractionApi.start(caseIdNum),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['requirements', caseIdNum] })
    },
  })

  const generatePlansMutation = useMutation({
    mutationFn: () => plansApi.generate(caseIdNum),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['plans', caseIdNum] })
    },
  })

  const generateDocsMutation = useMutation({
    mutationFn: () => documentsApi.generate(caseIdNum, undefined, 'spec,report,quote', 'docx,pdf'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents', caseIdNum] })
    },
  })

  if (!caseData) {
    return <div className="loading">載入中...</div>
  }

  return (
    <div className="case-detail">
      <div className="case-header">
        <h2>{caseData.title}</h2>
        <div className="case-status">
          狀態：{caseData.status}
        </div>
      </div>

      <div className="tabs">
        <button
          className={activeTab === 'upload' ? 'active' : ''}
          onClick={() => setActiveTab('upload')}
        >
          上傳檔案
        </button>
        <button
          className={activeTab === 'requirements' ? 'active' : ''}
          onClick={() => setActiveTab('requirements')}
        >
          需求提取
        </button>
        <button
          className={activeTab === 'plans' ? 'active' : ''}
          onClick={() => setActiveTab('plans')}
        >
          報價方案
        </button>
        <button
          className={activeTab === 'documents' ? 'active' : ''}
          onClick={() => setActiveTab('documents')}
        >
          文件下載
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'upload' && (
          <UploadPanel
            caseId={caseIdNum}
            uploads={uploads || []}
            onUpload={() => {
              queryClient.invalidateQueries({ queryKey: ['uploads', caseIdNum] })
            }}
          />
        )}

        {activeTab === 'requirements' && (
          <RequirementsEditor
            caseId={caseIdNum}
            requirements={requirements}
            onExtract={() => extractMutation.mutate()}
            onUpdate={() => {
              queryClient.invalidateQueries({ queryKey: ['requirements', caseIdNum] })
            }}
          />
        )}

        {activeTab === 'plans' && (
          <PlansComparison
            caseId={caseIdNum}
            plans={plans || []}
            onGenerate={() => generatePlansMutation.mutate()}
          />
        )}

        {activeTab === 'documents' && (
          <DocumentsPanel
            caseId={caseIdNum}
            documents={documents || []}
            onGenerate={() => generateDocsMutation.mutate()}
          />
        )}
      </div>
    </div>
  )
}

