from typing import Dict, Any, List

class RequirementsValidator:
    """Validate extracted requirements against required fields"""
    
    REQUIRED_FIELDS = [
        "workpiece.weight_range",
        "process.count",
        "process.needs_flip",
        "machines.count"
    ]
    
    def validate(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate requirements and return validation result
        Returns: {
            "valid": bool,
            "missing_fields": List[str],
            "open_questions": List[str]
        }
        """
        missing_fields = []
        open_questions = requirements.get("open_questions", [])
        
        for field_path in self.REQUIRED_FIELDS:
            if not self._get_field_value(requirements, field_path):
                missing_fields.append(field_path)
                # Add to open_questions if not already there
                question = f"缺少必要欄位：{field_path}"
                if question not in open_questions:
                    open_questions.append(question)
        
        return {
            "valid": len(missing_fields) == 0,
            "missing_fields": missing_fields,
            "open_questions": open_questions
        }
    
    def _get_field_value(self, data: Dict[str, Any], field_path: str) -> Any:
        """Get nested field value by dot-separated path"""
        parts = field_path.split(".")
        value = data
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return None
            if value is None:
                return None
        return value

