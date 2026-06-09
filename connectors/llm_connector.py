from __future__ import annotations

import json
import os
from typing import Any


PROVIDERS = {
    "9router": {
        "base_url": "https://9router.com/api/v1",
        "api_key_env": "9ROUTER_API_KEY",
        "base_url_env_alt": "ROUTER9_BASE_URL",
        "api_key_env_alt": "ROUTER9_API_KEY",
        "default_model": "oc/deepseek-v4-flash-free",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key_env": "OPENROUTER_API_KEY",
        "default_model": "poolside/laguna-m.1:free",
        "models": [
            "poolside/laguna-m.1:free",
            "z-ai/glm-4.5-air:free",
            "nvidia/nemotron-3-ultra-550b-a55b:free",
            "sourceful/riverflow-v2.5-pro:free",
            "nvidia/nemotron-3-super-120b-a12b:free",
            "meta-llama/llama-3.3-70b-instruct:free",
            "openrouter/free",
        ],
    },
}

_DEFAULT_PROVIDER = os.environ.get("LLM_PROVIDER") or os.environ.get("AK_LLM_PROVIDER") or "auto"


def _get_env(name: str, alt: str | None = None) -> str:
    val = os.environ.get(name)
    if not val and alt:
        val = os.environ.get(alt)
    return val or ""


def _build_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    if not base.endswith("/chat/completions"):
        base = base + "/chat/completions"
    return base


def _provider_api_key(provider: str) -> str:
    cfg = PROVIDERS[provider]
    return _get_env(cfg["api_key_env"], cfg.get("api_key_env_alt"))


def _provider_base_url(provider: str) -> str:
    cfg = PROVIDERS[provider]
    env_url = _get_env(
        f"{provider.upper()}_BASE_URL",
        cfg.get("base_url_env_alt"),
    )
    if env_url:
        return _build_url(env_url)
    return _build_url(cfg["base_url"])


def _provider_models(provider: str) -> list[str]:
    cfg = PROVIDERS[provider]
    env_model = os.environ.get(f"{provider.upper()}_MODEL")
    if env_model:
        return [env_model]
    models = cfg.get("models")
    if models:
        return list(models)
    return [cfg["default_model"]]


class LLMConnector:
    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
        provider: str | None = None,
    ):
        self._provider = (provider or _DEFAULT_PROVIDER).strip().lower()
        self._explicit_api_key = api_key
        self._explicit_model = model
        self._explicit_base_url = base_url

    @property
    def provider_name(self) -> str:
        if self._provider == "auto":
            return self._provider_list()[0] if self._provider_list() else "9router"
        return self._provider

    def is_available(self) -> bool:
        if self._explicit_api_key:
            return True
        return any(bool(_provider_api_key(p)) for p in self._provider_list())

    def _provider_list(self) -> list[str]:
        if self._provider == "auto":
            candidates = ["9router", "openrouter"]
            return [p for p in candidates if _provider_api_key(p)] or ["9router"]
        return [self._provider]

    def _model_list(self, provider: str) -> list[str]:
        if self._explicit_model:
            return [self._explicit_model]
        return _provider_models(provider)

    def execute(self, prompt: str, **kwargs: Any) -> dict:
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, **kwargs)

    def chat(self, messages: list[dict], **kwargs: Any) -> dict:
        providers = self._provider_list()
        if not providers:
            return self._mock_response(str(messages))

        for provider in providers:
            models = self._model_list(provider)
            for model in models:
                result = self._try_chat(provider, model, messages, **kwargs)
                if result["success"]:
                    return result
        return {"success": False, "content": "", "error": "All providers and models failed", "mode": "api", "provider": self._provider}

    def _try_chat(self, provider: str, model: str, messages: list[dict], **kwargs: Any) -> dict:
        api_key = self._explicit_api_key or _provider_api_key(provider)
        if not api_key:
            return {"success": False, "content": "", "error": f"no api key for {provider}", "mode": "api", "provider": provider}

        base_url = self._explicit_base_url or _provider_base_url(provider)

        try:
            import urllib.request

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            if provider == "openrouter":
                headers["HTTP-Referer"] = "https://github.com/ak/agents"
                headers["X-Title"] = "AK Agent"

            payload = json.dumps({
                "model": model,
                "messages": messages,
                "max_tokens": kwargs.get("max_tokens", 512),
                "temperature": kwargs.get("temperature", 0.7),
            }).encode("utf-8")

            req = urllib.request.Request(
                base_url,
                data=payload,
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=kwargs.get("timeout", 30)) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            return {
                "success": True,
                "content": result["choices"][0]["message"]["content"],
                "model": result.get("model", model),
                "usage": result.get("usage", {}),
                "mode": "api",
                "provider": provider,
            }
        except Exception as e:
            return {"success": False, "content": "", "error": str(e), "mode": "api", "provider": provider}

    def _mock_response(self, prompt: str) -> dict:
        return {
            "success": True,
            "content": f"[MOCK:{self._provider}] Analyzed: {prompt[:100]}...",
            "model": "mock",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "mode": "mock",
            "provider": self._provider,
        }
