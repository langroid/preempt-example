"""
Run this from project root:

pytest tests/test-llm-chat.py

"""
from rich import print
import langroid as lr
import langroid.language_models as lm
from preempt_example.common.utils import sanitize_names_money, desanitize_money_names

def test_llm_sanitized_chat(
    model: str=""
) -> str:
    """
    Safely call a chat LLM with the given text.

    Args:
        text (str): Text to send to the LLM.

    Returns:
        str: Response from the LLM.
    """

    llm_config = lm.OpenAIGPTConfig(
        chat_model=model or lm.OpenAIChatModel.GPT4_1_MINI,
    )
    agent = lr.ChatAgent(lr.ChatAgentConfig(llm=llm_config))


    text = """
    Jack Ma made $100,000 last year. He gave half of it to Vinod Singh.
    How much did Vinod get? Give the EXACT amount within square brackets
    so I can parse it out. 
    """
    # Sanitize the text
    sanitized_text = sanitize_names_money([text])[0]
    print(f"[cyan][Sanitized]:{sanitized_text}[/cyan]")
    response = agent.llm_response(sanitized_text)
    if response.metadata.cached or not response.metadata.displayed:
        print(f"[green]{response.content}[/green]")

    # Desanitize the response
    desan_msg = desanitize_money_names([response.content])[0]
    print(f"[bold green]{desan_msg}[/bold green]")
    # extract amount within square brackets
    amount = desan_msg.split("[")[1].split("]")[0]
    assert "50,000" in amount or "50000" in amount, f"Expected 50,000 or 50000, got {amount}"

if __name__ == "__main__":
    Fire(main)
