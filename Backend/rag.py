from pydantic import BaseModel, Field
from llm import get_llm


class HealthAdvice(BaseModel):
    symptom_summary: str = Field(
        description="A 2-3 sentence plain-language answer to the question, written entirely in the target language."
    )
    prevention_steps: list[str] = Field(
        description=(
            "3-6 concrete, actionable prevention or self-care steps, each a short sentence, "
            "written entirely in the target language. Empty list if the context has none."
        )
    )
    when_to_seek_care: str = Field(
        description=(
            "1-3 sentences naming concrete warning signs that mean the person should see a doctor or "
            "seek emergency care, written entirely in the target language."
        )
    )
    disclaimer: str = Field(
        description=(
            "A short medical disclaimer, written entirely in the target language, stating this is general "
            "health information and not a diagnosis, and that a healthcare professional or emergency "
            "services should be consulted for real symptoms or urgent situations."
        )
    )
    
PROMPT_TEMPLATE = """You are a public health information assistant. Answer the user's health question
using ONLY the information in the context below, drawn from WHO guidelines and health ministry documents.

Respond entirely in {language} — every field of your answer, including the disclaimer, must be written
in {language}, regardless of what language the context below is written in.

Be specific: name concrete symptoms, prevention actions, and warning signs whenever the context provides
them, rather than vague generalities. If the context doesn't fully answer the question, say so plainly in
the symptom summary instead of guessing. You are not a doctor — never phrase anything as a diagnosis, and
always name concrete signs that mean the person should seek professional or emergency medical care.

Question: {question}

Context:
{context}
"""
NO_DOCUMENTS_ADVICE = HealthAdvice(
    symptom_summary="No health documents have been uploaded yet, so I can't answer that from a real source.",
    prevention_steps=[],
    when_to_seek_care="If you have concerning symptoms right now, contact a healthcare professional or emergency services — don't wait on this app.",
    disclaimer="This app provides general information from uploaded documents only, never a diagnosis. Always consult a healthcare professional, or emergency services for urgent symptoms.",
)


def generate_answer(question, chunks, language="English"):
    if not chunks:
        return NO_DOCUMENTS_ADVICE, []

    context = "\n\n---\n\n".join(
        "[From: " + c["document_title"] + "]\n" + c["text"]
        for c in chunks
    )
    prompt = PROMPT_TEMPLATE.format(question=question, context=context, language=language)

    structured_llm = get_llm().with_structured_output(HealthAdvice)
    advice = structured_llm.invoke(prompt)

    sources = []
    seen_titles = set()
    for c in chunks:
        if c["document_title"] not in seen_titles:
            seen_titles.add(c["document_title"])
            sources.append(c["document_title"])

    return advice, sources
        