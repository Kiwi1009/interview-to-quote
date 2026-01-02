import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { casesApi } from '../api/cases'
import { uploadsApi } from '../api/uploads'
import { extractionApi } from '../api/extraction'
import { plansApi } from '../api/plans'
import { documentsApi } from '../api/documents'
import SimpleHeader from '../components/SimpleHeader'
import './SimpleUpload.css'

export default function SimpleUpload() {
  const [caseId, setCaseId] = useState<number | null>(null)
  const [caseTitle, setCaseTitle] = useState('')
  const [transcriptFile, setTranscriptFile] = useState<File | null>(null)
  const [photoFiles, setPhotoFiles] = useState<File[]>([])
  const [processing, setProcessing] = useState(false)
  const [status, setStatus] = useState('')
  const queryClient = useQueryClient()

  // Create case mutation
  const createCaseMutation = useMutation({
    mutationFn: (title: string) => casesApi.create({ title, industry: '製造業' }),
    onSuccess: (response) => {
      setCaseId(response.data.id)
      setStatus('案件已建立，請上傳檔案')
    },
  })

  // Upload files mutation
  const uploadMutation = useMutation({
    mutationFn: async ({ caseId, file }: { caseId: number; file: File }) => {
      return uploadsApi.upload(caseId, file)
    },
  })

  // Extraction mutation
  const extractMutation = useMutation({
    mutationFn: (caseId: number) => extractionApi.start(caseId),
  })

  // Generate plans mutation
  const generatePlansMutation = useMutation({
    mutationFn: (caseId: number) => plansApi.generate(caseId),
  })

  // Generate documents mutation
  const generateDocsMutation = useMutation({
    mutationFn: (caseId: number) =>
      documentsApi.generate(caseId, undefined, 'spec,report,quote', 'docx,pdf'),
  })

  // Query documents
  const { data: documents, refetch: refetchDocuments } = useQuery({
    queryKey: ['documents', caseId],
    queryFn: () => documentsApi.list(caseId!).then(r => r.data),
    enabled: !!caseId,
    refetchInterval: caseId ? 3000 : false, // Poll every 3 seconds
  })

  // Query extraction status
  const { data: requirements } = useQuery({
    queryKey: ['requirements', caseId],
    queryFn: () => extractionApi.getRequirements(caseId!).then(r => r.data),
    enabled: !!caseId,
    refetchInterval: caseId ? 3000 : false,
  })

  // Handle file selection
  const handleTranscriptChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setTranscriptFile(file)
    }
  }

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    setPhotoFiles(files)
  }

  // Handle create case and upload
  const handleSubmit = async () => {
    if (!caseTitle.trim()) {
      alert('請輸入案件名稱')
      return
    }

    if (!transcriptFile) {
      alert('請上傳會議逐字稿')
      return
    }

    setProcessing(true)
    setStatus('正在建立案件...')

    try {
      // Create case if not exists
      let currentCaseId = caseId
      if (!currentCaseId) {
        const caseResponse = await createCaseMutation.mutateAsync(caseTitle)
        currentCaseId = caseResponse.data.id
        setCaseId(currentCaseId)
      }

      setStatus('正在上傳逐字稿...')
      // Upload transcript
      await uploadMutation.mutateAsync({ caseId: currentCaseId, file: transcriptFile })

      // Upload photos
      if (photoFiles.length > 0) {
        setStatus('正在上傳圖片...')
        for (const photo of photoFiles) {
          await uploadMutation.mutateAsync({ caseId: currentCaseId, file: photo })
        }
      }

      setStatus('正在提取需求...')
      // Start extraction
      const extractResponse = await extractMutation.mutateAsync(currentCaseId)
      const runId = extractResponse.data.id

      // Wait for extraction to complete
      setStatus('等待需求提取完成...')
      await waitForExtraction(currentCaseId, runId)

      setStatus('正在產生報價方案...')
      // Generate plans
      await generatePlansMutation.mutateAsync(currentCaseId)

      setStatus('正在產生文件...')
      // Generate documents
      await generateDocsMutation.mutateAsync(currentCaseId)

      setStatus('處理完成！文件已生成，請查看下方下載區域')
      refetchDocuments()
    } catch (error) {
      console.error('處理失敗:', error)
      setStatus('處理失敗，請重試')
      alert('處理失敗：' + (error as Error).message)
    } finally {
      setProcessing(false)
    }
  }

  // Wait for extraction to complete
  const waitForExtraction = async (caseId: number, runId: number, maxWait = 120000) => {
    const startTime = Date.now()
    while (Date.now() - startTime < maxWait) {
      try {
        const run = await extractionApi.getRun(runId)
        if (run.data.status === 'completed') {
          return
        }
        if (run.data.status === 'failed') {
          throw new Error('需求提取失敗')
        }
        await new Promise(resolve => setTimeout(resolve, 2000)) // Wait 2 seconds
      } catch (error) {
        console.error('檢查提取狀態失敗:', error)
      }
    }
    throw new Error('提取超時')
  }

  // Handle document download
  const handleDownload = async (docId: number, filename: string) => {
    try {
      const response = await documentsApi.download(docId)
      const blob = new Blob([response.data])
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('下載失敗:', error)
      alert('下載失敗')
    }
  }

  const getDocTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      spec: '需求規格書',
      report: '需求報告表',
      quote: '報價單',
    }
    return labels[type] || type
  }

  const getFormatLabel = (format: string) => {
    return format.toUpperCase()
  }

  return (
    <div className="simple-upload">
      <SimpleHeader />
      <div className="upload-container-wrapper">
        <div className="upload-container">
        <h1>訪談轉報價平台</h1>
        <p className="subtitle">上傳會議逐字稿和圖片，自動生成需求文件和報價單</p>

        <div className="form-section">
          <div className="form-group">
            <label htmlFor="case-title">案件名稱 *</label>
            <input
              id="case-title"
              type="text"
              value={caseTitle}
              onChange={(e) => setCaseTitle(e.target.value)}
              placeholder="例如：XX公司自動化專案"
              disabled={processing || !!caseId}
            />
          </div>

          <div className="form-group">
            <label htmlFor="transcript">會議逐字稿 *</label>
            <input
              id="transcript"
              type="file"
              accept=".txt,.doc,.docx"
              onChange={handleTranscriptChange}
              disabled={processing}
            />
            {transcriptFile && (
              <div className="file-info">
                <span className="file-name">✓ {transcriptFile.name}</span>
                <span className="file-size">
                  ({(transcriptFile.size / 1024).toFixed(2)} KB)
                </span>
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="photos">工廠機器照片（可選，可多選）</label>
            <input
              id="photos"
              type="file"
              accept="image/*"
              multiple
              onChange={handlePhotoChange}
              disabled={processing}
            />
            {photoFiles.length > 0 && (
              <div className="files-list">
                {photoFiles.map((file, idx) => (
                  <div key={idx} className="file-info">
                    <span className="file-name">✓ {file.name}</span>
                    <span className="file-size">
                      ({(file.size / 1024).toFixed(2)} KB)
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          <button
            className="submit-button"
            onClick={handleSubmit}
            disabled={processing || !transcriptFile || !caseTitle.trim()}
          >
            {processing ? '處理中...' : '開始處理並生成文件'}
          </button>

          {status && (
            <div className={`status-message ${processing ? 'processing' : 'completed'}`}>
              {status}
            </div>
          )}
        </div>

        {documents && documents.length > 0 && (
          <div className="documents-section">
            <h2>生成的文件</h2>
            <div className="documents-grid">
              {documents.map((doc) => (
                <div key={doc.id} className="document-card">
                  <div className="doc-header">
                    <h3>{getDocTypeLabel(doc.doc_type)}</h3>
                    <span className="doc-format">{getFormatLabel(doc.format)}</span>
                  </div>
                  <div className="doc-meta">
                    <span>生成時間：{new Date(doc.created_at).toLocaleString('zh-TW')}</span>
                  </div>
                  <button
                    className="download-button"
                    onClick={() =>
                      handleDownload(doc.id, `${doc.doc_type}_${doc.id}.${doc.format}`)
                    }
                  >
                    下載
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
        </div>
      </div>
    </div>
  )
}

