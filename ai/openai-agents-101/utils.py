import base64
import os

import nest_asyncio
import logfire
from agents import set_default_openai_client
from openai import AsyncOpenAI


def setup_trace(name: str):
    # Build Basic Auth header.
    LANGFUSE_AUTH = base64.b64encode(
        f"{os.environ['LANGFUSE_PUBLIC_KEY']}:{os.environ['LANGFUSE_SECRET_KEY']}".encode()
    ).decode()

    # Configure OpenTelemetry endpoint & headers
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = os.environ["LANGFUSE_HOST"] + "/api/public/otel"
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"


    nest_asyncio.apply()
    # Configure logfire instrumentation.
    logfire.configure(
        service_name=name,
        send_to_logfire=False,
    )
    # This method automatically patches the OpenAI Agents SDK to send logs via OTLP to Langfuse.
    logfire.instrument_openai_agents()


def setup_openai():
    custom_client = AsyncOpenAI(base_url=os.environ['OPENAI_URL_BASE'],
                                api_key=os.environ['OPENAI_API_KEY'],)
    set_default_openai_client(custom_client)
