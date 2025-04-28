from typing import Any, List, Optional
import os
import requests
import aiohttp
from pydantic import Field

from langchain_core.language_models import BaseChatModel, BaseLLM
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, Generation, LLMResult, ChatResult


class ChatSiliconFlow(BaseChatModel):
    """Chat model for SiliconFlow API."""

    api_key: str = Field(
        default_factory=lambda: os.environ.get("SILICONFLOW_API_KEY", "")
    )
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 2048
    
    @property
    def _llm_type(self) -> str:
        """Return type of chat model."""
        return "siliconflow"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResult:  # 修改返回类型为 ChatResult
        """Generate chat completion from SiliconFlow API."""
        if not self.api_key:
            raise ValueError("SiliconFlow API key is not set")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "messages": [{
                "role": "user" if isinstance(msg, HumanMessage) else "assistant",
                "content": msg.content
            } for msg in messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False  # 明确关闭流式输出
        }
        
        if stop:
            payload["stop"] = stop
        
        try:
            response = requests.post(
                "https://api.siliconflow.cn/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            if "choices" not in result:
                raise ValueError("Invalid API response format: missing 'choices' field")

            # 转换为 ChatGeneration 列表
            generations = [ChatGeneration(
                message=AIMessage(content=choice["message"]["content"])
            ) for choice in result["choices"]]

            return ChatResult(generations=generations)  # 返回 ChatResult 类型
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"SiliconFlow API request failed: {str(e)}")
        except requests.exceptions.JSONDecodeError as e:
            raise ValueError(f"Failed to decode API response: {str(e)}")

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Async generate chat completion from SiliconFlow API."""
        if not self.api_key:
            raise ValueError("SiliconFlow API key is not set")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user" if isinstance(msg, HumanMessage) else "assistant", 
                          "content": msg.content} for msg in messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False,  # 添加 stream 参数
            **kwargs
        }
        
        if stop:
            payload["stop"] = stop
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                async with session.post(
                    "https://api.siliconflow.cn/v1/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    response.raise_for_status()
                    result = await response.json()

                    if "choices" not in result:
                        raise ValueError("Invalid API response format: missing 'choices' field")

                    # 确保 generations 是一维列表
                    generations = [ChatGeneration(
                        message=AIMessage(content=choice["message"]["content"])
                    ) for choice in result["choices"]]

                    return LLMResult(
                        generations=generations
                    )
        except Exception as e:
            raise ConnectionError(f"SiliconFlow API request failed: {str(e)}")


class SiliconFlowLLM(BaseLLM):
    """LLM for SiliconFlow API."""

    api_key: Optional[str] = None  # 改为Optional类型
    model_name: str = "glm4"
    temperature: float = 0.7
    max_tokens: int = 2048

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        if self.api_key is None:
            self.api_key = os.getenv("SILICONFLOW_API_KEY")

    def _generate(
        self, prompts: List[str], stop: Optional[List[str]] = None, **kwargs: Any
    ) -> LLMResult:
        """Generate text from SiliconFlow API."""
        if not self.api_key:
            raise ValueError("SiliconFlow API key is not set")
            
        import requests
        import json
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "prompt": prompts[0],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            **kwargs
        }
        
        if stop:
            payload["stop"] = stop
        
        try:
            response = requests.post(
                "https://api.siliconflow.cn/v1/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if "choices" not in result:
                raise ValueError("Invalid API response format")
                
            return LLMResult(
                generations=[[Generation(text=choice["text"]) 
                             for choice in result["choices"]]]
            )
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"SiliconFlow API request failed: {str(e)}")

    async def _agenerate(
        self, prompts: List[str], stop: Optional[List[str]] = None, **kwargs: Any
    ) -> LLMResult:
        """Async generate text from SiliconFlow API."""
        if not self.api_key:
            raise ValueError("SiliconFlow API key is not set")
            
        import aiohttp
        import json
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "prompt": prompts[0],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            **kwargs
        }
        
        if stop:
            payload["stop"] = stop
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                async with session.post(
                    "https://api.siliconflow.cn/v1/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
                    
                    if "choices" not in result:
                        raise ValueError("Invalid API response format")
                        
                    return LLMResult(
                        generations=[[Generation(text=choice["text"]) 
                                     for choice in result["choices"]]]
                    )
        except Exception as e:
            raise ConnectionError(f"SiliconFlow API request failed: {str(e)}")