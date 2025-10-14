from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI, OpenAIError


class AIProviderError(RuntimeError):
    """Error de alto nivel para la generación de contenido asistido por IA."""


class AIContentProvider(ABC):
    """Contrato para servicios que generan descripciones e imágenes de espacios deportivos."""

    @abstractmethod
    def generate_description(self, nombre: str, palabras: int = 60) -> str:
        """Genera una descripción en lenguaje natural para un espacio deportivo."""

    @abstractmethod
    def generate_image_url(self, nombre: str) -> str:
        """Genera (o recupera) la URL de una imagen representativa del espacio deportivo."""


@dataclass
class OpenAIContentProvider(AIContentProvider):
    """Implementación concreta basada en OpenAI."""

    api_key: str
    description_model: str = "gpt-3.5-turbo"
    image_model: str = "dall-e-3"
    temperature: float = 0.7

    def __post_init__(self) -> None:
        if not self.api_key:
            raise AIProviderError(
                "La clave de API de OpenAI no está configurada; define OPENAI_API_KEY o proporciona 'api_key'."
            )
        self._client = OpenAI(api_key=self.api_key)

    def generate_description(self, nombre: str, palabras: int = 60) -> str:
        prompt = (
            "Describe brevemente el espacio deportivo llamado '{nombre}' que puede ser reservado por estudiantes "
            "en una universidad." if palabras <= 70 else
            "Describe en aproximadamente {palabras} palabras el espacio deportivo llamado '{nombre}' que puede ser "
            "reservado por estudiantes en una universidad."
        ).format(nombre=nombre, palabras=palabras)

        try:
            respuesta = self._client.chat.completions.create(
                model=self.description_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente que describe espacios deportivos universitarios.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max(100, palabras + 20),
                temperature=self.temperature,
            )
        except OpenAIError as exc:
            raise AIProviderError(f"Error al generar la descripción: {exc}") from exc

        descripcion = respuesta.choices[0].message.content.strip()
        if not descripcion:
            raise AIProviderError("No se recibió contenido de la API de OpenAI.")
        return descripcion

    def generate_image_url(self, nombre: str) -> str:
        try:
            response_img = self._client.images.generate(
                model=self.image_model,
                prompt=(
                    "Ilustración digital de un espacio deportivo universitario llamado '{nombre}', "
                    "moderno y bien iluminado"
                ).format(nombre=nombre),
                size="1024x1024",
                quality="standard",
                n=1,
            )
        except OpenAIError as exc:
            raise AIProviderError(f"Error al generar la imagen: {exc}") from exc

        if not response_img.data:
            raise AIProviderError("La respuesta de OpenAI no contiene datos de imagen.")
        return response_img.data[0].url
