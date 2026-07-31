from langchain_openai import ChatOpenAI
from typing import Literal

ModelTier = Literal["local", "strong"]

def get_llm(tier: ModelTier, temperature: float = 0.0) -> ChatOpenAI:
    """
    Model selection factory that resolves the LLM by tier.
    Currently, both tiers point to the local LM Studio instance running smollm3-3b.
    The 'strong' tier can be repointed to a more capable model in the future without changing agent code.
    """
    
    # LM Studio default configuration
    base_url = "http://10.90.216.24:1234/v1"
    api_key = "lm-studio"
    model_name = "smollm3-3b"
    
    if tier == "local":
        return ChatOpenAI(
            base_url=base_url,
            api_key=api_key, # type: ignore
            model=model_name,
            temperature=temperature
        )
    elif tier == "strong":
        # Evaluator Agent uses the strong tier.
        # Currently aliased to local, but isolated for future upgrade.
        return ChatOpenAI(
            base_url=base_url,
            api_key=api_key, # type: ignore
            model=model_name,
            temperature=temperature
        )
    else:
        raise ValueError(f"Unknown model tier: {tier}")
