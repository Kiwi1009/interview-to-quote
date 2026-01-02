import json
import hashlib
from typing import Dict, Any, List
from openai import OpenAI
from app.core.config import settings
from app.models.transcript_segment import TranscriptSegment

class LLMService:
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.LLM_BASE_URL,
            api_key=settings.LLM_API_KEY
        )
        self.model_name = settings.LLM_MODEL_TEXT
    
    def extract_requirements(self, transcript_text: str, segments: List[TranscriptSegment]) -> Dict[str, Any]:
        """Extract requirements from transcript using LLM"""
        prompt = self._build_extraction_prompt(transcript_text)
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1  # Low temperature for consistency
        )
        
        result_json = json.loads(response.choices[0].message.content)
        
        # Map evidence to segments
        evidence_list = []
        if "evidence" in result_json:
            for ev in result_json["evidence"]:
                # Find matching segment
                segment_idx = self._find_segment_for_snippet(ev["snippet"], segments)
                ev["segment_idx"] = segment_idx
                evidence_list.append(ev)
        
        return {
            "requirements": result_json.get("requirements", {}),
            "confidence": result_json.get("confidence", {}),
            "evidence": evidence_list,
            "prompt_hash": prompt_hash
        }
    
    def _get_system_prompt(self) -> str:
        return """你是一個自動化系統需求分析專家。請從訪談逐字稿中提取結構化的需求資訊。

規則：
1. 只提取逐字稿中明確提到的資訊，不要發明數據
2. 如果某個欄位未知，設為 null 並加入 open_questions 清單
3. 使用繁體中文（台灣用法）填寫所有文字欄位
4. 對於每個提取的欄位，提供證據片段（snippet）和位置資訊
5. 為每個主要區塊提供信心分數（0-1）

輸出格式必須是 JSON，包含：
- requirements: 提取的需求結構
- confidence: 各區塊的信心分數
- evidence: 證據列表，每個包含 field_path, snippet, start_char, end_char"""
    
    def _build_extraction_prompt(self, transcript_text: str) -> str:
        return f"""請從以下訪談逐字稿中提取自動化系統需求：

{transcript_text}

請提取以下結構的需求資訊：
- customer_pain_points: 客戶痛點（陣列）
- products: 產品資訊（物件，包含 name, material, dimensions 等）
- workpiece: 工件資訊（物件，包含 weight_range, dimensions, material 等）
- process: 製程資訊（物件，包含 count, steps, needs_flip 等）
- cycle_time: 週期時間（物件，包含 current, target 等）
- layout: 佈局資訊（物件，包含 space_constraints, existing_equipment 等）
- constraints: 限制條件（物件，包含 budget, timeline, technical 等）
- options: 選項偏好（物件，包含 robot_type, automation_level 等）
- acceptance: 驗收標準（物件，包含 criteria, tests 等）
- open_questions: 開放問題（陣列，包含 priority）

請以 JSON 格式回應，包含 requirements, confidence, evidence 三個主要欄位。"""
    
    def _find_segment_for_snippet(self, snippet: str, segments: List[TranscriptSegment]) -> int:
        """Find the segment index that contains the snippet"""
        snippet_lower = snippet.lower().strip()
        for segment in segments:
            if snippet_lower in segment.text.lower():
                return segment.idx
        return None

