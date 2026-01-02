import { useState } from 'react'
import { uploadsApi, Upload } from '../api/uploads'
import './UploadPanel.css'

interface UploadPanelProps {
  caseId: number
  uploads: Upload[]
  onUpload: () => void
}

export default function UploadPanel({ caseId, uploads, onUpload }: UploadPanelProps) {
  const [uploading, setUploading] = useState(false)

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    try {
      await uploadsApi.upload(caseId, file)
      onUpload()
    } catch (error) {
      console.error('Upload failed:', error)
      alert('上傳失敗')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="upload-panel">
      <h3>上傳檔案</h3>
      <div className="upload-area">
        <input
          type="file"
          id="file-upload"
          onChange={handleFileUpload}
          disabled={uploading}
          accept=".txt,.doc,.docx,image/*"
        />
        <label htmlFor="file-upload" className="upload-button">
          {uploading ? '上傳中...' : '選擇檔案'}
        </label>
        <p className="upload-hint">支援格式：文字檔（逐字稿）、圖片（工廠機器照片）</p>
      </div>

      <div className="uploads-list">
        <h4>已上傳檔案</h4>
        {uploads.length > 0 ? (
          <ul>
            {uploads.map((upload) => (
              <li key={upload.id}>
                <span className="upload-type">{upload.type === 'transcript' ? '逐字稿' : '照片'}</span>
                <span className="upload-filename">{upload.filename}</span>
                <span className="upload-date">
                  {new Date(upload.created_at).toLocaleString('zh-TW')}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="empty">尚無上傳檔案</p>
        )}
      </div>
    </div>
  )
}

