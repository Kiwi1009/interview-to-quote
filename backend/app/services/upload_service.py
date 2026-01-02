import os
import hashlib
import aiofiles
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.upload import Upload, UploadType
from app.models.case import Case
from app.core.config import settings

class UploadService:
    def __init__(self, db: Session):
        self.db = db
        os.makedirs(settings.UPLOAD_PATH, exist_ok=True)
    
    async def upload_file(self, case_id: int, file: UploadFile) -> Upload:
        # Verify case exists
        case = self.db.query(Case).filter(Case.id == case_id).first()
        if not case:
            return None
        
        # Determine upload type based on file extension and content type
        file_ext = os.path.splitext(file.filename)[1].lower()
        text_extensions = ['.txt', '.doc', '.docx']
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        
        if file_ext in text_extensions or (file.content_type and "text" in file.content_type):
            upload_type = UploadType.TRANSCRIPT
        elif file_ext in image_extensions or (file.content_type and "image" in file.content_type):
            upload_type = UploadType.PHOTO
        else:
            # Default to transcript for unknown types
            upload_type = UploadType.TRANSCRIPT
        
        # Save file
        file_ext = os.path.splitext(file.filename)[1]
        file_path = os.path.join(settings.UPLOAD_PATH, f"{case_id}_{file.filename}")
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Calculate SHA256
        sha256 = hashlib.sha256(content).hexdigest()
        
        # Check for duplicate
        existing = self.db.query(Upload).filter(Upload.sha256 == sha256).first()
        if existing:
            return existing
        
        # Create upload record
        upload = Upload(
            case_id=case_id,
            type=upload_type,
            filename=file.filename,
            path=file_path,
            sha256=sha256
        )
        self.db.add(upload)
        self.db.commit()
        self.db.refresh(upload)
        
        # If transcript, parse and create segments
        if upload_type == UploadType.TRANSCRIPT:
            await self._parse_transcript(case_id, file_path, content)
        
        return upload
    
    async def _parse_transcript(self, case_id: int, file_path: str, content: bytes):
        from app.models.transcript_segment import TranscriptSegment
        
        text = content.decode('utf-8')
        # Simple segmentation by newlines (can be enhanced with speaker detection)
        lines = text.split('\n')
        char_pos = 0
        
        for idx, line in enumerate(lines):
            line = line.strip()
            if not line:
                char_pos += len(line) + 1
                continue
            
            start_char = char_pos
            end_char = char_pos + len(line)
            
            segment = TranscriptSegment(
                case_id=case_id,
                idx=idx,
                speaker=None,  # Can be enhanced with speaker detection
                text=line,
                start_char=start_char,
                end_char=end_char
            )
            self.db.add(segment)
            char_pos = end_char + 1
        
        self.db.commit()
    
    def list_uploads(self, case_id: int):
        return self.db.query(Upload).filter(Upload.case_id == case_id).all()

