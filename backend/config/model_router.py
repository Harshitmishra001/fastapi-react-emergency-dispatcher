from langchain_openai import ChatOpenAI
from typing import Literal
from backend.config.settings import settings

ModelTier = Literal["local", "strong"]

def get_llm(tier: ModelTier, temperature: float = 0.0) -> ChatOpenAI:
    """
    Model selection factory that resolves the LLM by tier.
    Both tiers use the same LM Studio endpoint for now.
    The 'strong' tier is isolated so it can be repointed to a better model
    without changing any agent code — just update LM_STUDIO_MODEL in .env.
    # ponytail: both tiers same model, split when a real strong-tier is added
    """
    return ChatOpenAI(
        base_url=settings.LM_STUDIO_BASE_URL,
        api_key=settings.LM_STUDIO_API_KEY,  # type: ignore
        model=settings.LM_STUDIO_MODEL,
        temperature=temperature
    )

