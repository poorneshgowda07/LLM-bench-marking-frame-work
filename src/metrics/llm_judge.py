"""LLM-as-a-Judge evaluation."""
import os
from typing import Dict, Any, Optional
from src.providers.factory import get_provider
from src.utils.logger import logger

class LLMJudge:
    def __init__(self, judge_model_id: str = "gpt-4o-mini"):
        # For mock test, if not OpenAI key, fallback to mock judge
        if not os.environ.get("OPENAI_API_KEY") and judge_model_id != "mock":
            logger.warning("No OPENAI_API_KEY, falling back to mock judge")
            judge_model_id = "mock"
        
        self.provider = get_provider(judge_model_id)
        
    def evaluate(self, prompt: str, prediction: str, reference: str, criteria: str = "") -> Dict[str, Any]:
        """Use LLM to evaluate the prediction against the reference."""
        if not prediction:
            return {"score": 0.0, "reasoning": "Empty prediction"}
            
        sys_prompt = "You are an expert evaluator. Evaluate the prediction against the reference. Output a score from 0.0 to 1.0 and reasoning. Format as JSON: {'score': float, 'reasoning': string}"
        
        eval_prompt = f"Prompt: {prompt}\n\nReference: {reference}\n\nPrediction: {prediction}\n\nCriteria: {criteria}"
        
        try:
            response = self.provider.complete(eval_prompt, system_prompt=sys_prompt, options={"temperature": 0.0, "max_tokens": 150})
            if "mock" in self.provider.model_id:
                # Mock response
                return {"score": 0.85, "reasoning": "Mock judge evaluation"}
                
            # Naive parse - in production we'd use robust JSON parsing
            import json
            import re
            
            # extract json block
            match = re.search(r'\{.*\}', response.prediction, re.DOTALL)
            if match:
                res = json.loads(match.group(0))
                return {"score": float(res.get("score", 0.0)), "reasoning": res.get("reasoning", "")}
            return {"score": 0.0, "reasoning": "Failed to parse judge output"}
        except Exception as e:
            logger.error(f"LLM Judge error: {e}")
            return {"score": 0.0, "reasoning": str(e)}
