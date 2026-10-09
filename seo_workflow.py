import os

from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.researcher import create_researcher
from agents.writer import create_writer
from agents.seo_checker import create_seo_checker
from agents.reviewer import create_reviewer


load_dotenv()


def get_model_client():

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing from the .env file."
        )

    return OpenAIChatCompletionClient(
        model=model,
        api_key=api_key,
    )


async def run_agent(agent, task):

    result = await agent.run(task=task)

    if not result.messages:
        return "No response generated."

    last_message = result.messages[-1]

    content = getattr(last_message, "content", None)

    if content is None:
        return str(last_message)

    return str(content)


async def run_seo_workflow(topic):

    model_client = get_model_client()

    try:

        # ==========================================
        # AGENT 1
        # SEO RESEARCHER
        # ==========================================

        researcher = create_researcher(model_client)

        research = await run_agent(
            researcher,
            f"""
            Research the following topic:

            {topic}

            Use the web search tool.

            Provide detailed SEO research for the content writer.
            """,
        )


        # ==========================================
        # AGENT 2
        # CONTENT WRITER
        # ==========================================

        writer = create_writer(model_client)

        draft = await run_agent(
            writer,
            f"""
            Create an SEO article about:

            {topic}

            Use the following research:

            -------------------------
            RESEARCH
            -------------------------

            {research}

            -------------------------
            END RESEARCH
            -------------------------

            Create the complete first draft.
            """,
        )


        # ==========================================
        # AGENT 3
        # SEO CHECKER
        # ==========================================

        seo_checker = create_seo_checker(model_client)

        seo_audit = await run_agent(
            seo_checker,
            f"""
            Original topic:

            {topic}


            SEO RESEARCH:

            {research}


            DRAFT ARTICLE:

            {draft}


            Analyze the draft and provide a detailed SEO audit.
            """,
        )


        # ==========================================
        # AGENT 4
        # FINAL REVIEWER
        # ==========================================

        reviewer = create_reviewer(model_client)

        final_content = await run_agent(
            reviewer,
            f"""
            Original Topic:

            {topic}


            SEO RESEARCH:

            {research}


            DRAFT ARTICLE:

            {draft}


            SEO AUDIT:

            {seo_audit}


            Create the final polished SEO article.
            """,
        )


        return {
            "research": research,
            "draft": draft,
            "seo_audit": seo_audit,
            "final_content": final_content,
        }

    finally:

        await model_client.close()